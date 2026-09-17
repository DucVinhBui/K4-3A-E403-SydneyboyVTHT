"""Test client cho API server — kiểm tra tất cả endpoints mà không cần mở trình duyệt.

Chạy khi API server đang chạy (bật server ở terminal khác):

    python -m eval.api_test
    python -m eval.api_test --base http://127.0.0.1:8080
    python -m eval.api_test --base http://127.0.0.1:8080 --provider openrouter --model openai/gpt-4o-mini

Script này:
  1. GET  /api/health          — kiểm tra server sống
  2. GET  /api/config          — xem provider/model đang dùng
  3. GET  /api/eval/cases      — liệt kê test cases
  4. POST /api/decide           — thử quyết định trên 5 sample
  5. POST /api/eval/run         — chạy toàn bộ golden set qua API
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any

# ensure codebase/ on sys.path (idempotent)
_codebase_root = Path(__file__).resolve().parent.parent
if str(_codebase_root) not in sys.path:
    sys.path.insert(0, str(_codebase_root))

# Windows UTF-8 stdout
if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# ── HTTP client (stdlib only — không dùng requests) ───────────────────────────

def _req(method: str, url: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body else None
    headers = {"Content-Type": "application/json; charset=utf-8"}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {"ok": True, "status": resp.status, "body": json.loads(resp.read().decode("utf-8"))}
    except urllib.error.HTTPError as exc:
        try:
            err_body = json.loads(exc.read().decode("utf-8"))
        except Exception:
            err_body = exc.read().decode("utf-8", errors="replace")
        return {"ok": False, "status": exc.code, "error": err_body}
    except urllib.error.URLError as exc:
        return {"ok": False, "error": f"URL error: {exc.reason}"}
    except TimeoutError:
        return {"ok": False, "error": "Request timed out"}


# ── Tests ───────────────────────────────────────────────────────────────────

def test_health(base: str) -> bool:
    r = _req("GET", f"{base}/api/health")
    if r["ok"]:
        print(f"✅ Health OK: {r['body']}")
        return True
    print(f"❌ Health failed: {r.get('error') or r}")
    return False


def test_config(base: str) -> dict[str, Any] | None:
    r = _req("GET", f"{base}/api/config")
    if r["ok"]:
        cfg = r["body"]
        print(f"✅ Config: provider={cfg['provider']!r}  model={cfg['model']!r}  temp={cfg['temperature']}")
        return cfg
    print(f"❌ Config failed: {r.get('error') or r}")
    return None


def test_decide(base: str, samples_dir: Path) -> int:
    """POST /api/decide trên từng sample file, đếm số thành công."""
    sample_files = sorted(samples_dir.glob("*.txt"))
    if not sample_files:
        print("⚠️  Không có sample files trong eval/samples/")
        return 0

    ok_count = 0
    for sf in sample_files:
        text = sf.read_text(encoding="utf-8").strip()
        # Cắt preview dài
        preview = text[:80] + ("…" if len(text) > 80 else "")
        r = _req("POST", f"{base}/api/decide", {"explanation": text})
        if r["ok"]:
            state = r["body"].get("state", "?")
            conf = r["body"].get("confidence", "?")
            print(f"  ✅ {sf.stem}: state={state}  conf={conf}")
            ok_count += 1
        else:
            print(f"  ❌ {sf.stem}: {r.get('error') or r.get('error', {}).get('error', '?')}")
            print(f"       (input preview: {preview})")
    return ok_count


def test_eval_cases(base: str) -> int:
    r = _req("GET", f"{base}/api/eval/cases")
    if r["ok"]:
        cases = r["body"].get("cases", [])
        print(f"✅ /api/eval/cases: {len(cases)} cases")
        for c in cases:
            print(f"  [{c['id']}] ({c.get('class','')})  expected={c.get('expected_state','?')}")
            print(f"       {c.get('input_preview','')[:70]}")
        return len(cases)
    print(f"❌ /api/eval/cases failed: {r.get('error') or r}")
    return 0


def test_eval_run(base: str, provider: str, model: str | None) -> dict[str, Any] | None:
    body: dict[str, Any] = {"provider": provider}
    if model:
        body["model"] = model
    r = _req("POST", f"{base}/api/eval/run", body)
    if r["ok"]:
        result = r["body"]
        total = result.get("total", 0)
        passed = result.get("passed", 0)
        failed = result.get("failed", 0)
        rate = result.get("pass_rate", 0.0)
        print(f"✅ Eval run: {passed}/{total} passed ({rate}%)")
        for item in result.get("results", []):
            tag = "PASS" if item.get("pass") else "FAIL"
            print(f"  [{tag}] {item['id']} ({item.get('class','')})  "
                  f"expected={item.get('expected_state')}  actual={item.get('actual_state')}")
            if item.get("reasons"):
                for reason in item["reasons"]:
                    print(f"        → {reason}")
        return result
    print(f"❌ /api/eval/run failed: {r.get('error') or r}")
    return None


# ── main ────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Test client cho Agent API server")
    parser.add_argument(
        "--base", "-b",
        default="http://127.0.0.1:8080",
        help="Base URL của API server (default: http://127.0.0.1:8080)",
    )
    parser.add_argument(
        "--provider", "-p",
        default="mock",
        help="Provider cho /api/eval/run (default: mock)",
    )
    parser.add_argument(
        "--model", "-m",
        help="Model cho /api/eval/run (tùy chọn, dùng default của provider nếu bỏ trống)",
    )
    parser.add_argument(
        "--decide-only", "-d",
        action="store_true",
        help="Chỉ chạy /api/decide trên sample files, không chạy eval run",
    )
    parser.add_argument(
        "--skip-health",
        action="store_true",
        help="Bỏ qua health check (khi biết chắc server sống)",
    )
    args = parser.parse_args()

    print("═" * 64)
    print(f"API test client — base: {args.base}")
    print("═" * 64)

    if not args.skip_health:
        print("\n── 1. Health check ──")
        if not test_health(args.base):
            sys.exit(1)

    print("\n── 2. Config ──")
    cfg = test_config(args.base)
    if not cfg:
        sys.exit(1)

    print("\n── 3. Eval cases list ──")
    n_cases = test_eval_cases(args.base)
    print(f"   ({n_cases} cases loaded)")

    print("\n── 4. /api/decide trên sample files ──")
    samples_dir = Path(__file__).resolve().parent / "samples"
    n_ok = test_decide(args.base, samples_dir)
    print(f"   ({n_ok}/{n_cases or 1} thành công)")

    if args.decide_only:
        print("\n✅ decide-only mode: bỏ qua eval run.")
        return

    print(f"\n── 5. /api/eval/run (provider={args.provider}" +
          (f", model={args.model}" if args.model else "") + ") ──")
    result = test_eval_run(args.base, args.provider, args.model)
    if result:
        print(f"\n{'═' * 64}")
        print(f"KẾT QUẢ: {result['passed']}/{result['total']} passed "
              f"({result['pass_rate']}%)  [{result['provider']}/{result['model']}]")
        print("═" * 64)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
