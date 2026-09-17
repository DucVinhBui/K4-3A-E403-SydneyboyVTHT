"""Output schema: lớp Python đại diện quyết định của agent (giống hàm `decide()`
trong JS trả về, nhưng chạy LLM thật thay vì heuristic đếm từ khoá).

Structured output — bắt LLM trả về JSON đúng schema này, dùng cho eval và
state machine M1→M4 (không phải parse free-text).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


StateType = Literal["ĐỦ_CĂN_CỨ", "THIẾU_CĂN_CỨ", "NGOÀI_PHẠM_VI"]
ConfidenceType = Literal["cao", "trung bình", "thấp", "không đánh giá"]


@dataclass
class ProbeQuestion:
    """Một câu hỏi ngược — PHẢI gắn `source_id` (spec.md §4b G11: giải thích vì sao)."""
    text: str
    source_id: str


@dataclass
class Evidence:
    """Câu/cụm từ CỦA HỌC VIÊN mà agent cho là chạm một tiêu chí.

    Có trường này thì việc "chạm tiêu chí" mới kiểm được bằng Python: nếu
    `quote` không thật sự nằm trong bài của học viên thì tiêu chí đó không
    được tính (spec.md §4 — chi phí lỗi không đối xứng).
    """
    criterion_key: str
    quote: str


@dataclass
class Decision:
    """Quyết định của agent, trả về sau khi gọi tool (nếu cần) rồi chọn state."""
    state: StateType
    confidence: ConfidenceType
    matched_criteria: list[str] = field(default_factory=list)
    matched_evidence: list[Evidence] = field(default_factory=list)
    missing_criteria: list[str] = field(default_factory=list)
    out_of_scope_terms: list[str] = field(default_factory=list)
    is_verbatim_paste: bool = False
    message: str = ""
    probes: list[ProbeQuestion] = field(default_factory=list)
    rationale: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Decision:
        probes_raw = data.get("probes") or []
        probes = [ProbeQuestion(text=p["text"], source_id=p["source_id"]) for p in probes_raw]
        return cls(
            state=data["state"],
            confidence=data["confidence"],
            matched_criteria=data.get("matched_criteria", []),
            matched_evidence=[
                Evidence(criterion_key=e.get("criterion_key", ""), quote=e.get("quote", ""))
                for e in (data.get("matched_evidence") or [])
            ],
            missing_criteria=data.get("missing_criteria", []),
            out_of_scope_terms=data.get("out_of_scope_terms", []),
            is_verbatim_paste=data.get("is_verbatim_paste", False),
            message=data.get("message", ""),
            probes=probes,
            rationale=data.get("rationale", ""),
        )

    def to_dict(self) -> dict:
        return {
            "state": self.state,
            "confidence": self.confidence,
            "matched_criteria": self.matched_criteria,
            "matched_evidence": [
                {"criterion_key": e.criterion_key, "quote": e.quote} for e in self.matched_evidence
            ],
            "missing_criteria": self.missing_criteria,
            "out_of_scope_terms": self.out_of_scope_terms,
            "is_verbatim_paste": self.is_verbatim_paste,
            "message": self.message,
            "probes": [{"text": p.text, "source_id": p.source_id} for p in self.probes],
            "rationale": self.rationale,
        }
