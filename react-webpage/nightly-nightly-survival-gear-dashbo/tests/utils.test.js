import { computeTotalWeight } from "../src/utils";

test("computeTotalWeight sums weights correctly", () => {
  const items = [
    { name: "Rope", weight: 2.5, durability: 80 },
    { name: "Water Bottle", weight: 1.2, durability: 100 },
    { name: "Tent", weight: 5.0, durability: 70 },
  ];
  const total = computeTotalWeight(items);
  expect(total).toBeCloseTo(8.7);
});
