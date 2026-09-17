import { mkdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const baseUrl = process.env.CP3_BASE_URL || "http://127.0.0.1:4173";
const dryRun = process.env.CP3_DRY_RUN === "1";
const goldenSetPath = resolve("eval/cases.json");
const latestPath = resolve("eval/results.json");
const runsDir = resolve("eval/runs");
const measurementPath = resolve("eval/cp3-measurement.md");
const cases = JSON.parse(await readFile(goldenSetPath, "utf8"));
const generatedAt = new Date().toISOString();
const runId = generatedAt.replace(/[:.]/g, "-");
const runPath = resolve(runsDir, `${runId}.json`);

let source = null;
let runError = null;
const results = [];

if (dryRun) {
  runError = "Dry run: chưa gửi transcript hoặc test case tới API.";
} else {
  try {
    const sourceResponse = await fetch(`${baseUrl}/api/source`);
    if (!sourceResponse.ok) throw new Error(`Không đọc được nguồn: HTTP ${sourceResponse.status}`);
    source = await sourceResponse.json();
  } catch (error) {
    runError = `Không thể bắt đầu bộ test: ${error.message}`;
  }
}

const sourceById = new Map((source?.excerpts || []).map((item) => [item.id, item.text]));
const allowedSources = new Set(["T06-136", "T06-138", "T06-139", "T06-148"]);
const requiredCoreSources = ["T06-136", "T06-138", "T06-139", "T06-148"];

for (const testCase of cases) {
  if (runError) {
    results.push(notRunResult(testCase, runError));
    continue;
  }

  const started = Date.now();
  try {
    const answer = testCase.mode === "paste"
      ? testCase.sourceIds.map((id) => sourceById.get(id)).filter(Boolean).join(" ")
      : testCase.answer;
    if (!answer) throw new Error("Test case không tạo được nội dung đầu vào.");

    const response = await fetch(`${baseUrl}/api/decide`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answer })
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.error || `HTTP ${response.status}`);

    const probes = Array.isArray(body.probes) ? body.probes : [];
    const citations = Array.isArray(body.citations) ? body.citations : [];
    const probeCountOk = body.state === "THIẾU_CĂN_CỨ" ? probes.length === 2 : probes.length === 0;
    const probeSourcesOk = probes.every((probe) => allowedSources.has(probe.source_id));
    const citationsValid = citations.every((id) => allowedSources.has(id));
    const okHasCoreSources = body.state !== "ĐỦ_CĂN_CỨ" || requiredCoreSources.every((id) => citations.includes(id));
    const structureCorrect = probeCountOk && probeSourcesOk && citationsValid && okHasCoreSources &&
      typeof body.summary === "string" && body.summary.length > 0;
    const stateCorrect = body.state === testCase.expected;
    const pass = stateCorrect && structureCorrect;

    results.push({
      id: testCase.id,
      expected: testCase.expected,
      actual: body.state,
      outcome: pass ? "ĐẠT" : "CHƯA_ĐẠT",
      executed: true,
      stateCorrect,
      structureCorrect,
      pass,
      latencyMs: Date.now() - started,
      citations,
      model: body.model || null,
      technicalError: null
    });
  } catch (error) {
    results.push({
      id: testCase.id,
      expected: testCase.expected,
      actual: null,
      outcome: "LỖI_KỸ_THUẬT",
      executed: true,
      stateCorrect: false,
      structureCorrect: false,
      pass: false,
      latencyMs: Date.now() - started,
      citations: [],
      model: null,
      technicalError: error.message
    });
  }

  const latest = results.at(-1);
  console.log(`${latest.outcome} ${latest.id}: ${latest.actual || latest.technicalError}`);
}

const counts = {
  total: results.length,
  executed: results.filter((item) => item.executed).length,
  passed: results.filter((item) => item.outcome === "ĐẠT").length,
  failed: results.filter((item) => item.outcome === "CHƯA_ĐẠT").length,
  technicalErrors: results.filter((item) => item.outcome === "LỖI_KỸ_THUẬT").length,
  notRun: results.filter((item) => item.outcome === "CHƯA_CHẠY").length
};
const accuracyPercent = counts.executed - counts.technicalErrors > 0
  ? Number(((counts.passed / (counts.executed - counts.technicalErrors)) * 100).toFixed(1))
  : null;
const overallOutcome = counts.notRun === counts.total ? "CHƯA_CHẠY"
  : counts.technicalErrors > 0 ? "LỖI_KỸ_THUẬT"
    : counts.failed > 0 ? "CHƯA_ĐẠT" : "ĐẠT";
const validForSubmission = overallOutcome !== "CHƯA_CHẠY" &&
  counts.executed === counts.total && counts.technicalErrors === 0 && source?.mock === false;

const report = {
  runId,
  generatedAt,
  overallOutcome,
  validForSubmission,
  runError,
  baseUrl,
  goldenSet: "eval/cases.json",
  model: results.find((item) => item.model)?.model || null,
  sourceMock: source ? Boolean(source.mock) : null,
  sourceLabel: source?.label || null,
  ...counts,
  accuracyPercent,
  results
};

await mkdir(runsDir, { recursive: true });
const serialized = `${JSON.stringify(report, null, 2)}\n`;
await writeFile(runPath, serialized, "utf8");
await writeFile(latestPath, serialized, "utf8");
await writeFile(measurementPath, renderMeasurement(report), "utf8");

console.log(`\nTrạng thái: ${overallOutcome}`);
console.log(`Đã chạy: ${counts.executed}/${counts.total}`);
console.log(`Đạt: ${counts.passed} · Chưa đạt: ${counts.failed} · Lỗi kỹ thuật: ${counts.technicalErrors} · Chưa chạy: ${counts.notRun}`);
console.log(`Độ chính xác: ${accuracyPercent === null ? "chưa có" : `${accuracyPercent}%`}`);
console.log(`Lưu lượt chạy: ${runPath}`);
console.log(`Số đo để nộp: ${measurementPath}`);

if (!dryRun && overallOutcome !== "ĐẠT") process.exitCode = 1;

function notRunResult(testCase, reason) {
  return {
    id: testCase.id,
    expected: testCase.expected,
    actual: null,
    outcome: "CHƯA_CHẠY",
    executed: false,
    stateCorrect: null,
    structureCorrect: null,
    pass: false,
    latencyMs: 0,
    citations: [],
    model: null,
    technicalError: reason
  };
}

function renderMeasurement(run) {
  const accuracy = run.accuracyPercent === null ? "chưa có" : `${run.accuracyPercent}%`;
  const submission = run.validForSubmission
    ? "Có — đủ 20 ca, không có lỗi kỹ thuật và dùng transcript thật."
    : "Chưa — chỉ nộp sau khi đủ 20 ca, không có lỗi kỹ thuật và `sourceMock: false`.";
  const failures = run.results.filter((item) => item.outcome !== "ĐẠT");
  const failureLines = failures.length
    ? failures.map((item) => `- \`${item.id}\`: **${item.outcome}**${item.technicalError ? ` — ${item.technicalError}` : ` — dự kiến \`${item.expected}\`, thực tế \`${item.actual}\``}`).join("\n")
    : "- Không có.";

  return `# Số đo CP3 — Agent học trò\n\n` +
    `- **Run ID:** \`${run.runId}\`\n` +
    `- **Thời điểm:** ${run.generatedAt}\n` +
    `- **Golden set:** \`${run.goldenSet}\`\n` +
    `- **Model:** ${run.model || "chưa xác định"}\n` +
    `- **Nguồn:** ${run.sourceLabel || "chưa đọc được"} · \`sourceMock: ${run.sourceMock}\`\n` +
    `- **Trạng thái lượt chạy:** **${run.overallOutcome}**\n` +
    `- **Đã chạy:** ${run.executed}/${run.total}\n` +
    `- **Đạt:** ${run.passed}/${run.total}\n` +
    `- **Chưa đạt:** ${run.failed}\n` +
    `- **Lỗi kỹ thuật:** ${run.technicalErrors}\n` +
    `- **Chưa chạy:** ${run.notRun}\n` +
    `- **Độ chính xác trên ca đã có kết quả:** ${accuracy}\n` +
    `- **Đủ điều kiện dùng làm số đo nộp:** ${submission}\n\n` +
    `## Ca chưa đạt, lỗi kỹ thuật hoặc chưa chạy\n\n${failureLines}\n\n` +
    `Chi tiết máy đọc được của lượt này: \`eval/runs/${run.runId}.json\`.\n`;
}
