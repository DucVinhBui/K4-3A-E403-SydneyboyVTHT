"""Eval runner — chạy agent trên bộ test mẫu và so sánh với expected state.

Bộ test tối thiểu phải có đủ 5 kịch bản trong spec.md §5 "Beatable baseline":
1. Đủ cả 3 tiêu chí → ĐỦ_CĂN_CỨ
2. Thiếu 1-2 tiêu chí → THIẾU_CĂN_CỨ
3. Nói sang ngoài phạm vi → NGOÀI_PHẠM_VI
4. Quá ngắn (<40 ký tự) → THIẾU_CĂN_CỨ
5. Dán nguyên văn tài liệu → THIẾU_CĂN_CỨ + is_verbatim_paste=True

Eval này test cho CP2/CP3 — không phải bài khảo sát thật lúc phát cho lớp.
Chỉ để kiểm tra agent logic đúng, chứ không phải validate giả thuyết.
"""

from __future__ import annotations

import io
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agent.config import load_settings
from agent.core import StateCheckAgent

# Windows console mặc định dùng cp1252 — không encode được ✅❌ hay tiếng Việt
# có dấu (giống lý do trong agent/cli.py).
if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding is None or sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


@dataclass
class TestCase:
    id: str
    input_file: Path
    expected_state: str
    expected_verbatim: bool = False
    note: str = ""


TEST_CASES: list[TestCase] = [
    TestCase(
        "001-day-du",
        Path("eval/samples/001-day-du.txt"),
        "ĐỦ_CĂN_CỨ",
        note="Đủ cả 3 tiêu chí, diễn đạt bằng lời của mình",
    ),
    TestCase(
        "002-thieu-2-tieu-chi",
        Path("eval/samples/002-thieu-2-tieu-chi.txt"),
        "THIẾU_CĂN_CỨ",
        note="Chỉ có c1, thiếu c2 và c3",
    ),
    TestCase(
        "003-ngoai-pham-vi",
        Path("eval/samples/003-ngoai-pham-vi.txt"),
        "NGOÀI_PHẠM_VI",
        note="Nói về fine-tune, RLHF — ngoài 4 đoạn [T06-138]–[T06-149]",
    ),
    TestCase(
        "004-qua-ngan",
        Path("eval/samples/004-qua-ngan.txt"),
        "THIẾU_CĂN_CỨ",
        note="Chỉ 2 ký tự, không đủ dữ kiện đánh giá",
    ),
    TestCase(
        "005-dan-nguyen-van",
        Path("eval/samples/005-dan-nguyen-van.txt"),
        "THIẾU_CĂN_CỨ",
        expected_verbatim=True,
        note="Dán gần như nguyên văn từ [T06-138]",
    ),
]


def run_eval(provider: str = "mock", model: str | None = None, verbose: bool = True) -> dict[str, Any]:
    """Chạy tất cả test case, trả về kết quả tổng hợp.

    Returns:
        {
            "provider": str,
            "model": str,
            "total": int,
            "passed": int,
            "failed": int,
            "results": [{"id": str, "pass": bool, "expected": str, "actual": str, ...}]
        }
    """
    settings = load_settings()
    settings.provider = provider
    if model:
        settings.model = model

    agent = StateCheckAgent.from_settings(settings)
    base = Path(__file__).resolve().parent.parent

    results = []
    passed = 0
    failed = 0

    for tc in TEST_CASES:
        input_path = base / tc.input_file
        if not input_path.exists():
            if verbose:
                print(f"⚠️  {tc.id}: file không tồn tại {input_path}")
            results.append({
                "id": tc.id,
                "pass": False,
                "expected": tc.expected_state,
                "actual": "FILE_NOT_FOUND",
                "note": tc.note,
            })
            failed += 1
            continue

        text = input_path.read_text(encoding="utf-8").strip()
        decision = agent.decide(text)

        # So sánh state
        state_match = decision.state == tc.expected_state
        verbatim_match = decision.is_verbatim_paste == tc.expected_verbatim
        test_pass = state_match and verbatim_match

        if test_pass:
            passed += 1
            status = "✅"
        else:
            failed += 1
            status = "❌"

        if verbose:
            print(f"{status} {tc.id}: expected={tc.expected_state}, actual={decision.state}")
            if not verbatim_match:
                print(f"   (verbatim mismatch: expected={tc.expected_verbatim}, actual={decision.is_verbatim_paste})")
            if not test_pass:
                print(f"   Rationale: {decision.rationale}")

        results.append({
            "id": tc.id,
            "pass": test_pass,
            "expected": tc.expected_state,
            "actual": decision.state,
            "confidence": decision.confidence,
            "verbatim": decision.is_verbatim_paste,
            "note": tc.note,
            "rationale": decision.rationale,
        })

    if verbose:
        print("─" * 70)
        print(f"Provider: {settings.provider} / {settings.model}")
        print(f"Passed: {passed}/{len(TEST_CASES)} | Failed: {failed}/{len(TEST_CASES)}")

    return {
        "provider": settings.provider,
        "model": settings.model,
        "total": len(TEST_CASES),
        "passed": passed,
        "failed": failed,
        "results": results,
    }


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Chạy eval cho agent học trò")
    parser.add_argument("--provider", "-p", default="mock", help="Provider: mock, openai, anthropic")
    parser.add_argument("--model", "-m", help="Model (tùy chọn)")
    parser.add_argument("--json", action="store_true", help="In ra JSON thay vì text")
    args = parser.parse_args()

    result = run_eval(provider=args.provider, model=args.model, verbose=not args.json)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
