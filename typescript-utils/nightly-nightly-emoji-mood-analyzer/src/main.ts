#!/usr/bin/env node
import { readFileSync } from "fs";

/**
 * Analyze the mood of a given text and return an emoji.
 * Positive words increase the score, negative words decrease it.
 *   score > 0  => ð
 *   score < 0  => ð
 *   otherwise => ð
 */
export function analyzeMood(text: string): string {
  const positive = [
    "happy","joy","love","awesome","great","fantastic","good","wonderful","excellent","pleased","delight"
  ];
  const negative = [
    "sad","bad","terrible","hate","angry","upset","depressed","awful","horrible","pain","sorrow"
  ];
  const words = text.toLowerCase().match(/\w+/g) ?? [];
  let score = 0;
  for (const w of words) {
    if (positive.includes(w)) score++;
    if (negative.includes(w)) score--;
  }
  if (score > 0) return "ð";
  if (score < 0) return "ð";
  return "ð";
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: emoji-mood <text>");
    process.exit(1);
  }
  const input = args.join(" ");
  console.log(analyzeMood(input));
}

