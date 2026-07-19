import { generateSkullQR } from "../src/index";
import assert from "assert";

// Mock rationale: we use a fixed input and compare against the exact expected ASCII art.
const result = generateSkullQR("AB");
const expected = "  ☠☠\n  ☠☠";
assert.strictEqual(result, expected);
console.log("test passed");
