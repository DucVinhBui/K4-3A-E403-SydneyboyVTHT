import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const baseUrl = process.env.CP3_BASE_URL || "http://127.0.0.1:4173";
const casesPath = resolve("eval/cases.json");
const resultsPath = resolve("eval/results.json");
const cases = JSON.parse(await readFile(casesPath, "utf8"));
const results = [];
const sourceResponse = await fetch(`${baseUrl}/api/source`);
if (!sourceResponse.ok) throw new Error(`Không đọc được nguồn đánh giá: HTTP ${sourceResponse.status}`);
const source = await sourceResponse.json();
const sourceById = new Map(source.excerpts.map((item) => [item.id, item.text]));

for (const testCase of cases) {
  const started = Date.now();
  try {
    const answer = testCase.mode === "paste"
      ? testCase.sourceIds.map((id) => sourceById.get(id)).filter(Boolean).join(" ")
      : testCase.answer;
    const response = await fetch(`${baseUrl}/api/decide`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answer })
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.error || `HTTP ${response.status}`);

    const allowedSources = new Set(["T06-136", "T06-138", "T06-139", "T06-148"]);
    const probes = Array.isArray(body.probes) ? body.probes : [];
    const citations = Array.isArray(body.citations) ? body.citations : [];
    const probeCountOk = body.state === "THIẾU_CĂN_CỨ" ? probes.length === 2 : probes.length === 0;
    const probeSourcesOk = probes.every((probe) => allowedSources.has(probe.source_id));
    const citationsValid = citations.every((id) => allowedSources.has(id));
    const okHasCoreSources = body.state !== "ĐỦ_CĂN_CỨ" || ["T06-136", "T06-138", "T06-139", "T06-148"].every((id) => citations.includes(id));
    const structureOk = probeCountOk && probeSourcesOk && citationsValid && okHasCoreSources &&
      typeof body.summary === "string" && body.summary.length > 0;
    results.push({
      id: testCase.id,
      expected: testCase.expected,
      actual: body.state,
      stateCorrect: body.state === testCase.expected,
      structureCorrect: structureOk,
      pass: body.state === testCase.expected && structureOk,
      latencyMs: Date.now() - started,
      citations: body.citations,
      model: body.model || null,
      error: null
    });
  } catch (error) {
    results.push({
      id: testCase.id,
      expected: testCase.expected,
      actual: null,
      stateCorrect: false,
      structureCorrect: false,
      pass: false,
      latencyMs: Date.now() - started,
      citations: [],
      model: null,
      error: error.message
    });
  }
  console.log(`${results.at(-1).pass ? "PASS" : "FAIL"} ${testCase.id}: ${results.at(-1).actual || results.at(-1).error}`);
}

const passed = results.filter((result) => result.pass).length;
const report = {
  generatedAt: new Date().toISOString(),
  baseUrl,
  model: results.find((result) => result.model)?.model || null,
  sourceMock: Boolean(source.mock),
  sourceLabel: source.label || null,
  total: results.length,
  passed,
  accuracyPercent: Number(((passed / results.length) * 100).toFixed(1)),
  results
};

await writeFile(resultsPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(`\nKết quả: ${passed}/${results.length} (${report.accuracyPercent}%)`);
console.log(`Đã lưu: ${resultsPath}`);
if (passed !== results.length) process.exitCode = 1;
