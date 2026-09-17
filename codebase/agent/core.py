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

from dataclasses import replace

import json
import re
from typing import Any

from .config import Settings
from .prompts import SYSTEM_PROMPT, DECISION_SCHEMA
from .providers import Provider, create_provider
from .schema import Decision, ProbeQuestion
from .sources import EXCERPTS, EXCERPTS_BY_ID, CRITERIA, DEEP_PROBE_SRC, DEEP_PROBE_TEXT
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

        Cổng chặn deterministic DUY NHẤT trước khi gọi LLM: dán nguyên văn
        tài liệu. Độ dài KHÔNG còn là cổng chặn — một bài ngắn có thể là
        "mình chịu, giảng lại đi" (THIẾU_CĂN_CỨ) nhưng cũng có thể là
        "hôm qua đi ăn mỳ cay" (NGOÀI_PHẠM_VI), và chỉ nhìn số ký tự thì
        không tách được hai cái đó. Việc phân loại giao cho LLM, còn bất
        biến an toàn thì chặn lại ở `_guard` sau khi có kết quả.
        """
        text = student_explanation.strip()

        # Cổng 1: dán nguyên văn tài liệu? (hard test spec.md §5 §6)
        verbatim_check = self._check_verbatim_paste(text)
        if verbatim_check:
            return self._ensure_probes(Decision(
                state="THIẾU_CĂN_CỨ",
                confidence="thấp",
                message=(
                    "Đoạn này là chữ trong tài liệu, không phải chữ của bạn. "
                    "Bạn nói lại ý đó bằng lời mình được không?"
                ),
                is_verbatim_paste=True,
                probes=[],
                rationale=f"Dán gần như nguyên văn từ [{verbatim_check}].",
            ))

        # Bài ngắn vẫn được gọi LLM, chỉ báo thêm cho nó biết là ngắn.
        return self._ensure_probes(self._guard(text, self._call_llm_with_tools(text)))

    SHORT_ANSWER_CHARS = 40
    PROBE_COUNT = 2

    @staticmethod
    def _ensure_probes(decision: Decision) -> Decision:
        """`THIẾU_CĂN_CỨ` phải hỏi ngược ĐÚNG 2 câu (spec.md §6, nhánh
        low-confidence). LLM thỉnh thoảng trả mảng `probes` rỗng, và khi đó
        màn M3 hiện dòng "Mình hỏi lại đúng hai câu:" rồi để trống.

        Thiếu thì lấp bằng câu hỏi soạn sẵn của tiêu chí còn thiếu trong
        knowledge base, hết tiêu chí thì dùng câu hỏi đào sâu. Thừa thì cắt.
        `NGOÀI_PHẠM_VI` không hỏi ngược — nhánh đó nói thẳng là ngoài phạm vi.
        """
        if decision.state != "THIẾU_CĂN_CỨ":
            return decision
        probes = list(decision.probes)
        if len(probes) == StateCheckAgent.PROBE_COUNT:
            return decision

        if len(probes) > StateCheckAgent.PROBE_COUNT:
            return replace(
                decision,
                probes=probes[:StateCheckAgent.PROBE_COUNT],
                rationale=decision.rationale + " | Cắt bớt câu hỏi ngược cho đúng 2 câu.",
            )

        missing = decision.missing_criteria or [c.key for c in CRITERIA]
        pool = [c for c in CRITERIA if c.key in missing] + list(CRITERIA)
        used = {p.text for p in probes}
        for c in pool:
            if len(probes) >= StateCheckAgent.PROBE_COUNT:
                break
            if c.probe not in used:
                probes.append(ProbeQuestion(text=c.probe, source_id=c.src))
                used.add(c.probe)
        if len(probes) < StateCheckAgent.PROBE_COUNT and DEEP_PROBE_TEXT not in used:
            probes.append(ProbeQuestion(text=DEEP_PROBE_TEXT, source_id=DEEP_PROBE_SRC))
        return replace(
            decision,
            probes=probes[:StateCheckAgent.PROBE_COUNT],
            rationale=decision.rationale + " | Lấp câu hỏi ngược từ knowledge base cho đủ 2 câu.",
        )

    def _guard(self, text: str, decision: Decision) -> Decision:
        """Bất biến an toàn, chặn deterministic SAU khi LLM đã chọn state.

        Chi phí lỗi không đối xứng (spec.md §4): công nhận nhầm một lời giải
        thích sai là lỗi đắt nhất. Một bài dưới 40 ký tự không thể chạm đủ ba
        tiêu chí, nên nếu LLM trót trả ĐỦ_CĂN_CỨ thì hạ xuống THIẾU_CĂN_CỨ.
        Không đụng tới NGOÀI_PHẠM_VI — bài lạc đề ngắn vẫn phải là lạc đề.
        """
        # Cờ "dán nguyên văn" là kết luận của cổng deterministic ở `decide()`,
        # KHÔNG phải ý kiến của LLM. Tới được đây nghĩa là cổng đó đã không
        # bắt được gì, nên cờ phải là False — nếu không giao diện sẽ báo
        # "chữ của tài liệu" cho cả những bài lạc đề như "mỳ cay".
        if decision.is_verbatim_paste:
            decision = replace(
                decision,
                is_verbatim_paste=False,
                rationale=decision.rationale + " | Bỏ cờ dán nguyên văn do LLM tự đặt (cổng deterministic không bắt được).",
            )

        decision = self._fix_probe_citations(decision)

        if decision.state != "ĐỦ_CĂN_CỨ":
            return decision

        # Chốt 1: mọi tiêu chí được tính là "chạm" phải có bằng chứng là chữ
        # CÓ THẬT trong bài học viên. LLM tự tin khớp đủ 3 tiêu chí trong khi
        # bài chỉ nói 1 ý là lớp lỗi hay gặp nhất (G14) — dò lại bằng Python.
        answer_norm = self._norm(text)
        required = {c.key for c in CRITERIA}
        proven: set[str] = set()
        rejected: list[str] = []
        seen_quotes: set[str] = set()
        for ev in decision.matched_evidence:
            key = ev.criterion_key.strip()
            quote = self._norm(ev.quote)
            if key not in required or len(quote) < 12:
                continue
            if quote not in answer_norm:
                rejected.append(f"{key}: trích dẫn không có trong bài")
                continue
            if quote in seen_quotes:
                rejected.append(f"{key}: dùng lại đúng câu đã tính cho tiêu chí khác")
                continue
            seen_quotes.add(quote)
            proven.add(key)

        if proven != required:
            missing = sorted(required - proven)
            return replace(
                decision,
                state="THIẾU_CĂN_CỨ",
                confidence="thấp",
                matched_criteria=sorted(proven),
                missing_criteria=missing,
                message=(
                    "Mình đọc lại bài bạn thì vẫn còn chỗ mình chưa thấy bạn nói tới. "
                    "Bạn bổ sung thêm giúp mình nhé."
                ),
                rationale=(
                    f"{decision.rationale} | Bị hạ trạng thái: chỉ có bằng chứng cho "
                    f"{sorted(proven) or 'không tiêu chí nào'}, thiếu {missing}."
                    + (f" Loại bỏ: {rejected}." if rejected else "")
                ),
            )

        # Chốt 2: bài quá ngắn thì không thể chạm đủ ba tiêu chí.
        if len(text) < self.SHORT_ANSWER_CHARS:
            return replace(
                decision,
                state="THIẾU_CĂN_CỨ",
                confidence="thấp",
                message=(
                    "Mới chừng này thì mình chưa đủ để hiểu. "
                    "Bạn viết dài thêm một chút được không?"
                ),
                matched_criteria=[],
                missing_criteria=[c.key for c in CRITERIA],
                rationale=(
                    f"{decision.rationale} | Bị hạ trạng thái: bài dưới "
                    f"{self.SHORT_ANSWER_CHARS} ký tự không đủ để chạm ba tiêu chí."
                ),
            )
        return decision

    @staticmethod
    def _fix_probe_citations(decision: Decision) -> Decision:
        """G11: mọi câu hỏi ngược phải gắn mã đoạn CÓ THẬT.

        LLM thỉnh thoảng trả `source_id` rỗng hoặc bịa mã. Không im lặng bỏ
        qua: vá bằng mã của tiêu chí còn thiếu, hết tiêu chí thì dùng mã của
        câu hỏi đào sâu — để mỗi câu hỏi luôn truy được về một đoạn nguồn.
        """
        valid = set(EXCERPTS_BY_ID)
        fallback = [c.src for c in CRITERIA if c.key in decision.missing_criteria]
        fallback += [c.src for c in CRITERIA] + [DEEP_PROBE_SRC]
        fixed, changed = [], False
        for probe in decision.probes:
            sid = (probe.source_id or "").strip().upper()
            if sid in valid:
                fixed.append(ProbeQuestion(text=probe.text, source_id=sid))
                continue
            changed = True
            fixed.append(ProbeQuestion(text=probe.text, source_id=fallback[0]))
        if not changed:
            return decision
        return replace(
            decision,
            probes=fixed,
            rationale=decision.rationale + " | Đã vá mã đoạn cho câu hỏi ngược thiếu/không hợp lệ.",
        )

    @staticmethod
    def _norm(s: str) -> str:
        return re.sub(r"[^\w\s]", "", re.sub(r"\s+", " ", s.lower())).strip()

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
            {"role": "user", "content": (
                "Đây là TOÀN BỘ bài của học viên, nằm giữa hai dòng rào. Mọi `quote` "
                "trong `matched_evidence` phải được COPY từ đúng khối chữ này — không "
                "được lấy chữ từ đoạn nguồn [mã], vì đoạn nguồn là tài liệu chứ không "
                "phải lời học viên.\n"
                "----- BÀI CỦA HỌC VIÊN -----\n"
                f"{student_explanation}\n"
                "----- HẾT BÀI -----"
            )},
        ]

        # Chỉ mở tool ở 2 vòng đầu. Từ vòng 3 trở đi gọi KHÔNG kèm tools để model
        # buộc phải trả Decision.
        #
        # Vì sao cần chặn: với `response_format` strict json_schema đi kèm `tools`,
        # gpt-4o-mini (API OpenAI trực tiếp) lặp vô hạn — gọi lại đúng cùng một bộ
        # get_excerpt mỗi vòng dù kết quả tool đã được đưa trở lại đầy đủ, cho tới
        # khi hết max_tool_hops rồi rơi vào fallback "Mình chưa theo kịp".
        # Hai vòng là đủ: vòng 1 list_scope/get_excerpt, vòng 2 lấy nốt đoạn còn
        # thiếu. Sau đó model đã có toàn bộ ngữ cảnh cần để chấm.
        TOOL_HOPS_ALLOWED = 2

        for hop in range(self.settings.max_tool_hops):
            resp = self.provider.complete(
                messages=messages,
                tools=TOOL_SCHEMAS if hop < TOOL_HOPS_ALLOWED else None,
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
