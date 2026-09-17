"""CLI để test agent học trò — chạy nhanh một lời giải thích, xem agent quyết định gì.

Usage:
    python -m agent.cli "Mô hình không tra cứu, chỉ dự đoán token tiếp theo..."
    python -m agent.cli --file eval/samples/001-day-du.txt
    python -m agent.cli --provider openai --model gpt-4o-mini "LLM bịa vì..."

Output: in ra state, confidence, message, probes (nếu có), rationale.
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

# Cho phép chạy cả `python cli.py` (script) lẫn `python -m agent.cli` (module).
# Khi chạy trực tiếp, __package__ rỗng → relative import sẽ crash. Ta thử relative
# trước (chuẩn khi dùng `python -m`), fallback sang absolute.
try:
    from .config import Settings, load_settings
    from .core import StateCheckAgent
except ImportError:
    # Đảm bảo thư mục cha (codebase/) có trong sys.path để import tuyệt đối.
    _cli_dir = Path(__file__).resolve().parent
    _codebase_root = _cli_dir.parent
    if str(_codebase_root) not in sys.path:
        sys.path.insert(0, str(_codebase_root))
    from agent.config import Settings, load_settings  # type: ignore[no-redef]
    from agent.core import StateCheckAgent  # type: ignore[no-redef]

# Windows console mặc định dùng cp1252 — không encode được ┌─│ hay tiếng Việt
# có dấu. Ép stdout/stderr sang UTF-8 để CLI chạy được cả trên PowerShell.
if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding is None or sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def main() -> None:
    parser = argparse.ArgumentParser(description="Test agent học trò — CLI đơn giản")
    parser.add_argument("explanation", nargs="?", help="Lời giải thích của học viên (trực tiếp)")
    parser.add_argument("--file", "-f", help="Đọc lời giải thích từ file")
    parser.add_argument("--provider", "-p", help="Provider: mock, openai, anthropic")
    parser.add_argument("--model", "-m", help="Model (tùy chọn)")
    parser.add_argument("--temperature", "-t", type=float, help="Temperature 0.0–1.0")
    parser.add_argument("--json", action="store_true", help="In ra JSON thay vì text dễ đọc")
    args = parser.parse_args()

    # Lấy lời giải thích từ arg hoặc file
    if args.file:
        explanation = Path(args.file).read_text(encoding="utf-8").strip()
    elif args.explanation:
        explanation = args.explanation.strip()
    else:
        parser.print_help()
        sys.exit(1)

    # Load settings (ưu tiên arg CLI > biến môi trường > default)
    settings = load_settings()
    if args.provider:
        settings.provider = args.provider.lower()
    if args.model:
        settings.model = args.model
    if args.temperature is not None:
        settings.temperature = args.temperature

    # Chạy agent
    agent = StateCheckAgent.from_settings(settings)
    decision = agent.decide(explanation)

    # In kết quả
    if args.json:
        print(json.dumps(decision.to_dict(), ensure_ascii=False, indent=2))
    else:
        _print_human_readable(decision, explanation, settings)


def _print_human_readable(decision, explanation: str, settings: Settings) -> None:
    print("┌─────────────────────────────────────────────────────────────────────")
    print(f"│ Provider: {settings.provider} / {settings.model}")
    print(f"│ Lời giải thích: {explanation[:80]}{'...' if len(explanation) > 80 else ''}")
    print("├─────────────────────────────────────────────────────────────────────")
    print(f"│ STATE:      {decision.state}")
    print(f"│ CONFIDENCE: {decision.confidence}")
    if decision.matched_criteria:
        print(f"│ Matched:    {', '.join(decision.matched_criteria)}")
    if decision.missing_criteria:
        print(f"│ Missing:    {', '.join(decision.missing_criteria)}")
    if decision.out_of_scope_terms:
        print(f"│ Out:        {', '.join(decision.out_of_scope_terms)}")
    if decision.is_verbatim_paste:
        print("│ Verbatim:   YES")
    print("├─────────────────────────────────────────────────────────────────────")
    print(f"│ MESSAGE:\n│   {decision.message}")
    if decision.probes:
        print("│ PROBES:")
        for i, p in enumerate(decision.probes, 1):
            print(f"│   {i}. [{p.source_id}] {p.text}")
    print("├─────────────────────────────────────────────────────────────────────")
    print(f"│ RATIONALE: {decision.rationale}")
    print("└─────────────────────────────────────────────────────────────────────")


if __name__ == "__main__":
    main()
