import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { extname, join, normalize, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(fileURLToPath(new URL("..", import.meta.url)));
const PUBLIC_DIR = join(ROOT, "codebase", "prototype");
const ENV_PATH = join(ROOT, ".env");
const LOCAL_SOURCE_PATH = join(PUBLIC_DIR, "sources.local.json");
const EXAMPLE_SOURCE_PATH = join(PUBLIC_DIR, "sources.example.json");

await loadEnv(ENV_PATH);

const PORT = Number(process.env.PORT || 4173);
const MODEL = process.env.OPENAI_MODEL || "gpt-5-mini";

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png"
};

const schema = {
  type: "object",
  additionalProperties: false,
  required: ["state", "confidence", "kind", "summary", "missing_labels", "out_topics", "citations", "probes"],
  properties: {
    state: { type: "string", enum: ["ĐỦ_CĂN_CỨ", "THIẾU_CĂN_CỨ", "NGOÀI_PHẠM_VI"] },
    confidence: { type: "string", enum: ["cao", "thấp", "không đánh giá"] },
    kind: { type: "string", enum: ["ok", "gap", "out"] },
    summary: { type: "string" },
    missing_labels: { type: "array", items: { type: "string" } },
    out_topics: { type: "array", items: { type: "string" } },
    citations: {
      type: "array",
      items: { type: "string", enum: ["T06-136", "T06-138", "T06-139", "T06-148"] }
    },
    probes: {
      type: "array",
      maxItems: 2,
      items: {
        type: "object",
        additionalProperties: false,
        required: ["text", "source_id"],
        properties: {
          text: { type: "string" },
          source_id: { type: "string", enum: ["T06-136", "T06-138", "T06-139", "T06-148"] }
        }
      }
    }
  }
};

const instructions = `Bạn là agent học trò kiểm tra một lời giải thích bằng phương pháp teach-back.
Chỉ được dùng các đoạn nguồn được cung cấp. Không dùng kiến thức ngoài nguồn.

Ba tiêu chí:
1. Nêu cơ chế mô hình dự đoán token có xác suất cao nhất — T06-136.
2. Giải thích bias có thể đi từ dữ liệu internet đến các chuyên gia tinh chỉnh, nên hallucination vẫn tồn tại — T06-138 và T06-139.
3. Nêu knowledge cutoff: mô hình không biết sự kiện sau mốc dữ liệu nếu không có công cụ truy xuất — T06-148.

Quy tắc:
- Đánh giá ý nghĩa, không đếm từ khóa. Phủ định sai hoặc nhắc từ khóa không có lập luận thì không đạt.
- ĐỦ_CĂN_CỨ khi đủ cả ba tiêu chí bằng lời người học. kind=ok, confidence=cao, probes=[] và missing_labels=[].
- THIẾU_CĂN_CỨ khi người học đang cố trả lời câu “vì sao LLM bịa” nhưng thiếu ý, chỉ nêu một phần, hoặc nói sai/trái với nguồn. Một câu trả lời sai về đúng chủ đề vẫn là THIẾU_CĂN_CỨ, không phải NGOÀI_PHẠM_VI. kind=gap, confidence=thấp, hỏi đúng 2 câu ngắn vào chỗ thiếu hoặc sai; không đưa đáp án.
- NGOÀI_PHẠM_VI chỉ khi câu trả lời chủ yếu chuyển sang một chủ đề khác không nhằm giải thích vì sao LLM bịa, ví dụ GPU, chi phí, MCP, quantization hoặc so sánh kiến trúc. kind=out, confidence=không đánh giá, probes=[]; không phán đúng/sai.
- citations và source_id chỉ được dùng bốn mã nguồn đã cho.
- Nếu ĐỦ_CĂN_CỨ, citations phải chứa đủ T06-136, T06-138, T06-139 và T06-148.
- Nếu THIẾU_CĂN_CỨ, citations phải chứa các source_id được dùng trong hai câu hỏi.
- Nếu NGOÀI_PHẠM_VI, citations=[] và probes=[].
- Không tự kết luận người học đã hiểu; chỉ đánh giá mức căn cứ của lời giải thích.`;

const server = createServer(async (req, res) => {
  try {
    const url = new URL(req.url || "/", `http://${req.headers.host || "localhost"}`);

    if (req.method === "GET" && url.pathname === "/api/health") {
      const source = await loadSource();
      return json(res, 200, {
        ok: true,
        apiKeyConfigured: Boolean(process.env.OPENAI_API_KEY),
        model: MODEL,
        sourceMock: Boolean(source.mock),
        sourceLabel: source.label || "Nguồn cục bộ"
      });
    }

    if (req.method === "GET" && url.pathname === "/api/source") {
      return json(res, 200, await loadSource());
    }

    if (req.method === "POST" && url.pathname === "/api/decide") {
      const body = await readJsonBody(req);
      const answer = String(body.answer || "").trim();
      if (!answer) return json(res, 400, { error: "Câu trả lời đang trống." });
      if (answer.length > 5000) return json(res, 400, { error: "Câu trả lời vượt quá 5.000 ký tự." });

      const source = await loadSource();
      const gated = localAssessment(answer, source);
      if (gated) return json(res, 200, { ...gated, model: "local-gate", sourceMock: Boolean(source.mock), usage: null });

      if (!process.env.OPENAI_API_KEY) {
        return json(res, 503, { error: "Chưa có OPENAI_API_KEY trong file .env." });
      }

      const apiResponse = await fetch("https://api.openai.com/v1/responses", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: MODEL,
          store: false,
          instructions,
          input: JSON.stringify({
            source: source.excerpts,
            learner_answer: answer
          }),
          text: {
            format: {
              type: "json_schema",
              name: "teach_back_assessment",
              strict: true,
              schema
            }
          }
        })
      });

      const payload = await apiResponse.json();
      if (!apiResponse.ok) {
        const message = payload?.error?.message || `OpenAI API trả về HTTP ${apiResponse.status}.`;
        return json(res, apiResponse.status, { error: message });
      }

      let assessment;
      try {
        assessment = JSON.parse(extractOutputText(payload));
      } catch {
        return json(res, 502, { error: "AI không trả về JSON hợp lệ." });
      }

      if (assessment.state === "THIẾU_CĂN_CỨ" && assessment.probes.length !== 2) {
        return json(res, 502, { error: "AI chưa trả đúng hai câu hỏi ngược." });
      }

      return json(res, 200, {
        ...assessment,
        model: payload.model || MODEL,
        sourceMock: Boolean(source.mock),
        usage: payload.usage || null
      });
    }

    if (req.method !== "GET" && req.method !== "HEAD") {
      return json(res, 405, { error: "Method not allowed" });
    }

    return serveStatic(url.pathname, res, req.method === "HEAD");
  } catch (error) {
    console.error(error);
    return json(res, 500, { error: "Lỗi server cục bộ. Xem terminal để biết chi tiết." });
  }
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`CP3 prototype: http://127.0.0.1:${PORT}`);
  console.log(`Model: ${MODEL}`);
  console.log(process.env.OPENAI_API_KEY ? "API key: đã cấu hình" : "API key: CHƯA CẤU HÌNH — điền OPENAI_API_KEY trong .env rồi khởi động lại");
});

async function loadEnv(path) {
  try {
    const text = await readFile(path, "utf8");
    for (const rawLine of text.split(/\r?\n/)) {
      const line = rawLine.trim();
      if (!line || line.startsWith("#")) continue;
      const splitAt = line.indexOf("=");
      if (splitAt < 1) continue;
      const key = line.slice(0, splitAt).trim();
      let value = line.slice(splitAt + 1).trim();
      if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      if (!(key in process.env)) process.env[key] = value;
    }
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
}

async function loadSource() {
  for (const path of [LOCAL_SOURCE_PATH, EXAMPLE_SOURCE_PATH]) {
    try {
      const source = JSON.parse(await readFile(path, "utf8"));
      if (!Array.isArray(source.excerpts) || source.excerpts.length !== 4) {
        throw new Error(`${path} phải chứa đúng 4 excerpts.`);
      }
      const expectedIds = ["T06-136", "T06-138", "T06-139", "T06-148"];
      if (source.excerpts.some((item, index) => item.id !== expectedIds[index] || typeof item.text !== "string" || !item.text.trim())) {
        throw new Error(`${path} phải giữ đúng bốn mã nguồn và mỗi đoạn phải có text.`);
      }
      return source;
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
  }
  throw new Error("Không tìm thấy file nguồn.");
}

function localAssessment(answer, source) {
  const normalized = answer.toLowerCase().replace(/\s+/g, " ").trim();
  for (const excerpt of source.excerpts) {
    const text = excerpt.text.toLowerCase().replace(/\s+/g, " ").trim();
    for (let offset = 0; offset + 40 <= text.length; offset += 10) {
      if (normalized.includes(text.slice(offset, offset + 40))) {
        return {
          state: "THIẾU_CĂN_CỨ",
          confidence: "thấp",
          kind: "gap",
          summary: "Câu trả lời sao chép nguyên văn nguồn thay vì diễn đạt bằng lời người học.",
          missing_labels: ["diễn đạt bằng lời của người học"],
          out_topics: [],
          citations: [excerpt.id, "T06-148"],
          probes: [
            { text: "Bạn nói lại ý vừa trích bằng lời của mình được không?", source_id: excerpt.id },
            { text: "Bạn cho một ví dụ cụ thể để tự kiểm lại cách hiểu này được không?", source_id: "T06-148" }
          ]
        };
      }
    }
  }

  if (normalized.length < 40) {
    return {
      state: "THIẾU_CĂN_CỨ",
      confidence: "thấp",
      kind: "gap",
      summary: "Câu trả lời quá ngắn để đối chiếu đủ ba tiêu chí.",
      missing_labels: ["cơ chế", "lập luận"],
      out_topics: [],
      citations: ["T06-136"],
      probes: [
        { text: "Bạn viết dài thêm một chút về cách mô hình tạo câu trả lời được không?", source_id: "T06-136" },
        { text: "Theo bạn, bias trong dữ liệu và quá trình tinh chỉnh liên quan thế nào đến hallucination?", source_id: "T06-138" }
      ]
    };
  }
  return null;
}

async function readJsonBody(req) {
  let text = "";
  for await (const chunk of req) {
    text += chunk;
    if (text.length > 20_000) throw new Error("Request body quá lớn.");
  }
  try {
    return JSON.parse(text || "{}");
  } catch {
    throw new Error("Request body không phải JSON hợp lệ.");
  }
}

async function serveStatic(pathname, res, headOnly) {
  const relative = pathname === "/" ? "index.html" : decodeURIComponent(pathname).replace(/^\/+/, "");
  const safePath = normalize(join(PUBLIC_DIR, relative));
  if (safePath !== PUBLIC_DIR && !safePath.startsWith(PUBLIC_DIR + sep)) {
    return json(res, 403, { error: "Forbidden" });
  }

  try {
    const info = await stat(safePath);
    const filePath = info.isDirectory() ? join(safePath, "index.html") : safePath;
    const data = await readFile(filePath);
    res.writeHead(200, {
      "Content-Type": MIME[extname(filePath)] || "application/octet-stream",
      "Cache-Control": "no-store"
    });
    res.end(headOnly ? undefined : data);
  } catch (error) {
    if (error.code === "ENOENT") return json(res, 404, { error: "Not found" });
    throw error;
  }
}

function json(res, status, data) {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" });
  res.end(JSON.stringify(data));
}

function extractOutputText(payload) {
  if (typeof payload.output_text === "string" && payload.output_text.trim()) {
    return payload.output_text;
  }
  const texts = [];
  for (const item of payload.output || []) {
    for (const content of item.content || []) {
      if (content.type === "output_text" && typeof content.text === "string") {
        texts.push(content.text);
      }
    }
  }
  if (!texts.length) throw new Error("Response không có output_text.");
  return texts.join("");
}
