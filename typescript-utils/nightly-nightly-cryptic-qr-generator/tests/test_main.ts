import { generateQR } from "../src/main";

// Mock rationale: No external dependencies, deterministic mapping based on char codes.

describe("generateQR", () => {
  test("produces expected pattern for 'AB'", () => {
    const result = generateQR("AB");
    const expected = "@@..\n..**";
    expect(result).toBe(expected);
  });

  test("handles empty string", () => {
    const result = generateQR("");
    const expected = "\n"; // two empty rows joined by newline
    expect(result).toBe(expected);
  });
});
