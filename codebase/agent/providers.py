"""Provider LLM — lớp trừu tượng + 3 hiện thực: mock (test offline), openai, anthropic.

Tất cả đều qua interface `Provider.complete(messages, tools, response_format)`,
trả về `{"content": str|None, "tool_calls": list[dict]}` giống OpenAI. Anthropic
có schema khác (block-based) — map ở hàm `_anthropic_to_openai_format()`.

Mock provider: trả ra quyết định giả theo pattern đơn giản, không gọi API thật —
dùng để test eval logic offline khi chưa có hoặc không muốn tốn credit API.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import Settings


def _log_llm_call(
    log_dir: str,
    provider: str,
    model: str,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None,
    raw_response: Any,
    parsed: dict[str, Any],
    latency_ms: float,
    error: str | None = None,
) -> None:
    """Ghi vết (logging) prompt đầu vào và phản hồi thô của mô hình.

    Mỗi lời gọi LLM thật (openai/anthropic/openrouter) được ghi một dòng JSON
    vào `codebase/logs/llm_calls.jsonl` — phục vụ xác minh kỹ thuật (yêu cầu
    "cơ chế ghi vết rõ ràng cho prompt đầu vào và phản hồi thô của mô hình").
    Mock provider không gọi API thật nên không cần log ở đây.
    """
    try:
        base = Path(__file__).resolve().parent.parent / log_dir
        base.mkdir(parents=True, exist_ok=True)
        entry = {
            "id": str(uuid.uuid4()),
            "ts": datetime.now(timezone.utc).isoformat(),
            "provider": provider,
            "model": model,
            "latency_ms": round(latency_ms, 1),
            "request": {"messages": messages, "tools": tools},
            "raw_response": raw_response,
            "parsed": parsed,
            "error": error,
        }
        with open(base / "llm_calls.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
    except OSError:
        # Logging không được để làm sập lời gọi agent chính — chỉ bỏ qua nếu ghi lỗi.
        pass


class Provider(ABC):
    """Interface chung cho mọi provider — cho phép eval chạy đồng dạng trên
    mock/openai/anthropic mà không phải sửa agent logic."""

    @abstractmethod
    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        response_format: dict[str, Any] | None = None,
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        """Gọi LLM, trả về:
        {
            "content": str | None,
            "tool_calls": [{"id": str, "name": str, "arguments": dict}],
        }
        """
        ...


class MockProvider(Provider):
    """Mock provider — KHÔNG gọi API, quyết định heuristic đơn giản (gần giống
    `decide()` trong codebase/prototype/index.html). Dùng để:
    - Test offline khi chưa có key.
    - Baseline cho eval: so sánh heuristic vs LLM thật chênh bao nhiêu.
    - Debug: khi LLM trả lỗi không rõ thì chạy mock trước để chắc logic đúng.
    """

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        response_format: dict[str, Any] | None = None,
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        # Lấy tin cuối — giả định là lời giải thích của học viên
        user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        text_lower = user_msg.lower()
        length = len(user_msg.strip())

        # Hai cổng chặn (deterministic) — giống sơ đồ luồng trong prototype.
        if length < 40:
            return self._mk_decision("THIẾU_CĂN_CỨ", "thấp", "Quá ngắn, chưa đủ để đánh giá.", [])

        # Heuristic giản lược — đếm từ khoá (spec.md §5: đây là rủi ro — không
        # đủ cho transcript văn nói, nhưng đủ làm baseline mock).
        kw_c1 = any(w in text_lower for w in ["dự đoán", "token", "xác suất", "không tra cứu"])
        kw_c2 = any(w in text_lower for w in ["thiếu dữ liệu", "không có dữ liệu", "vẫn trả lời", "buộc phải"])
        kw_c3 = any(w in text_lower for w in ["trôi chảy", "hợp lý", "ngôn ngữ", "không phải sự thật"])
        kw_out = any(w in text_lower for w in ["fine-tune", "rlhf", "gpu", "chi phí", "huấn luyện lại"])

        matched = sum([kw_c1, kw_c2, kw_c3])

        if matched == 0 and kw_out:
            return self._mk_decision(
                "NGOÀI_PHẠM_VI", "không đánh giá",
                "Bốn đoạn [T06-138]–[T06-149] của mình không có chỗ nào nói về cái đó.",
                [],
            )
        if matched == 3:
            return self._mk_decision(
                "ĐỦ_CĂN_CỨ", "cao",
                "Mình nghĩ là mình hiểu rồi — nhưng bạn kiểm lại giúp mình.",
                [],
            )
        # Thiếu 1-2 tiêu chí
        miss = []
        if not kw_c1:
            miss.append("c1")
        if not kw_c2:
            miss.append("c2")
        probes = [
            {"text": "Mô hình lấy câu trả lời ở đâu ra?", "source_id": "T06-138"},
            {"text": "Sao nó không im luôn?", "source_id": "T06-141"},
        ][:len(miss)]
        return self._mk_decision("THIẾU_CĂN_CỨ", "thấp", "Mình còn hổng chỗ này.", probes)

    def _mk_decision(self, state: str, conf: str, msg: str, probes: list) -> dict:
        dec = {
            "state": state,
            "confidence": conf,
            "matched_criteria": [],
            "missing_criteria": [],
            "message": msg,
            "probes": probes,
            "rationale": "[Mock provider — heuristic cứng]",
        }
        return {"content": json.dumps(dec, ensure_ascii=False), "tool_calls": []}


class OpenAIProvider(Provider):
    """OpenAI-compatible provider (gpt-4o-mini, gpt-4o, gpt-4-turbo...) —
    dùng SDK chính thức hoặc HTTP requests trực tiếp nếu không muốn cài thêm."""

    def __init__(self, api_key: str, model: str, log_dir: str = "logs", base_url: str | None = None):
        self.api_key = api_key
        self.model = model
        self.log_dir = log_dir
        self.base_url = base_url
        self._client: Any = None

    def _get_client(self) -> Any:
        if self._client is None:
            try:
                from openai import OpenAI
                kwargs: dict[str, Any] = {"api_key": self.api_key}
                if self.base_url:
                    kwargs["base_url"] = self.base_url
                self._client = OpenAI(**kwargs)
            except ImportError as exc:
                raise RuntimeError(
                    "Thiếu package 'openai'. Cài: pip install openai\n"
                    "Hoặc dùng MINILAB_PROVIDER=mock để test offline."
                ) from exc
        return self._client

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        response_format: dict[str, Any] | None = None,
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        client = self._get_client()
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            kwargs["tools"] = tools
        if response_format:
            kwargs["response_format"] = response_format

        provider_name = "openrouter" if self.base_url else "openai"
        start = time.monotonic()
        error: str | None = None
        raw_dump: Any = None
        result: dict[str, Any] = {"content": None, "tool_calls": []}
        try:
            resp = client.chat.completions.create(**kwargs)
            raw_dump = resp.model_dump() if hasattr(resp, "model_dump") else str(resp)
            msg = resp.choices[0].message
            content = msg.content if hasattr(msg, "content") else None
            tool_calls_raw = msg.tool_calls if hasattr(msg, "tool_calls") else None
            tool_calls = []
            if tool_calls_raw:
                for tc in tool_calls_raw:
                    tool_calls.append({
                        "id": tc.id,
                        "name": tc.function.name,
                        "arguments": json.loads(tc.function.arguments),
                    })
            result = {"content": content, "tool_calls": tool_calls}
            return result
        except Exception as exc:  # noqa: BLE001 — ghi vết lỗi rồi ném lại
            error = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            latency_ms = (time.monotonic() - start) * 1000
            _log_llm_call(
                self.log_dir, provider_name, self.model, messages, tools,
                raw_dump, result, latency_ms, error,
            )


class AnthropicProvider(Provider):
    """Anthropic provider (claude-3-5-haiku, claude-3-5-sonnet...) — map
    schema tool + response format từ OpenAI sang Anthropic block-based."""

    def __init__(self, api_key: str, model: str, log_dir: str = "logs"):
        self.api_key = api_key
        self.model = model
        self.log_dir = log_dir
        self._client: Any = None

    def _get_client(self) -> Any:
        if self._client is None:
            try:
                from anthropic import Anthropic
                self._client = Anthropic(api_key=self.api_key)
            except ImportError as exc:
                raise RuntimeError(
                    "Thiếu package 'anthropic'. Cài: pip install anthropic\n"
                    "Hoặc dùng MINILAB_PROVIDER=mock hoặc openai."
                ) from exc
        return self._client

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        response_format: dict[str, Any] | None = None,
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        client = self._get_client()
        # Anthropic cần tách system message ra ngoài
        system_msg = ""
        user_msgs = []
        for m in messages:
            if m["role"] == "system":
                system_msg = m["content"]
            else:
                user_msgs.append(m)

        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": 4096,
            "temperature": temperature,
            "messages": user_msgs,
        }
        if system_msg:
            kwargs["system"] = system_msg
        if tools:
            # Map OpenAI function schema → Anthropic tool schema
            anthropic_tools = []
            for t in tools:
                fn = t.get("function", {})
                anthropic_tools.append({
                    "name": fn["name"],
                    "description": fn.get("description", ""),
                    "input_schema": fn.get("parameters", {}),
                })
            kwargs["tools"] = anthropic_tools

        start = time.monotonic()
        error: str | None = None
        raw_dump: Any = None
        result: dict[str, Any] = {"content": None, "tool_calls": []}
        try:
            resp = client.messages.create(**kwargs)
            raw_dump = resp.model_dump() if hasattr(resp, "model_dump") else str(resp)
            content_text = ""
            tool_calls = []
            for block in resp.content:
                if block.type == "text":
                    content_text += block.text
                elif block.type == "tool_use":
                    tool_calls.append({
                        "id": block.id,
                        "name": block.name,
                        "arguments": block.input,
                    })
            result = {"content": content_text or None, "tool_calls": tool_calls}
            return result
        except Exception as exc:  # noqa: BLE001
            error = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            latency_ms = (time.monotonic() - start) * 1000
            _log_llm_call(
                self.log_dir, "anthropic", self.model, kwargs.get("messages", []), tools,
                raw_dump, result, latency_ms, error,
            )


def create_provider(settings: Settings) -> Provider:
    if settings.provider == "mock":
        return MockProvider()
    if settings.provider == "openai":
        key = settings.require_key()
        return OpenAIProvider(api_key=key, model=settings.model, log_dir=settings.log_dir)
    if settings.provider == "anthropic":
        key = settings.require_key()
        return AnthropicProvider(api_key=key, model=settings.model, log_dir=settings.log_dir)
    if settings.provider == "openrouter":
        key = settings.require_key()
        return OpenAIProvider(
            api_key=key, model=settings.model, log_dir=settings.log_dir,
            base_url="https://openrouter.ai/api/v1",
        )
    raise ValueError(f"Provider {settings.provider!r} không được hỗ trợ.")
