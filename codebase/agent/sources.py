"""Nguồn đối chiếu — nạp từ thư mục `codebase/knowledge/`.

Mỗi file `knowledge/<tên>.json` là một **topic pack**: 4 đoạn nguồn có mã,
3 tiêu chí "đã dạy được", 1 câu hỏi đào sâu. Đây là thứ DUY NHẤT agent được
phép đối chiếu — không có đoạn nào trong pack thì agent không có căn cứ, và
phải trả `NGOÀI_PHẠM_VI` chứ không được tự suy.

Chọn pack bằng biến môi trường `MINILAB_TOPIC` (mặc định `hallucination`, để
golden set và bản mẫu CP2/CP3 không đổi kết quả):

    MINILAB_TOPIC=hallucination   # vì sao LLM bịa            (mặc định)
    MINILAB_TOPIC=toolcall        # vì sao phải cho LLM gọi công cụ
    MINILAB_TOPIC=grounding       # vì sao phải cấp nguồn cho mô hình đọc
    MINILAB_TOPIC=eval-first      # vì sao phải có bộ đo trước khi chỉnh prompt
    MINILAB_TOPIC=automation-level# chọn mức tự động theo chi phí sai

Nội dung các pack hiện tại là **MOCK do nhóm tự viết** (trường `source_label`
của từng file ghi rõ), vì data pack của khoá là tài liệu nội bộ còn repo nộp
bài đang public — xem `spec.md` §4 và `knowledge/README.md`.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"
DEFAULT_TOPIC = "hallucination"


@dataclass(frozen=True)
class Excerpt:
    id: str
    text: str


@dataclass(frozen=True)
class Criterion:
    key: str
    src: str
    label: str
    probe: str


@dataclass(frozen=True)
class Topic:
    name: str
    title: str
    concept: str
    domain: str
    persona_gap: str
    scope_range: str
    source_label: str
    out_of_scope_examples: list[str]
    excerpts: list[Excerpt]
    criteria: list[Criterion]
    deep_probe_src: str
    deep_probe_text: str


class KnowledgeError(ValueError):
    """Pack hỏng — thà nổ lúc khởi động còn hơn để agent đối chiếu với rác."""


def _load_topic_file(path: Path) -> Topic:
    raw = json.loads(path.read_text(encoding="utf-8"))

    def need(field: str):
        if field not in raw:
            raise KnowledgeError(f"{path.name}: thiếu trường '{field}'")
        return raw[field]

    excerpts = [Excerpt(e["id"].strip().upper(), e["text"].strip()) for e in need("excerpts")]
    if not excerpts:
        raise KnowledgeError(f"{path.name}: không có đoạn nguồn nào")

    ids = [e.id for e in excerpts]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        raise KnowledgeError(f"{path.name}: mã đoạn trùng {sorted(dup)}")

    criteria = [
        Criterion(c["key"].strip(), c["src"].strip().upper(), c["label"].strip(), c["probe"].strip())
        for c in need("criteria")
    ]
    for c in criteria:
        if c.src not in ids:
            raise KnowledgeError(
                f"{path.name}: tiêu chí {c.key} trỏ tới '{c.src}' nhưng pack không có mã đó"
            )

    deep = need("deep_probe")
    if deep["src"].strip().upper() not in ids:
        raise KnowledgeError(
            f"{path.name}: deep_probe trỏ tới '{deep['src']}' nhưng pack không có mã đó"
        )

    name = need("name").strip()
    if name != path.stem:
        raise KnowledgeError(f"{path.name}: trường 'name' là '{name}', không khớp tên file")

    return Topic(
        name=name,
        title=need("title").strip(),
        concept=need("concept").strip(),
        domain=need("domain").strip(),
        persona_gap=need("persona_gap").strip(),
        scope_range=need("scope_range").strip(),
        source_label=need("source_label").strip(),
        out_of_scope_examples=[s.strip() for s in raw.get("out_of_scope_examples", [])],
        excerpts=excerpts,
        criteria=criteria,
        deep_probe_src=deep["src"].strip().upper(),
        deep_probe_text=deep["text"].strip(),
    )


def load_topics() -> dict[str, Topic]:
    if not KNOWLEDGE_DIR.is_dir():
        raise KnowledgeError(f"Không thấy thư mục knowledge base: {KNOWLEDGE_DIR}")
    topics = {}
    for path in sorted(KNOWLEDGE_DIR.glob("*.json")):
        t = _load_topic_file(path)
        topics[t.name] = t
    if not topics:
        raise KnowledgeError(f"{KNOWLEDGE_DIR} không có file topic nào (*.json)")
    return topics


TOPICS: dict[str, Topic] = load_topics()


def _active_topic() -> Topic:
    name = os.getenv("MINILAB_TOPIC", DEFAULT_TOPIC).strip().lower()
    if name not in TOPICS:
        raise KnowledgeError(
            f"MINILAB_TOPIC={name!r} không có trong knowledge base. "
            "Chọn một trong: " + ", ".join(sorted(TOPICS))
        )
    return TOPICS[name]


TOPIC: Topic = _active_topic()

# Giao diện cũ — giữ nguyên tên để core/prompts/tools/eval không phải sửa.
EXCERPTS: list[Excerpt] = TOPIC.excerpts
EXCERPTS_BY_ID: dict[str, Excerpt] = {e.id: e for e in EXCERPTS}
CRITERIA: list[Criterion] = TOPIC.criteria
DEEP_PROBE_SRC = TOPIC.deep_probe_src
DEEP_PROBE_TEXT = TOPIC.deep_probe_text
CONCEPT = TOPIC.concept
SCOPE_RANGE = TOPIC.scope_range


def get_excerpt(excerpt_id: str) -> Excerpt | None:
    return EXCERPTS_BY_ID.get(excerpt_id.strip().upper())


def format_scope_block() -> str:
    return "\n".join(f"[{e.id}] {e.text}" for e in EXCERPTS)


def format_criteria_block() -> str:
    return "\n".join(
        f"{i}. {c.label} — [{c.src}]" for i, c in enumerate(CRITERIA, start=1)
    )
