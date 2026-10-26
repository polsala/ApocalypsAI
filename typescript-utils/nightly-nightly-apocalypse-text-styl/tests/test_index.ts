import { stylize } from "../src/index";

function assertEqual(actual: string, expected: string): void {
  if (actual !== expected) {
    throw new Error(`Expected "${expected}", got "${actual}"`);
  }
}

// Basic mapping test
assertEqual(stylize("abc"), "αβ¢");

// Case preservation test
assertEqual(stylize("AbC"), "Αβ¢");

// Space replacement test
assertEqual(stylize("a b"), "α ☢ β");

// Full sentence test
assertEqual(stylize("Hello World"), "Нεℓℓο ☢ Ωοяℓδ");
