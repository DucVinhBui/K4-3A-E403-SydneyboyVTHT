
# Agent học trò — tích hợp LLM/tool/eval (CP2/CP3)

Đúng spec.md §4–§6: agent học trò với tool-calling, test trên eval, state machine M1→M4 không có đường cụt.

## Cấu trúc

```
codebase/
├── agent/
│   ├── config.py       # Runtime settings (provider, model, API key)
│   ├── sources.py      # MOCK fixture: 4 đoạn nguồn [T06-138]–[T06-149]
│   ├── tools.py        # Tool-calling: list_scope(), get_excerpt(id)
│   ├── prompts.py      # System prompt + JSON schema cho agent
│   ├── schema.py       # Decision, ProbeQuestion (output)
│   ├── providers.py    # Provider interface: mock/openai/anthropic
│   ├── core.py         # StateCheckAgent — lõi quyết định (thay decide() JS)
│   ├── session.py      # TeachingSession — state machine M1→M4
│   ├── cli.py          # CLI test nhanh
│   └── __init__.py
├── eval/
│   ├── samples/        # 5 test case tối thiểu (spec §5)
│   │   ├── 001-day-du.txt
│   │   ├── 002-thieu-2-tieu-chi.txt
│   │   ├── 003-ngoai-pham-vi.txt
│   │   ├── 004-qua-ngan.txt
│   │   └── 005-dan-nguyen-van.txt
│   ├── runner.py       # Eval runner
│   └── __init__.py
├── .env.example        # Template config — copy thành .env
└── README.md           # (file này)
```

## Setup

1. **Môi trường Python ≥3.10** (cần `dataclass`, `|` union type hint).

2. **Không bắt buộc cài dependency** nếu chỉ test với mock provider:
   ```bash
   # Mock provider — chạy ngay không cần API key
   python -m agent.cli "Mô hình bịa vì không có nguồn đọc..."
   ```

3. **Với provider thật** (openai/anthropic/openrouter):
   ```bash
   pip install openai      # đủ cho openai VÀ openrouter (cùng SDK, đổi base_url)
   pip install anthropic   # chỉ cần nếu dùng anthropic
   ```

4. **Config API key**:
   ```bash
   cp .env.example .env
   # Mở .env và điền OPENAI_API_KEY / ANTHROPIC_API_KEY / OPENROUTER_API_KEY
   ```

   Hoặc export trực tiếp:
   ```bash
   export MINILAB_PROVIDER=openai
   export OPENAI_API_KEY=sk-...
   ```

   **OpenRouter** (dùng SDK `openai`, chỉ đổi `base_url` sang `https://openrouter.ai/api/v1`):
   ```bash
   export MINILAB_PROVIDER=openrouter
   export MINILAB_MODEL=openai/gpt-4o-mini   # hoặc bất kỳ model OpenRouter hỗ trợ
   export OPENROUTER_API_KEY=sk-or-v1-...
   ```

## CLI — test nhanh

```bash
# Mock provider (offline, không tốn API credit)
python -m agent.cli "LLM bịa vì..."

# Đọc từ file
python -m agent.cli --file eval/samples/001-day-du.txt

# Dùng OpenAI
python -m agent.cli --provider openai --model gpt-4o-mini "Mô hình không tra cứu..."

# Dùng Anthropic
python -m agent.cli --provider anthropic --model claude-3-5-haiku-latest "..."

# Dùng OpenRouter (LLM thật dùng để chạy golden set CP3)
python -m agent.cli --provider openrouter --model openai/gpt-4o-mini "Mô hình không tra cứu..."

# Output JSON (để pipe vào tool khác)
python -m agent.cli --json "..."
```

**Output** in ra:
- STATE: ĐỦ_CĂN_CỨ / THIẾU_CĂN_CỨ / NGOÀI_PHẠM_VI
- CONFIDENCE: cao / trung bình / thấp / không đánh giá
- MESSAGE: câu agent nói với học viên
- PROBES: câu hỏi ngược (nếu có), gắn `source_id`
- RATIONALE: lý do agent chọn state này (cho eval)

## Ghi vết (logging) — prompt đầu vào + phản hồi thô

Mọi lời gọi LLM thật (openai/anthropic/openrouter — **không** áp dụng cho mock)
được ghi một dòng JSON vào [`logs/llm_calls.jsonl`](logs/llm_calls.jsonl):
`provider`, `model`, `latency_ms`, `request.messages` (toàn bộ prompt, kể cả
system prompt + lịch sử tool-calling), `raw_response` (nguyên văn response
object từ API, qua `model_dump()`), `parsed` (content/tool_calls đã parse),
và `error` nếu request lỗi. File này phục vụ xác minh kỹ thuật — đối chiếu
đúng những gì đã gửi lên mô hình và mô hình trả về, không suy diễn.

`logs/` không commit lên git (rác runtime, xem `.gitignore`).

## Eval — chạy bộ test

**Bộ 5 case tối thiểu** (`eval/samples/`, dùng `eval/runner.py`):
```bash
# Mock provider (baseline heuristic)
python -m eval.runner

# OpenAI
python -m eval.runner --provider openai --model gpt-4o-mini

# Anthropic
python -m eval.runner --provider anthropic

# Output JSON
python -m eval.runner --provider openai --json > results.json
```

**Golden set 25 case theo taxonomy 4 lớp chỗ khó** (`eval/golden_set.json`,
dùng `eval/run_golden.py` — đây là bộ dùng để báo cáo số liệu CP3):
```bash
# Mock provider — chạy nhanh để kiểm tra logic offline
python -m eval.run_golden --provider mock

# LLM thật qua OpenRouter — ghi kết quả UTF-8 ra file (tránh lỗi encode PowerShell)
python -m eval.run_golden --provider openrouter --model openai/gpt-4o-mini --out eval/run_results_raw.json
```

Kết quả đã chạy (2 lượt run-01 → sửa prompt → run-02, pass rate 56%→84%) và
phân tích chi tiết nguyên nhân từng case fail: [`eval/run_results.md`](eval/run_results.md).

**5 test case tối thiểu** (spec.md §5 "Beatable baseline"):
1. `001-day-du.txt` — đủ cả 3 tiêu chí → ĐỦ_CĂN_CỨ
2. `002-thieu-2-tieu-chi.txt` — thiếu c2, c3 → THIẾU_CĂN_CỨ
3. `003-ngoai-pham-vi.txt` — nói về fine-tune, RLHF → NGOÀI_PHẠM_VI
4. `004-qua-ngan.txt` — quá ngắn (<40 ký tự) → THIẾU_CĂN_CỨ
5. `005-dan-nguyen-van.txt` — dán nguyên văn [T06-138] → THIẾU_CĂN_CỨ + verbatim=True

# Chạy bản mẫu để demo CP3

> ⚠️ **`npm start` và cổng `4173` là stack Node cũ của CP2 — không còn dùng.**
> `index.html` hiện gọi 5 endpoint (`/api/config`, `/api/decide`, `/api/eval/cases`, `/api/eval/run`, `/api/flow`)
> mà **chỉ `api/server.py` phục vụ đủ**. Chạy `npm start` sẽ 404 ở màn eval và sơ đồ luồng.

Tạo `codebase/.env` (đã bị `.gitignore` chặn):

```
MINILAB_PROVIDER=openrouter
MINILAB_MODEL=openai/gpt-4o-mini
OPENROUTER_API_KEY=<khoá thật>
```

Chạy:

```bash
cd codebase && python3 -m api.server --port 8765
```

Mở `http://127.0.0.1:8765`. Thanh trạng thái phải hiện **`OPENROUTER · OPENAI/GPT-4O-MINI`**;
còn hiện `BẢN MẪU — MOCK` nghĩa là khoá chưa vào.

Không mở `index.html` bằng `file://` khi demo — trình duyệt cần server cục bộ để giữ kín API key.
API key chỉ được đọc trong tiến trình Python, không gửi xuống trình duyệt.

### Nguồn transcript nội bộ

Prototype chạy được ngay với `sources.example.json`, nhưng giao diện sẽ ghi rõ **NGUỒN MẪU**. Trước khi quay CP3:

```bash
cp codebase/prototype/sources.example.json codebase/prototype/sources.local.json
```

Thay bốn trường `text` trong `sources.local.json` bằng nội dung thật của `[T06-138]`, `[T06-141]`, `[T06-145]`, `[T06-149]`. File này được Git bỏ qua và không được đẩy lên repo public.


Bộ này **fail được và đó là chủ ý** — nếu mock provider đạt 100% thì không cần LLM thật. Mục tiêu: mock đạt 3-4/5, LLM thật (gpt-4o-mini, claude-haiku) đạt ≥4/5.

## Dùng từ code

```python
from agent import StateCheckAgent, Settings

settings = Settings(provider="mock")
agent = StateCheckAgent.from_settings(settings)

decision = agent.decide("Mô hình không tra cứu, chỉ dự đoán token...")
print(decision.state)        # ĐỦ_CĂN_CỨ / THIẾU_CĂN_CỨ / NGOÀI_PHẠM_VI
print(decision.message)      # Câu agent nói
for p in decision.probes:
    print(f"[{p.source_id}] {p.text}")
```

**State machine M1→M4** (full session):
```python
from agent import TeachingSession, StateCheckAgent

agent = StateCheckAgent.from_settings()
session = TeachingSession(agent=agent)

session.start()  # M1 → M2
decision = session.submit_explanation("LLM bịa vì...")  # M2 → M3

if decision.state == "ĐỦ_CĂN_CỨ":
    session.confirm()  # M3 → M4, học viên tự chốt
elif decision.state == "THIẾU_CĂN_CỨ":
    session.revise()   # M3 → M2, bổ sung
else:
    session.end_session()  # M3 → M4, kết thúc

print(session.verdict())  # True nếu "đã dạy được"
```

## So với prototype HTML

| Prototype JS (`index.html`)          | Agent Python (`agent/`)                     |
|--------------------------------------|---------------------------------------------|
| `decide()` heuristic đếm từ khoá     | `StateCheckAgent.decide()` gọi LLM + tool   |
| `SRC`, `CRIT` hard-coded trong JS    | `sources.py` MOCK fixture                   |
| Không có tool-calling                | `tools.py`: `list_scope()`, `get_excerpt()` |
| State machine M1-M4 inline           | `session.py`: `TeachingSession` class       |
| Không có eval                        | `eval/runner.py` + 5 samples                |

## Bước tiếp (CP3 thật)

1. ~~Thêm test case lên 15-20~~ — **xong**, golden set 25 case trong `eval/golden_set.json`.
2. ~~Tích hợp UI gọi backend~~ — **xong**, `index.html` gọi `/api/decide` qua `api/server.py`.
3. **Đổi `sources.py`** đọc từ `transcript-06-clean.md` — **chưa làm**, vẫn dùng fixture MOCK. Cần trước bản nộp cuối.
4. **Chặn false-positive `ĐỦ_CĂN_CỨ`** (case G14) — bắt LLM trả thêm `evidence_quote` cho mỗi tiêu chí rồi validate ở Python. Đây là lỗi đắt nhất theo §7 điều kiện 3.
5. **Log phiên thật** của học viên ở vòng validation CP5 để đo chỉ số học (§7 điều kiện 4).

## Bảo mật

- `.env` đã nằm trong `.gitignore` — **KHÔNG BAO GIỜ** commit API key lên repo.
- Mock provider không gọi API — an toàn dùng trên máy không có mạng hoặc khi demo không muốn lộ key.
- Data pack (transcript thật) KHÔNG đưa vào repo public (xem `.gitignore` gốc + README §Bảo mật dữ liệu).

## License

Đúng license của repo gốc `K4-3A-E403-SydneyboyVTHT`. Agent code này là phần CP2/CP3 nội bộ của nhóm.
