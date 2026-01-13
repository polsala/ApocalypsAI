import { packSurvivalKit } from "../src/index";

/**
 * Tests are deterministic because the algorithm contains no randomness.
 * # Mock rationale: none needed – pure function.
 */

describe("packSurvivalKit", () => {
  test("fits within weight limit and selects optimal items", () => {
    const kit = packSurvivalKit(10);
    const totalWeight = kit.reduce((sum, i) => sum + i.weight, 0);
    expect(totalWeight).toBeLessThanOrEqual(10);
    const names = kit.map(i => i.name);
    // Expected deterministic selection based on greedy algorithm
    expect(names).toEqual([
      "Flashlight",
      "Knife",
      "Canned Food",
      "Map",
      "Water Bottle"
    ]);
  });

  test("handles small weight limits", () => {
    const kit = packSurvivalKit(2);
    const totalWeight = kit.reduce((sum, i) => sum + i.weight, 0);
    expect(totalWeight).toBeLessThanOrEqual(2);
    const names = kit.map(i => i.name);
    // With maxWeight 2, only the highest‑ratio item that fits is Flashlight (weight 1)
    expect(names).toEqual(["Flashlight"]);
  });
});

