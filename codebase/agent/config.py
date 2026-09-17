"""Cấu hình runtime: chọn provider LLM, model, khoá API — đọc từ biến môi trường.

Không có key thật trong repo (theo `.gitignore` và luật bảo mật ở README gốc).
Copy `.env.example` ở gốc `codebase/` thành `.env` rồi điền key của bạn, hoặc
export trực tiếp biến môi trường trước khi chạy CLI.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _load_dotenv_if_present() -> None:
    """Đọc file `.env` cạnh package này (nếu có) mà không cần cài `python-dotenv`.

    Cố tình tự viết thay vì bắt buộc thêm dependency — CLI vẫn phải chạy được
    ở máy không có mạng để cài package.
    """
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)


_load_dotenv_if_present()

VALID_PROVIDERS = ("mock", "openai", "anthropic", "openrouter")


@dataclass
class Settings:
    provider: str = field(default_factory=lambda: os.environ.get("MINILAB_PROVIDER", "mock").lower())
    model: str = field(default_factory=lambda: os.environ.get("MINILAB_MODEL", ""))
    openai_api_key: str = field(default_factory=lambda: os.environ.get("OPENAI_API_KEY", ""))
    anthropic_api_key: str = field(default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY", ""))
    openrouter_api_key: str = field(default_factory=lambda: os.environ.get("OPENROUTER_API_KEY", ""))
    temperature: float = field(default_factory=lambda: float(os.environ.get("MINILAB_TEMPERATURE", "0.2")))
    max_tool_hops: int = field(default_factory=lambda: int(os.environ.get("MINILAB_MAX_TOOL_HOPS", "4")))
    log_dir: str = field(default_factory=lambda: os.environ.get("MINILAB_LOG_DIR", "logs"))

    def __post_init__(self) -> None:
        if self.provider not in VALID_PROVIDERS:
            raise ValueError(
                f"MINILAB_PROVIDER={self.provider!r} không hợp lệ. "
                f"Chọn một trong: {', '.join(VALID_PROVIDERS)}"
            )
        if not self.model:
            self.model = {
                "openai": "gpt-4o-mini",
                "anthropic": "claude-3-5-haiku-latest",
                "openrouter": "openai/gpt-4o-mini",
                "mock": "mock-decide-v1",
            }[self.provider]

    def require_key(self) -> str:
        if self.provider == "openai":
            if not self.openai_api_key:
                raise RuntimeError(
                    "Thiếu OPENAI_API_KEY. Đặt biến môi trường hoặc điền vào codebase/.env "
                    "(copy từ .env.example). Hoặc dùng MINILAB_PROVIDER=mock để test offline."
                )
            return self.openai_api_key
        if self.provider == "anthropic":
            if not self.anthropic_api_key:
                raise RuntimeError(
                    "Thiếu ANTHROPIC_API_KEY. Đặt biến môi trường hoặc điền vào codebase/.env "
                    "(copy từ .env.example). Hoặc dùng MINILAB_PROVIDER=mock để test offline."
                )
            return self.anthropic_api_key
        if self.provider == "openrouter":
            if not self.openrouter_api_key:
                raise RuntimeError(
                    "Thiếu OPENROUTER_API_KEY. Đặt biến môi trường hoặc điền vào codebase/.env "
                    "(copy từ .env.example). Hoặc dùng MINILAB_PROVIDER=mock để test offline."
                )
            return self.openrouter_api_key
        return ""


def load_settings() -> Settings:
    return Settings()
