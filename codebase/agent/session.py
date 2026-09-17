"""State-check-agent: state machine M1→M4 y hệt bốn màn trong
`codebase/prototype/index.html`, nhưng gọi `StateCheckAgent.decide()` (LLM
thật/mock) ở M2→M3 thay cho hàm JS `decide()` heuristic.

Bốn trạng thái màn (khác với "state" ĐỦ_CĂN_CỨ/THIẾU_CĂN_CỨ/NGOÀI_PHẠM_VI của
Decision — đây là state của *phiên*, không phải state của *câu trả lời*):

    M1 (mở phiên) → M2 (dạy lại) → M3 (agent hỏi ngược) → M4 (kết phiên)
                        ↑______________|
                        (revise / bổ sung — bài cũ giữ nguyên, spec §4b G9)

Bất biến (invariant) mà class này phải giữ đúng, đối chiếu với spec.md §6
"Không có đường cụt":
  - Từ M3, luôn có đường về M2 (revise) VÀ đường sang M4 (end_session) VÀ
    đường "disagree" (correction) — không bao giờ bị kẹt.
  - M4 luôn có đường sang M2 (dạy lại lần nữa) hoặc restart hoàn toàn.
  - Nút "Không đồng ý" (disagree) có ở MỌI trạng thái M3, kể cả nhánh ok.
  - "Đã dạy được" ở M4 chỉ đúng khi học viên tự xác nhận sau ĐỦ_CĂN_CỨ
    (agent không tự chốt — spec §4 Automation: augment).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .core import StateCheckAgent
from .schema import Decision

ScreenType = Literal["m1", "m2", "m3", "m4"]


@dataclass
class LogEntry:
    turn: int
    what: str
    state: str = "—"
    src: str = "—"


class SessionError(RuntimeError):
    """Gọi hành động không hợp lệ ở trạng thái hiện tại (state-check thất bại)."""


@dataclass
class TeachingSession:
    """Một phiên dạy lại — quản lý đúng bốn màn M1-M4, gọi agent ở M2→M3."""

    agent: StateCheckAgent
    screen: ScreenType = "m1"
    turn: int = 0
    log: list[LogEntry] = field(default_factory=list)
    last_decision: Decision | None = None
    last_answer: str = ""
    _disagree_open: bool = field(default=False, repr=False)

    # ── M1 → M2 ──────────────────────────────────────────────────────────
    def start(self) -> None:
        """Bấm 'Bắt đầu dạy lại' ở M1."""
        self._require_screen("m1", "start")
        self.screen = "m2"

    # ── M2 → M3 (điểm gọi agent) ─────────────────────────────────────────
    def submit_explanation(self, text: str) -> Decision:
        """Học viên gửi lời giải thích. Đây là điểm cắm agent — tương ứng
        `send` handler + `decide()` trong prototype JS."""
        self._require_screen("m2", "submit_explanation")
        text = text.strip()
        if not text:
            raise SessionError("Lời giải thích rỗng — không gửi được (giống guard `if (!v) return;` ở JS).")

        self.turn += 1
        self.last_answer = text
        decision = self.agent.decide(text)
        self.last_decision = decision

        src_summary = ", ".join(p.source_id for p in decision.probes) if decision.probes else "—"
        self.log.append(LogEntry(
            turn=self.turn,
            what=f"Học viên gửi lời giải thích ({len(text)} ký tự) → agent đánh giá",
            state=decision.state,
            src=src_summary,
        ))
        self.screen = "m3"
        self._disagree_open = False
        return decision

    # ── M3 actions ───────────────────────────────────────────────────────
    def confirm(self) -> None:
        """Nhánh happy path: 'Mình đã đối chiếu — đúng rồi' (chỉ hợp lệ khi
        state ĐỦ_CĂN_CỨ). Đây là chỗ HỌC VIÊN tự chốt, KHÔNG phải agent
        (spec §4 Automation: augment)."""
        self._require_screen("m3", "confirm")
        if self.last_decision is None or self.last_decision.state != "ĐỦ_CĂN_CỨ":
            raise SessionError("confirm() chỉ hợp lệ khi Decision.state == 'ĐỦ_CĂN_CỨ'.")
        self.log.append(LogEntry(
            turn=self.turn,
            what="Học viên tự đối chiếu và xác nhận với đoạn nguồn",
            state=self.last_decision.state,
            src="T06-138/141/145",
        ))
        self.screen = "m4"

    def revise(self) -> None:
        """Nhánh low-confidence / out-of-scope: quay lại M2, bài cũ giữ
        nguyên (spec §4b G9 — 'Sửa dễ dàng')."""
        self._require_screen("m3", "revise")
        state = self.last_decision.state if self.last_decision else "—"
        self.log.append(LogEntry(
            turn=self.turn,
            what="Học viên quay lại bổ sung (bài viết được giữ nguyên)",
            state=state,
        ))
        self.screen = "m2"
        self._disagree_open = False

    def disagree(self) -> None:
        """Mở form 'Không đồng ý với đánh giá này' — có ở MỌI trạng thái M3."""
        self._require_screen("m3", "disagree")
        self._disagree_open = True

    def correct(self, corrected_state: str, why: str = "") -> None:
        """Học viên ghi lại đánh giá đúng ra phải là gì. Vô hiệu hoá quyết
        định của agent — 'giữ quyền quyết định' (spec §6 nhánh ④ Correction)."""
        self._require_screen("m3", "correct")
        if not self._disagree_open:
            raise SessionError("Phải gọi disagree() trước khi correct().")
        what = "Học viên không đồng ý với đánh giá của agent"
        if why:
            what += f": \u201c{why}\u201d"
        self.log.append(LogEntry(turn=self.turn, what=what, state=f"{corrected_state} (học viên sửa)"))
        self._disagree_open = False
        # Đánh giá agent không còn được dùng để kết luận — không đổi last_decision.state
        # thật, chỉ ghi log; state machine vẫn ở m3, học viên chọn tiếp confirm/revise/end.

    def end_session(self) -> None:
        """Nút 'Kết thúc phiên' — có ở MỌI màn M3, không có đường cụt."""
        self._require_screen("m3", "end_session")
        self.log.append(LogEntry(
            turn=self.turn,
            what="Học viên kết thúc phiên",
            state=self.last_decision.state if self.last_decision else "—",
        ))
        self.screen = "m4"

    # ── M4 ───────────────────────────────────────────────────────────────
    def teach_again(self) -> None:
        self._require_screen("m4", "teach_again")
        self.screen = "m2"

    def restart(self) -> None:
        self._require_screen("m4", "restart")
        self.turn = 0
        self.log = []
        self.last_decision = None
        self.last_answer = ""
        self._disagree_open = False
        self.screen = "m1"

    def verdict(self) -> bool:
        """'Đã dạy được' — chỉ đúng khi có ít nhất một lượt học viên TỰ xác
        nhận sau ĐỦ_CĂN_CỨ. Y hệt điều kiện `taught` trong prototype JS:
        `log.some(r => r.what.indexOf("tự đối chiếu và xác nhận") !== -1)`.
        """
        return any("tự đối chiếu và xác nhận" in r.what for r in self.log)

    # ── invariant check nội bộ ───────────────────────────────────────────
    def _require_screen(self, expected: ScreenType, action: str) -> None:
        if self.screen != expected:
            raise SessionError(
                f"Không thể gọi {action}() ở màn '{self.screen}' — cần đang ở màn '{expected}'."
            )
