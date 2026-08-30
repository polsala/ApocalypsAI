import { strict as assert } from "assert";
import { hashToArt } from "../src/main";

// Mock rationale: The expected output is pre‑computed using the same
// HEX_TO_BLOCK mapping defined in the implementation. This ensures the test
// runs offline without any external dependencies.
const expectedArt = "▎■▏▇▊▁▏▂▏▏▅▋█▊▇▆▎▍▃■▉▍▍▁▋▆▆▍▊▁▂▆▍▄▌■▅■▂▌▃▌▁▌▏▃▃▋▊▂▆▊▇▋▂▆▌▁■▁▁▍▁▏";

const actualArt = hashToArt("test");
assert.equal(actualArt, expectedArt, "hashToArt('test') should produce the expected ASCII art representation");

console.log("All tests passed.");
