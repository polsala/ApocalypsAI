import { encodeToAsciiArt } from "../src/main";
import assert from "assert";

function testSingleCharacter() {
  // "A" => char code 65 => binary 01000001 => " #    #"
  const result = encodeToAsciiArt("A");
  const expected = [" #    #"];
  assert.deepStrictEqual(result, expected, "Encoding of 'A' failed");
}

function testMultipleCharacters() {
  // "AB" => [" #    #", " #   # "]
  const result = encodeToAsciiArt("AB");
  const expected = [" #    #", " #   # "];
  assert.deepStrictEqual(result, expected, "Encoding of 'AB' failed");
}

function runAll() {
  testSingleCharacter();
  testMultipleCharacters();
  console.log("All tests passed.");
}

runAll();
