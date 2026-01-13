import { generateQr } from "../src/index";

test("generateQr produces deterministic placeholder", () => {
  // Mock rationale: using simple placeholder algorithm ensures deterministic output.
  const result = generateQr("AB");
  // 'A' charCode 65 % 4 = 1 => blockMap[1] = "ââ
ââ"
  // 'B' charCode 66 % 4 = 2 => blockMap[2] = "ââ
ââ"
  const expected = "ââââ
ââââ";
  expect(result).toBe(expected);
});

