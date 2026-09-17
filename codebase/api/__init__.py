"""api — HTTP server cho agent học trò.

Chạy server:
    python -m api.server
    python -m api.server --port 8765
    python -m api.server --host 0.0.0.0 --port 8080

Endpoints:
    GET  /                  → serve prototype/index.html
    GET  /api/config        → provider, model, temperature
    POST /api/decide        → body: {"explanation": "..."} → Decision JSON
    GET  /api/eval/cases   → list test cases
    POST /api/eval/run     → body: {"provider": "mock"} → eval results
    GET  /api/health       → health check
"""

from .server import run, main

__all__ = ["run", "main"]
