import { generateQrAscii } from "../src/qr";

const expected = `+------+\n|######|\n|######|\n|######|\n+------+`;

if (generateQrAscii("test") !== expected) {
  console.error("Test failed for input 'test'");
  process.exit(1);
} else {
  console.log("All tests passed");
  process.exit(0);
}
