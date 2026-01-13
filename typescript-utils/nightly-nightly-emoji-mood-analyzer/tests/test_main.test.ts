import { analyzeMood } from "../src/main";

function assertEqual(actual: any, expected: any, msg: string): void {
  if (actual !== expected) {
    throw new Error(`${msg}: expected ${expected}, got ${actual}`);
  }
}

// Positive mood test
assertEqual(analyzeMood("I am feeling happy and wonderful today!"), "ð", "Positive mood");

// Negative mood test
assertEqual(analyzeMood("It was a terrible, horrible day."), "ð", "Negative mood");

// Neutral mood test
assertEqual(analyzeMood("The sky is blue."), "ð", "Neutral mood");

console.log("All tests passed.");

