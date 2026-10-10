import { strict as assert } from "assert";
import { generateQrAscii } from "../src/index";

function testSingleChar() {
  const result = generateQrAscii("A");
  const expected = "# \n  ";
  assert.equal(result, expected, "Single character A should match expected pattern");
}

function testTwoChars() {
  const result = generateQrAscii("AB");
  const expected = "#  #\n    ";
  assert.equal(result, expected, "Characters AB should produce combined pattern");
}

testSingleChar();
testTwoChars();
console.log("All tests passed.");
