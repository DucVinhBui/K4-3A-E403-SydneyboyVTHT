"""Kiểm chứng knowledge base — `codebase/knowledge/`.

Chạy từ thư mục `codebase/`:

    ../.venv/bin/python -m eval.run_kb_check                 # tất cả topic
    ../.venv/bin/python -m eval.run_kb_check --topic grounding
    ../.venv/bin/python -m eval.run_kb_check --structure-only  # không gọi API

Hai tầng kiểm:

A. **Cấu trúc** (không tốn tiền, không cần mạng) — mọi pack phải nạp được,
   mã đoạn không trùng, mọi tiêu chí và câu hỏi đào sâu phải trỏ tới mã CÓ
   THẬT trong pack. Đây là chốt chống bịa mã đoạn.

B. **Hành vi** (gọi AI thật) — chạy `eval/kb_cases.json` với TỪNG pack:
   - ca `shared`: bài lạc lĩnh vực phải ra NGOÀI_PHẠM_VI ở MỌI pack, kể cả
     khi bài rất ngắn ("mỳ cay"); bài đúng đề nhưng chưa có nội dung phải ra
     THIẾU_CĂN_CỨ.
   - ca `by_topic`: đủ ý → ĐỦ_CĂN_CỨ, thiếu ý → THIẾU_CĂN_CỨ, khái niệm khác
     → NGOÀI_PHẠM_VI.
   Ngoài state, còn kiểm mọi `source_id` agent trích ra đều nằm trong pack.

Đổi pack bằng `MINILAB_TOPIC`, nên mỗi topic chạy trong một tiến trình con
riêng (module `agent.sources` đọc biến môi trường lúc import).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CASES_PATH = ROOT / "eval" / "kb_cases.json"


def check_structure() -> list[str]:
    """Nạp mọi pack và kiểm tính toàn vẹn. Trả về danh sách lỗi."""
    from agent.sources import load_topics

    errors: list[str] = []
    try:
        topics = load_topics()
    except Exception as exc:  # noqa: BLE001
        return [f"không nạp được knowledge base: {exc}"]

    for name, t in sorted(topics.items()):
        ids = {e.id for e in t.excerpts}
        if len(t.criteria) < 1:
            errors.append(f"{name}: không có tiêu chí nào")
        for c in t.criteria:
            if c.src not in ids:
                errors.append(f"{name}: tiêu chí {c.key} trỏ tới mã lạ {c.src}")
            if not c.probe.strip():
                errors.append(f"{name}: tiêu chí {c.key} thiếu câu hỏi ngược")
        if t.deep_probe_src not in ids:
            errors.append(f"{name}: deep_probe trỏ tới mã lạ {t.deep_probe_src}")
        for e in t.excerpts:
            if len(e.text) < 20:
                errors.append(f"{name}: đoạn {e.id} quá ngắn, khó làm căn cứ")
        print(f"  {name:18s} {len(t.excerpts)} đoạn · {len(t.criteria)} tiêu chí · {t.scope_range}")
    return errors


def _run_topic_worker(topic: str) -> dict:
    """Chạy phần hành vi của một topic trong tiến trình con (MINILAB_TOPIC)."""
    env = dict(os.environ, MINILAB_TOPIC=topic)
    proc = subprocess.run(
        [sys.executable, "-m", "eval.run_kb_check", "--worker", topic],
        cwd=ROOT, env=env, capture_output=True, text=True,
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        return {"topic": topic, "error": proc.stderr.strip()[-600:], "rows": []}
    try:
        return json.loads(proc.stdout[proc.stdout.index("{"):])
    except (ValueError, json.JSONDecodeError):
        return {"topic": topic, "error": (proc.stdout + proc.stderr)[-600:], "rows": []}


def _worker(topic: str) -> None:
    """Chạy trong tiến trình con: MINILAB_TOPIC đã được set trước khi import."""
    from agent import StateCheckAgent
    from agent.config import load_settings
    from agent.sources import EXCERPTS_BY_ID

    cases_all = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    cases = [dict(c, kind="shared") for c in cases_all["shared"]]
    cases += [dict(c, kind="topic") for c in cases_all["by_topic"].get(topic, [])]

    agent = StateCheckAgent.from_settings(load_settings())
    rows = []
    for c in cases:
        try:
            d = agent.decide(c["input"])
            cited = [p.source_id for p in d.probes]
            bad = [s for s in cited if s.strip().upper() not in EXCERPTS_BY_ID]
            rows.append({
                "id": c["id"], "kind": c["kind"], "expect": c["expect"], "got": d.state,
                "pass": d.state == c["expect"], "bad_citations": bad,
                "input": c["input"][:60], "why": c.get("why", ""),
            })
        except Exception as exc:  # noqa: BLE001
            rows.append({
                "id": c["id"], "kind": c["kind"], "expect": c["expect"],
                "got": f"LỖI: {type(exc).__name__}", "pass": False,
                "bad_citations": [], "input": c["input"][:60], "why": c.get("why", ""),
            })
    print(json.dumps({"topic": topic, "rows": rows}, ensure_ascii=False))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", help="chỉ chạy một topic")
    ap.add_argument("--structure-only", action="store_true", help="bỏ qua phần gọi AI")
    ap.add_argument("--worker", help=argparse.SUPPRESS)
    ap.add_argument("--out", default="eval/kb_check_results.json")
    args = ap.parse_args()

    if args.worker:
        _worker(args.worker)
        return 0

    print("A · CẤU TRÚC knowledge base")
    errors = check_structure()
    if errors:
        for e in errors:
            print(f"  ❌ {e}")
        print(f"\n{len(errors)} lỗi cấu trúc — dừng, không chạy phần hành vi.")
        return 1
    print("  ✅ mọi pack hợp lệ, không có mã đoạn nào trỏ ra ngoài\n")

    if args.structure_only:
        return 0

    from agent.sources import load_topics
    topics = [args.topic] if args.topic else sorted(load_topics())

    print("B · HÀNH VI (gọi AI thật)")
    all_rows, total, passed = [], 0, 0
    for t in topics:
        res = _run_topic_worker(t)
        if res.get("error"):
            print(f"\n  {t}: ❌ {res['error']}")
            continue
        print(f"\n  ── {t}")
        for r in res["rows"]:
            total += 1
            passed += bool(r["pass"])
            mark = "✅" if r["pass"] else "❌"
            note = f"  ⚠️ trích mã lạ {r['bad_citations']}" if r["bad_citations"] else ""
            print(f"  {mark} {r['id']:7s} {r['input'][:44]:46s} → {r['got']:15s} (cần {r['expect']}){note}")
            all_rows.append(dict(r, topic=t))

    pct = 100.0 * passed / total if total else 0.0
    print(f"\nTỔNG: {passed}/{total} = {pct:.1f}%")
    bad_cite = [r for r in all_rows if r["bad_citations"]]
    print(f"Trích mã đoạn không có trong pack: {len(bad_cite)}/{total}")

    out = ROOT / args.out
    out.write_text(json.dumps(
        {"total": total, "passed": passed, "percent": round(pct, 1),
         "bad_citation_rows": len(bad_cite), "rows": all_rows},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Đã ghi {out.relative_to(ROOT)}")
    return 0 if passed == total else 2


if __name__ == "__main__":
    raise SystemExit(main())
