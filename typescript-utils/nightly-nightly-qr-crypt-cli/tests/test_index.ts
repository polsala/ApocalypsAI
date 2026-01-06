// tests/test_index.ts
import { strict as assert } from "assert";
import { generateQr } from "../src/index";

// Mock rationale: generateQr uses only pure functions, no external I/O, so the tests are fully deterministic.

// Basic Caesar shift tests
assert.equal(generateQr("abc", 1), "QR:bcd");
assert.equal(generateQr("ABC", 2), "QR:CDE");
assert.equal(generateQr("xyz", 2), "QR:zab");
assert.equal(generateQr("Hello, World!", 5), "QR:Mjqqt, Btwqi!");

// Default shift (should be 1)
assert.equal(generateQr("test", undefined as any), "QR:uftu");

console.log("All tests passed.");
