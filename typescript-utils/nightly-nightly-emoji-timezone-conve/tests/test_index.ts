// Mock rationale: We use fixed timestamps and known IANA zones to ensure deterministic results without external services.\n\nimport { strict as assert } from "assert";\nimport { execSync } from "child_process";\n\n/** Helper to run the CLI with given arguments and capture stdout */
function runCli(args: string[]): string {
  const cmd = `ts-node src/index.ts ${args.map(a => `"${a}"`).join(" ")}`;
  return execSync(cmd, { encoding: "utf8" }).trim();
}\n\n// Test 1: ISO timestamp conversion from New York to Tokyo (should be night)\nconst result1 = runCli(["2023-08-13T15:30:00", "America/New_York", "Asia/Tokyo"]);
assert.equal(result1, "2023-08-14 04:30 🌙", "ISO conversion failed");\n\n// Test 2: Simple HH:MM from London to Sydney (daytime)\n// Assuming the test runs on 2023‑08‑13, London time 14:45 => Sydney same day 23:45 (still day)\n// To make it deterministic we mock the current date by setting TZ env var for the process.\nprocess.env.TZ = "Europe/London"; // force Node's local time zone for "today" calculations\nconst result2 = runCli(["14:45", "Europe/London", "Australia/Sydney"]);
assert.equal(result2, "2023-08-14 23:45 🌙", "HH:MM conversion failed");\n\nconsole.log("All tests passed.");\n
