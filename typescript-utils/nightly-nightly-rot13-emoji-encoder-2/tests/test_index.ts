import { rot13, toEmoji } from "../src/index";
\ndescribe("rot13", () => {
  test("basic transformation", () => {
    expect(rot13("Hello")).toBe("Uryyb");
    expect(rot13("Apocalypse")).toBe("Ncpnfbcr");
  });
});
\ndescribe("toEmoji", () => {
  test("maps letters to emojis after ROT13", () => {
    const result = toEmoji("Uryyb");
    // Expected emojis: 🤩😚😑😑😁
    expect(result).toBe("🤩😚😑😑😁");
  });
\n  test("leaves non‑alphabetic characters untouched", () => {
    expect(toEmoji("123! ?")).toBe("123! ?");
  });
});
\ndescribe("full pipeline", () => {
  test("rot13 then emoji conversion yields expected output", () => {
    const input = "Hello";
    const output = toEmoji(rot13(input));
    expect(output).toBe("🤩😚😑😑😁");
  });
});
