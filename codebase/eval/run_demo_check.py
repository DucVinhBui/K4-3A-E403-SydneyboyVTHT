"""Kiểm tra trước khi bấm quay — chạy đúng những gì sẽ bấm trong 30 giây.

    cd codebase
    ../.venv/bin/python -m eval.run_demo_check

Bắn thẳng vào server ĐANG CHẠY (không import agent), nên nó kiểm đúng thứ
người xem sẽ thấy: server sống chưa, đang là AI thật hay mock, knowledge base
nào đang nạp, bốn nút demo có ra đúng bốn nhánh không, và mỗi lượt mất bao lâu
— số giây này là thứ quyết định kịch bản 30 giây có vừa hay không.
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _get(base: str, path: str):
    with urllib.request.urlopen(base + path, timeout=30) as r:
        return json.load(r)


def _decide(base: str, text: str) -> tuple[float, dict]:
    req = urllib.request.Request(
        base + "/api/decide",
        data=json.dumps({"explanation": text}).encode(),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=180) as r:
        return time.time() - t0, json.load(r)


def _presets() -> list[str]:
    """Lấy đúng 4 câu nằm sau 4 nút demo trong bản mẫu."""
    html = (ROOT / "prototype" / "index.html").read_text(encoding="utf-8")
    blk = re.search(r"var PRESET = \[(.*?)\n  \];", html, re.S).group(1)
    out = re.findall(r'"((?:[^"\\]|\\.)*)"', blk)
    return out[:3]  # nút ④ ghép từ đoạn nguồn lúc chạy, xử lý riêng


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:8765")
    args = ap.parse_args()
    base = args.base.rstrip("/")

    print(f"Server: {base}\n")
    try:
        cfg = _get(base, "/api/config")
        scope = _get(base, "/api/scope")
    except (urllib.error.URLError, OSError) as exc:
        print(f"❌ Không gọi được server: {exc}")
        print("   Chạy: cd codebase && ../.venv/bin/python -m api.server --port 8765")
        return 1

    problems = []

    live = cfg.get("provider") not in (None, "", "mock")
    print(f"{'✅' if live else '❌'} Provider: {cfg.get('provider')} / {cfg.get('model')}"
          + ("" if live else "   ← đang MOCK, quay là hỏng"))
    if not live:
        problems.append("provider đang là mock")

    print(f"✅ Knowledge base: {scope['topic']} · {scope['scope_range']} · {len(scope['excerpts'])} đoạn")
    print(f"   {scope['source_label']}\n")

    ids = {e["id"] for e in scope["excerpts"]}
    presets = _presets()
    paste = scope["excerpts"][0]["text"] + " " + scope["excerpts"][1]["text"]
    plan = [
        ("① Trả lời đủ ý",          presets[0], "ĐỦ_CĂN_CỨ"),
        ("② Trả lời thiếu ý",       presets[1], "THIẾU_CĂN_CỨ"),
        ("③ Nói sang chuyện khác",  presets[2], "NGOÀI_PHẠM_VI"),
        ("④ Dán nguyên văn",        paste,      "THIẾU_CĂN_CỨ"),
        ("(gõ tay) mỳ cay",         "mỳ cay",   "NGOÀI_PHẠM_VI"),
    ]

    total = 0.0
    for label, text, want in plan:
        try:
            dt, d = _decide(base, text)
        except (urllib.error.URLError, OSError) as exc:
            print(f"❌ {label:24s} lỗi gọi API: {exc}")
            problems.append(f"{label}: lỗi API")
            continue
        total += dt
        ok = d["state"] == want
        notes = []
        if d["state"] == "THIẾU_CĂN_CỨ" and len(d["probes"]) != 2:
            notes.append(f"chỉ có {len(d['probes'])} câu hỏi ngược, cần đúng 2")
        bad = [p["source_id"] for p in d["probes"] if p["source_id"] not in ids]
        if bad:
            notes.append(f"trích mã lạ {bad}")
        if not ok:
            notes.append(f"cần {want}")
        if notes:
            problems.append(f"{label}: {'; '.join(notes)}")
        mark = "✅" if ok and not notes else "❌"
        cited = [p["source_id"] for p in d["probes"]]
        print(f"{mark} {label:24s} {dt:4.1f}s → {d['state']:14s} {cited}"
              + (f"   ⚠️ {'; '.join(notes)}" if notes else ""))

    n = len(plan)
    print(f"\nTrung bình {total / n:.1f}s mỗi lượt gọi — kịch bản 30 giây chỉ nên "
          f"chứa MỘT lượt chờ AI.")

    if problems:
        print("\nChưa quay được:")
        for x in problems:
            print(f"  - {x}")
        return 2
    print("\n✅ Bốn nhánh chạy đúng. Quay được.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
