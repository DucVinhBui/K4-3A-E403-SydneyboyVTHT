"""Chạy toàn bộ golden_set.json qua StateCheckAgent (mock hoặc LLM thật) và
in/ghi kết quả — dùng cho CP3 "đối mặt với số liệu kiểm thử thực tế".

Usage:
    python -m eval.run_golden --provider openrouter --model openai/gpt-4o-mini
    python -m eval.run_golden --provider mock
    python -m eval.run_golden --json > eval/run_results_raw.json

Tiêu chí ĐẠT một case (khớp _meta.acceptance_criteria trong golden_set.json):
  1. decision.state == expected_state
  2. nếu expected_verbatim=True thì decision.is_verbatim_paste cũng phải True
  3. mọi source_id trong decision.probes phải là mã hợp lệ trong EXCERPTS_BY_ID
     (agent không được bịa mã đoạn không tồn tại)
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path
from typing import Any

# Cho phép chạy cả `python -m eval.run_golden` (ưu tiên) lẫn `python run_golden.py`
# (chạy nhanh từ bất cứ đâu) mà không cần export PYTHONPATH. Khi chạy dưới dạng
# module, thư mục `codebase/` đã có sẵn trên sys.path; khi chạy như script, ta tự
# chèn. Hàm `ensure_codebase_on_path()` idempotent nên không gây trùng lặp.
def ensure_codebase_on_path() -> None:
    codebase_root = Path(__file__).resolve().parent.parent  # .../codebase
    if str(codebase_root) not in sys.path:
        sys.path.insert(0, str(codebase_root))


ensure_codebase_on_path()

from agent.config import load_settings  # noqa: E402 — sys.path phải chèn trước
from agent.core import StateCheckAgent  # noqa: E402
from agent.sources import EXCERPTS_BY_ID  # noqa: E402

if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def load_golden_set() -> dict[str, Any]:
    path = Path(__file__).resolve().parent / "golden_set.json"
    return json.loads(path.read_text(encoding="utf-8"))


def check_case(case: dict[str, Any], decision) -> tuple[bool, list[str]]:
    """Trả về (pass, list lý do fail nếu có)."""
    reasons = []
    if decision.state != case["expected_state"]:
        reasons.append(f"state sai: expected={case['expected_state']}, actual={decision.state}")
    if case.get("expected_verbatim", False) and not decision.is_verbatim_paste:
        reasons.append("expected_verbatim=True nhưng decision.is_verbatim_paste=False")
    bogus_ids = [p.source_id for p in decision.probes if p.source_id not in EXCERPTS_BY_ID]
    if bogus_ids:
        reasons.append(f"agent bịa mã đoạn không tồn tại: {bogus_ids}")
    return (len(reasons) == 0), reasons


def run(provider: str, model: str | None, verbose: bool = True) -> dict[str, Any]:
    settings = load_settings()
    settings.provider = provider
    if model:
        settings.model = model
    agent = StateCheckAgent.from_settings(settings)

    golden = load_golden_set()
    results = []
    passed = 0

    for case in golden["cases"]:
        try:
            decision = agent.decide(case["input"])
            ok, reasons = check_case(case, decision)
            actual_state = decision.state
            rationale = decision.rationale
        except Exception as exc:  # noqa: BLE001 — ghi lại lỗi runtime, không crash cả batch
            ok = False
            reasons = [f"EXCEPTION: {type(exc).__name__}: {exc}"]
            actual_state = "ERROR"
            rationale = str(exc)

        if ok:
            passed += 1
        results.append({
            "id": case["id"],
            "class": case["class"],
            "input_preview": case["input"][:70] + ("…" if len(case["input"]) > 70 else ""),
            "expected_state": case["expected_state"],
            "actual_state": actual_state,
            "pass": ok,
            "reasons": reasons,
            "rationale": rationale,
        })
        if verbose:
            status = "PASS" if ok else "FAIL"
            print(f"[{status}] {case['id']} ({case['class']}): expected={case['expected_state']} actual={actual_state}")
            if not ok:
                for r in reasons:
                    print(f"        - {r}")

    total = len(golden["cases"])
    summary = {
        "provider": settings.provider,
        "model": settings.model,
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": round(passed / total * 100, 1) if total else 0.0,
        "results": results,
    }
    if verbose:
        print("─" * 70)
        print(f"Provider: {settings.provider} / {settings.model}")
        print(f"Passed: {passed}/{total} ({summary['pass_rate']}%)")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Chạy golden set qua agent")
    parser.add_argument("--provider", "-p", default="mock")
    parser.add_argument("--model", "-m")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--out", "-o", help="Ghi JSON trực tiếp ra file này (UTF-8, tránh lỗi redirect PowerShell)")
    args = parser.parse_args()

    summary = run(provider=args.provider, model=args.model, verbose=not args.json or bool(args.out))
    if args.out:
        Path(args.out).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nĐã ghi kết quả vào {args.out}")
    elif args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
