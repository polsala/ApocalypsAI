import { strict as assert } from "assert";
import { generateQuestSchedule } from "../src/questScheduler";

// Mock random generator that yields a predefined sequence of numbers
function* mockRandomGenerator(values: number[]) {
  let i = 0;
  while (true) {
    yield values[i % values.length];
    i++;
  }
}
const mockRandom = (() => {
  const gen = mockRandomGenerator([0.0, 0.7]); // indices 0 (Mysterious) and 5 (Radiant)
  return () => gen.next().value as number;
})();

const tasks = ["Find the sword", "Defeat the dragon"];
const startDate = "2023-01-01";

const expected = `# Epic Quest Itinerary\n\n## Day 1: 2023-01-01 – Mysterious Find the sword\n\n## Day 2: 2023-01-02 – Radiant Defeat the dragon\n\n`;

const output = generateQuestSchedule(tasks, startDate, mockRandom);
assert.equal(output, expected);
console.log("All tests passed");
