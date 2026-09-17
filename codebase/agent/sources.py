"""Nguồn đối chiếu — MOCK fixture, y hệt mảng `SRC`/`CRIT` trong
`codebase/prototype/index.html`, để CLI và bản mẫu HTML luôn nói cùng một
phạm vi và cùng ba tiêu chí "đã dạy được" (spec.md §4, dòng "Nội dung 4 đoạn
[T06-138]–[T06-149]": mock — fixture nhóm tự viết, gắn nhãn MOCK).

CP3 thật: đổi `EXCERPTS` để đọc từ `transcript-06-clean.md` (không đưa data
pack vào repo public — xem `.gitignore` và README gốc §Bảo mật dữ liệu).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Excerpt:
    id: str
    text: str


# Bốn đoạn nguồn — MOCK, nhóm tự viết lại ý cho CP2/CP3, không phải data thật.
EXCERPTS: list[Excerpt] = [
    Excerpt(
        "T06-138",
        "Mô hình không tra cứu ở đâu cả. Mỗi bước nó chỉ chọn token tiếp theo "
        "có xác suất cao nhất theo những gì đã học được.",
    ),
    Excerpt(
        "T06-141",
        "Ở vùng kiến thức gần như không có dữ liệu, xác suất vẫn được chuẩn "
        "hoá cho đủ một. Mô hình vẫn buộc phải chọn ra một token, nên nó vẫn "
        "sinh ra câu trả lời thay vì im lặng.",
    ),
    Excerpt(
        "T06-145",
        "Câu bịa thường đọc lên rất trôi chảy, vì thứ mô hình được tối ưu là "
        "độ hợp lý về mặt ngôn ngữ, không phải độ đúng so với sự thật.",
    ),
    Excerpt(
        "T06-149",
        "Muốn giảm bịa thì phải cấp nguồn cho mô hình đọc, hoặc cho nó quyền "
        "nói là không biết.",
    ),
]

EXCERPTS_BY_ID: dict[str, Excerpt] = {e.id: e for e in EXCERPTS}


@dataclass(frozen=True)
class Criterion:
    key: str
    src: str
    label: str
    probe: str


# Ba tiêu chí "đã dạy được" — công bố trước ở M1, không đổi giữa phiên.
CRITERIA: list[Criterion] = [
    Criterion(
        "c1", "T06-138", "cơ chế dự đoán token, không tra cứu",
        "Chỗ này mình chưa theo kịp: lúc bị hỏi một câu nó chưa gặp bao giờ, "
        "mô hình lấy câu trả lời ở đâu ra? Bạn nói lại bước đó giúp mình.",
    ),
    Criterion(
        "c2", "T06-141", "vì sao vẫn trả lời khi thiếu dữ liệu",
        "Nếu chỗ đó gần như không có dữ liệu, sao nó không im luôn mà vẫn ra "
        "được một câu? Mình đang kẹt ở đây.",
    ),
    Criterion(
        "c3", "T06-145", "vì sao câu bịa nghe trôi chảy",
        "Câu bịa mà mình đọc thấy còn xuôi hơn cả câu đúng. Theo bạn thì vì "
        "sao lại thế?",
    ),
]

DEEP_PROBE_SRC = "T06-149"
DEEP_PROBE_TEXT = (
    "Cho mình một ví dụ cụ thể mà mình tự kiểm lại được, để mình chắc là "
    "mình hiểu chứ không phải gật bừa."
)

CONCEPT = "vì sao LLM bịa"
SCOPE_RANGE = "[T06-138]–[T06-149]"


def get_excerpt(excerpt_id: str) -> Excerpt | None:
    return EXCERPTS_BY_ID.get(excerpt_id.strip().upper().replace("T06-", "T06-"))


def format_scope_block() -> str:
    lines = [f"[{e.id}] {e.text}" for e in EXCERPTS]
    return "\n".join(lines)


def format_criteria_block() -> str:
    lines = []
    for i, c in enumerate(CRITERIA, start=1):
        lines.append(f"{i}. {c.label} — [{c.src}]")
    return "\n".join(lines)
