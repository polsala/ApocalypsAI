import {getKit} from "../src/kit.js";

describe("getKit", () => {
  test("returns correct items for Desert", () => {
    const kit = getKit("Desert");
    expect(kit).toContain("Sun hat");
    expect(kit.length).toBe(5);
  });

  test("returns empty array for unknown environment", () => {
    expect(getKit("Space")).toEqual([]);
  });
});
