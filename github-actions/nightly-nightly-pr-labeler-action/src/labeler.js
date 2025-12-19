// Minimal PR title labeler
// Reads INPUT_TITLE env var (GitHub actions prefix)
// Determines labels and writes to GITHUB_OUTPUT

function getInput(name) {
  const envName = `INPUT_${name.toUpperCase()}`;
  return process.env[envName] || "";
}

function setOutput(name, value) {
  const outputPath = process.env["GITHUB_OUTPUT"];
  if (!outputPath) return;
  const fs = require("fs");
  fs.appendFileSync(outputPath, `${name}=${value}\n`);
}

function suggestLabels(title) {
  const lower = title.toLowerCase();
  const labels = [];
  if (lower.includes("bug")) labels.push("bug");
  if (lower.includes("feature") || lower.includes("feat")) labels.push("enhancement");
  if (lower.includes("doc") || lower.includes("documentation")) labels.push("documentation");
  if (labels.length === 0) labels.push("question");
  return labels.join(",");
}

const title = getInput("title");
const labels = suggestLabels(title);
setOutput("labels", labels);
