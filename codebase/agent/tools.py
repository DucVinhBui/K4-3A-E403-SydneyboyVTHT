"""Tool-calling: agent tự lấy đoạn nguồn thay vì bịa (grounding thật, không
phải nhét cả 4 đoạn vào prompt và tin LLM tự nhớ đúng).

Hai tool cho LLM gọi:
- `list_scope()`      — liệt kê mã + tóm tắt 4 đoạn đang trong phạm vi
- `get_excerpt(id)`    — lấy nguyên văn một đoạn theo mã [Txx-NNN]

Việc bắt agent phải *gọi tool* để trích dẫn, thay vì cho sẵn full text trong
system prompt, là để bài test/eval phát hiện được lúc agent bịa mã nguồn
không tồn tại (lớp lỗi ① ở spec.md §5) — `get_excerpt` với id sai trả lỗi rõ
ràng, không trả về text ngẫu nhiên.
"""

from __future__ import annotations

from typing import Any, Callable

from .sources import EXCERPTS, EXCERPTS_BY_ID, CRITERIA, CONCEPT, SCOPE_RANGE

# ── Định nghĩa tool theo chuẩn OpenAI function-calling (Anthropic map lại ở providers.py) ──

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "list_scope",
            "description": (
                "Liệt kê mã và tóm tắt tất cả đoạn nguồn đang trong phạm vi đối chiếu "
                f"({SCOPE_RANGE}) cho khái niệm '{CONCEPT}'. Gọi tool này trước khi kết luận "
                "một ý của học viên là ngoài phạm vi."
            ),
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_excerpt",
            "description": (
                f"Lấy nguyên văn một đoạn nguồn theo mã, ví dụ '{EXCERPTS[0].id}'. Dùng để trích dẫn "
                "đúng chữ khi hỏi ngược hoặc khi giải thích vì sao một ý nằm ngoài phạm vi. "
                "Không tự bịa nội dung đoạn — luôn gọi tool này trước khi dẫn mã."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "excerpt_id": {
                        "type": "string",
                        "description": f"Mã đoạn, ví dụ '{EXCERPTS[0].id}' hoặc '{EXCERPTS[1].id}'.",
                    }
                },
                "required": ["excerpt_id"],
            },
        },
    },
]


def _tool_list_scope(**_: Any) -> dict[str, Any]:
    return {
        "concept": CONCEPT,
        "scope_range": SCOPE_RANGE,
        "excerpts": [{"id": e.id, "summary": e.text[:80] + ("…" if len(e.text) > 80 else "")} for e in EXCERPTS],
        "criteria": [{"key": c.key, "label": c.label, "src": c.src} for c in CRITERIA],
    }


def _tool_get_excerpt(excerpt_id: str = "", **_: Any) -> dict[str, Any]:
    key = (excerpt_id or "").strip().upper()
    excerpt = EXCERPTS_BY_ID.get(key)
    if excerpt is None:
        return {
            "error": f"Không có đoạn mã '{excerpt_id}' trong phạm vi {SCOPE_RANGE}.",
            "valid_ids": sorted(EXCERPTS_BY_ID.keys()),
        }
    return {"id": excerpt.id, "text": excerpt.text}


TOOL_IMPLS: dict[str, Callable[..., dict[str, Any]]] = {
    "list_scope": _tool_list_scope,
    "get_excerpt": _tool_get_excerpt,
}


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    impl = TOOL_IMPLS.get(name)
    if impl is None:
        return {"error": f"Không có tool tên '{name}'."}
    try:
        return impl(**arguments)
    except TypeError as exc:
        return {"error": f"Sai tham số gọi tool '{name}': {exc}"}
