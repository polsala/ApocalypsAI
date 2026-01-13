import { hashArt } from "../src/main";
import assert from "assert";

// Expected output for the input "test" (SHAâ256 hash: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08)
const expected = `ââââââââââ  ââââ
ââââââââââââââââ
ââââââââââââââ  
ââââââââââ  ââââ
ââââââââââââââââ
ââââ  ââââââââââ
ââââââââââââââââ
ââ  ââ  ââ  ââ`;

const result = hashArt("test");
assert.strictEqual(result, expected, "hashArt output does not match expected art for input 'test'");

console.log("All tests passed.");

