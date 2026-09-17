"""StateCheckAgent — lõi quyết định thay `decide()` heuristic trong prototype.

Đúng sơ đồ luồng trong `codebase/prototype/index.html`:
1. Hai cổng chặn deterministic (dán nguyên văn + quá ngắn) — trước khi gọi AI.
2. Điểm gọi quyết định AI — có tool-calling loop: agent gọi `get_excerpt` /
   `list_scope` nếu cần, rồi trả Decision.
3. Ba nhánh đi ra: ĐỦ_CĂN_CỨ / THIẾU_CĂN_CỨ / NGOÀI_PHẠM_VI.

Agent KHÔNG tự chốt "đã hiểu" — chỉ trả Decision, còn việc xác nhận là của
học viên (session.py sẽ handle màn M3→M4).
"""

from __future__ import annotations

import json
import re
from typing import Any

from .config import Settings
from .prompts import SYSTEM_PROMPT, DECISION_SCHEMA
from .providers import Provider, create_provider
from .schema import Decision
from .sources import EXCERPTS
from .tools import TOOL_SCHEMAS, call_tool


class StateCheckAgent:
    """Agent học trò — nhận lời giải thích học viên, quyết định trạng thái
    ĐỦ_CĂN_CỨ / THIẾU_CĂN_CỨ / NGOÀI_PHẠM_VI, có thể gọi tool để grounding."""

    def __init__(self, provider: Provider, settings: Settings):
        self.provider = provider
        self.settings = settings

    @classmethod
    def from_settings(cls, settings: Settings | None = None) -> StateCheckAgent:
        if settings is None:
            from .config import load_settings
            settings = load_settings()
        provider = create_provider(settings)
        return cls(provider, settings)

    def decide(self, student_explanation: str) -> Decision:
        """Điểm gọi quyết định AI (thay `decide()` trong index.html).

        Hai cổng chặn trước (deterministic):
        1. Dán nguyên văn tài liệu?
        2. Quá ngắn (<40 ký tự)?

        Nếu qua hai cổng → gọi LLM với tool-calling loop → Decision.
        """
        text = student_explanation.strip()

        # Cổng 1: dán nguyên văn tài liệu? (hard test spec.md §5 §6)
        verbatim_check = self._check_verbatim_paste(text)
        if verbatim_check:
            return Decision(
                state="THIẾU_CĂN_CỨ",
                confidence="thấp",
                message=(
                    "Đoạn này là chữ trong tài liệu, không phải chữ của bạn. "
                    "Bạn nói lại ý đó bằng lời mình được không?"
                ),
                is_verbatim_paste=True,
                probes=[],
                rationale=f"Dán gần như nguyên văn từ [{verbatim_check}].",
            )

        # Cổng 2: quá ngắn? (lớp lỗi ② mơ hồ — spec.md §5)
        if len(text) < 40:
            return Decision(
                state="THIẾU_CĂN_CỨ",
                confidence="thấp",
                message="Mới chừng này thì mình chưa đủ để hiểu. Bạn viết dài thêm một chút được không?",
                probes=[],
                rationale="Bài quá ngắn (<40 ký tự), chưa đủ dữ kiện để đánh giá.",
            )

        # Qua hai cổng → gọi LLM với tool-calling loop
        return self._call_llm_with_tools(text)

    def _check_verbatim_paste(self, text: str) -> str | None:
        """Tìm xem có đoạn nào dán gần như nguyên văn (≥35 ký tự khớp liên tục)
        từ EXCERPTS không. Trả về mã đoạn nếu phát hiện, None nếu không."""
        normalized = re.sub(r"\s+", " ", text.lower())
        for exc in EXCERPTS:
            src_norm = re.sub(r"\s+", " ", exc.text.lower())
            # Sliding window 35 ký tự
            for i in range(len(src_norm) - 34):
                snippet = src_norm[i:i+35]
                if snippet in normalized:
                    return exc.id
        return None

    def _call_llm_with_tools(self, student_explanation: str) -> Decision:
        """Tool-calling loop: agent có thể gọi `get_excerpt` / `list_scope` để
        grounding trước khi trả Decision. Max `settings.max_tool_hops` vòng."""
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Học viên giải thích:\n\n{student_explanation}"},
        ]

        for hop in range(self.settings.max_tool_hops):
            resp = self.provider.complete(
                messages=messages,
                tools=TOOL_SCHEMAS,
                response_format={"type": "json_schema", "json_schema": {
                    "name": "decision",
                    "strict": True,
                    "schema": DECISION_SCHEMA,
                }},
                temperature=self.settings.temperature,
            )

            # Agent gọi tool?
            if resp["tool_calls"]:
                assistant_tool_calls = [
                    {
                        "id": tc["id"],
                        "type": "function",
                        "function": {
                            "name": tc["name"],
                            "arguments": json.dumps(tc["arguments"], ensure_ascii=False),
                        },
                    }
                    for tc in resp["tool_calls"]
                ]
                messages.append({
                    "role": "assistant",
                    "tool_calls": assistant_tool_calls,
                    "content": None,
                })
                for tc in resp["tool_calls"]:
                    result = call_tool(tc["name"], tc["arguments"])
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc["id"],
                        "content": json.dumps(result, ensure_ascii=False),
                    })
                continue  # lặp lại để agent có thể gọi tool tiếp hoặc trả Decision

            # Agent trả content → parse Decision
            if resp["content"]:
                try:
                    data = json.loads(resp["content"])
                    return Decision.from_dict(data)
                except (json.JSONDecodeError, KeyError) as exc:
                    # LLM trả JSON sai format — fallback THIẾU_CĂN_CỨ
                    return Decision(
                        state="THIẾU_CĂN_CỨ",
                        confidence="thấp",
                        message="Mình chưa theo kịp. Bạn nói lại được không?",
                        probes=[],
                        rationale=f"LLM trả JSON không hợp lệ: {exc}",
                    )

            # Không có tool_calls và không có content → lỗi
            return Decision(
                state="THIẾU_CĂN_CỨ",
                confidence="thấp",
                message="Mình chưa theo kịp. Bạn nói lại được không?",
                probes=[],
                rationale="LLM không trả tool_calls cũng không trả content.",
            )

        # Vượt quá max_tool_hops → agent gọi tool quá nhiều, chưa ra quyết định
        return Decision(
            state="THIẾU_CĂN_CỨ",
            confidence="thấp",
            message="Mình chưa theo kịp. Bạn nói lại được không?",
            probes=[],
            rationale=f"Agent gọi tool vượt quá {self.settings.max_tool_hops} vòng.",
        )
