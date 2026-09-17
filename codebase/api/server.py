"""API server cho agent học trò — dùng stdlib http.server, không cần thêm dep.

Chạy:
    python -m api.server
    python -m api.server --port 8765
    python -m api.server --host 0.0.0.0

Endpoints:
    GET  /                    → serve prototype/index.html
    GET  /api/config          → {"provider", "model", "temperature"}
    POST /api/decide           → {"explanation": "..."} → Decision JSON
    GET  /api/eval/cases      → danh sách test cases từ golden_set.json
    POST /api/eval/run         → {"provider", "model"} → eval results JSON
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

# ensure codebase/ on sys.path (idempotent — cần thiết khi chạy python -m api.server
# từ thư mục con, hoặc khi Python không tự đặt nó vào sys.path)
_codebase_root = Path(__file__).resolve().parent.parent  # .../codebase
if str(_codebase_root) not in sys.path:
    sys.path.insert(0, str(_codebase_root))

from agent.config import load_settings
from agent.core import StateCheckAgent


# ── Windows UTF-8 stdout ──────────────────────────────────────────────────────
if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding is None or sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# ── Helpers ──────────────────────────────────────────────────────────────────

def _read_json_body(handler: BaseHTTPRequestHandler) -> dict[str, Any]:
    """Đọc body JSON từ request, trả về dict."""
    content_length = int(handler.headers.get("Content-Length", 0))
    raw = handler.rfile.read(content_length) if content_length else b""
    return json.loads(raw.decode("utf-8"))


def _send_json(handler: BaseHTTPRequestHandler, status: int, data: Any) -> None:
    """Gửi response JSON với CORS headers phù hợp."""
    body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.end_headers()
    handler.wfile.write(body)


def _send_html(handler: BaseHTTPRequestHandler, status: int, html: bytes) -> None:
    """Gửi HTML dạng chunked transfer để tránh Chrome hủy kết nối (WinError 10053)
    khi user navigate đi trước khi nhận đủ file ~50KB. Chunked cho phép server
    bắt được BrokenPipeError sớm thay vì dump cả file rồi mới biết client đã đi."""
    handler.send_response(status)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Transfer-Encoding", "chunked")
    handler.end_headers()
    CHUNK = 8192
    try:
        for i in range(0, len(html), CHUNK):
            chunk = html[i:i + CHUNK]
            handler.wfile.write(f"{len(chunk):x}\r\n".encode("ascii"))
            handler.wfile.write(chunk)
            handler.wfile.write(b"\r\n")
            handler.wfile.flush()
        handler.wfile.write(b"0\r\n\r\n")
    except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError):
        # Client đã đi (Chrome reload, navigate, đóng tab) — không sao, bỏ qua.
        pass


def _send_text(handler: BaseHTTPRequestHandler, status: int, text: str, content_type: str = "text/plain") -> None:
    body = text.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", f"{content_type}; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


# ── Agent singleton (reuse cho tất cả request) ─────────────────────────────

_agent: StateCheckAgent | None = None
_settings_cache: dict[str, Any] = {}


def _get_agent() -> StateCheckAgent:
    global _agent
    if _agent is None:
        settings = load_settings()
        _agent = StateCheckAgent.from_settings(settings)
    return _agent


def _get_config() -> dict[str, Any]:
    global _settings_cache
    if not _settings_cache:
        s = load_settings()
        _settings_cache = {
            "provider": s.provider,
            "model": s.model,
            "temperature": s.temperature,
            "max_tool_hops": s.max_tool_hops,
        }
    return _settings_cache


# ── eval helpers ─────────────────────────────────────────────────────────────

def _load_golden_cases() -> list[dict[str, Any]]:
    path = Path(__file__).resolve().parent.parent / "eval" / "golden_set.json"
    return json.loads(path.read_text(encoding="utf-8")).get("cases", [])


def _run_golden_eval(provider: str, model: str | None) -> dict[str, Any]:
    """Chạy golden set, trả kết quả JSON (dùng lại logic từ eval/run_golden.py)."""
    from agent.sources import EXCERPTS_BY_ID

    settings = load_settings()
    settings.provider = provider
    if model:
        settings.model = model

    agent = StateCheckAgent.from_settings(settings)
    cases = _load_golden_cases()
    results = []
    passed = 0

    for case in cases:
        try:
            decision = agent.decide(case["input"])
        except Exception as exc:  # noqa: BLE001
            results.append({
                "id": case["id"], "class": case.get("class", ""),
                "input_preview": case["input"][:70] + ("…" if len(case["input"]) > 70 else ""),
                "expected_state": case["expected_state"],
                "actual_state": "ERROR",
                "pass": False,
                "reasons": [f"EXCEPTION: {type(exc).__name__}: {exc}"],
                "rationale": str(exc),
            })
            continue

        reasons = []
        if decision.state != case["expected_state"]:
            reasons.append(f"state sai: expected={case['expected_state']}, actual={decision.state}")
        if case.get("expected_verbatim", False) and not decision.is_verbatim_paste:
            reasons.append("expected_verbatim=True nhưng decision.is_verbatim_paste=False")
        bogus_ids = [p.source_id for p in decision.probes if p.source_id not in EXCERPTS_BY_ID]
        if bogus_ids:
            reasons.append(f"agent bịa mã đoạn không tồn tại: {bogus_ids}")

        ok = len(reasons) == 0
        if ok:
            passed += 1
        results.append({
            "id": case["id"],
            "class": case.get("class", ""),
            "input_preview": case["input"][:70] + ("…" if len(case["input"]) > 70 else ""),
            "expected_state": case["expected_state"],
            "actual_state": decision.state,
            "pass": ok,
            "reasons": reasons,
            "rationale": decision.rationale,
            "confidence": decision.confidence,
        })

    total = len(cases)
    return {
        "provider": settings.provider,
        "model": settings.model,
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": round(passed / total * 100, 1) if total else 0.0,
        "results": results,
    }


# ── Request handler ─────────────────────────────────────────────────────────

_PROTOTYPE_PATH = Path(__file__).resolve().parent.parent / "prototype" / "index.html"
_FLOW_PATH = _PROTOTYPE_PATH  # SVG flow nằm trong cùng file, lazy-extract bằng regex khi serve


def _extract_flow_svg() -> str:
    """Trích SVG sơ đồ luồng từ prototype/index.html — lazy-load qua API."""
    if not _FLOW_PATH.exists():
        return ""
    html = _FLOW_PATH.read_text(encoding="utf-8")
    # Tìm <svg viewBox="0 0 920 1110" ...>...</svg> — viewBox có thể xuống dòng.
    import re
    m = re.search(r'(<svg[^>]*?viewBox="0 0 920 1110".*?</svg>)', html, re.DOTALL)
    return m.group(1) if m else ""


class AgentHandler(BaseHTTPRequestHandler):
    """HTTP handler — dispatch theo path, trả JSON hoặc HTML."""

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def handle_one_request(self) -> None:
        try:
            super().handle_one_request()
        except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError):
            # Chrome/curl đóng kết nối giữa chừng — im lặng.
            self.close_connection = True
        except Exception as exc:
            # Log lỗi thật nhưng không làm chết server
            sys.stderr.write(f"UNHANDLED: {type(exc).__name__}: {exc}\n")
            self.close_connection = True

    # Alias cho Python 3.13+: http.server đổi tên phương thức này qua handle()
    # nhưng BaseHTTPRequestHandler vẫn gọi handle_one_request. Để an toàn:
    handle = handle_one_request

    def do_GET(self) -> None:
        path = self.path.split("?")[0]

        if path == "/" or path == "/index.html":
            if _PROTOTYPE_PATH.exists():
                html = _PROTOTYPE_PATH.read_bytes()
                try:
                    _send_html(self, 200, html)
                except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError):
                    # Client đóng kết nối giữa chừng (Chrome reload/navigate).
                    pass
            else:
                _send_text(self, 404, f"prototype/index.html not found at {_PROTOTYPE_PATH}")
            return

        if path == "/api/config":
            _send_json(self, 200, _get_config())
            return

        if path == "/api/eval/cases":
            cases = _load_golden_cases()
            # Strip full input, chỉ giữ preview để list không quá nặng
            for c in cases:
                c["input_preview"] = c["input"][:120] + ("…" if len(c["input"]) > 120 else "")
                del c["input"]
            _send_json(self, 200, {"cases": cases})
            return

        if path == "/api/health":
            _send_json(self, 200, {"status": "ok", "config": _get_config()})
            return

        if path == "/api/flow":
            _send_json(self, 200, {"svg": _extract_flow_svg()})
            return

        # 404 cho mọi GET khác
        _send_json(self, 404, {"error": f"GET {path!r} not found"})

    def do_POST(self) -> None:
        path = self.path.split("?")[0]

        if path == "/api/decide":
            try:
                body = _read_json_body(self)
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                _send_json(self, 400, {"error": f"Invalid JSON body: {exc}"})
                return

            explanation = body.get("explanation", "").strip()
            if not explanation:
                _send_json(self, 400, {"error": "Field 'explanation' is required and non-empty."})
                return

            try:
                decision = _get_agent().decide(explanation)
                _send_json(self, 200, decision.to_dict())
            except Exception as exc:  # noqa: BLE001
                _send_json(self, 500, {"error": f"Agent error: {type(exc).__name__}: {exc}"})
            return

        if path == "/api/eval/run":
            try:
                body = _read_json_body(self)
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                _send_json(self, 400, {"error": f"Invalid JSON body: {exc}"})
                return

            provider = body.get("provider", "mock")
            model = body.get("model") or None
            try:
                result = _run_golden_eval(provider, model)
                _send_json(self, 200, result)
            except Exception as exc:  # noqa: BLE001
                _send_json(self, 500, {"error": f"Eval error: {type(exc).__name__}: {exc}"})
            return

        _send_json(self, 404, {"error": f"POST {path!r} not found"})

    def log_message(self, format: str, *args: Any) -> None:
        # Giữ format mặc định nhưng ghi qua stderr để không ảnh hưởng stdout
        sys.stderr.write(f"{self.address_string()} - [{self.log_date_time_string()}] {format % args}\n")


# ── Entry point ──────────────────────────────────────────────────────────────

def run(host: str = "127.0.0.1", port: int = 8080) -> None:
    server = HTTPServer((host, port), AgentHandler)
    print(f"🌐 Agent server đang chạy tại http://{host}:{port}/")
    print(f"   Giao diện:       http://{host}:{port}/")
    print(f"   API config:      GET  /api/config")
    print(f"   Chat thật:       POST /api/decide  (body: {{'explanation': '...'}})")
    print(f"   Eval cases:      GET  /api/eval/cases")
    print(f"   Chạy eval:      POST /api/eval/run  (body: {{'provider': 'mock', 'model': null}})")
    print(f"   Health check:    GET  /api/health")
    print(f"   Dừng:           Ctrl+C")
    print()
    print(f"   Provider hiện tại: {_get_config()['provider']} / {_get_config()['model']}")
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⛔ Đã dừng server.")
        server.shutdown()


def main() -> None:
    parser = argparse.ArgumentParser(description="Chạy API server cho agent học trò")
    parser.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Port (default: 8080)")
    args = parser.parse_args()
    run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
