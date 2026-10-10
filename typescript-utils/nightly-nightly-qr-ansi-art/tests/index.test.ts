import { generate } from "../src/index";
import assert from "assert";

function normalize(str: string): string {
  return str.trim().replace(/\r\n/g, "\n");
}

// Test for single character 'A' (ASCII 65 -> 01000001)
const expectedA = " █    █";
assert.strictEqual(normalize(generate("A")), expectedA);

// Test for string "AB"
// 'B' is ASCII 66 -> 01000010 => " █   █ "
const expectedAB = " █    █\n █   █ ";
assert.strictEqual(normalize(generate("AB")), expectedAB);
