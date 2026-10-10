#!/usr/bin/env node
import { generateWhisper } from './generator';
import { WhisperCategory } from './types';

/**
 * Runs the CLI application to generate and display a cosmic whisper.
 * Parses command-line arguments for an optional category.
 */
function run() {
  const args = process.argv.slice(2);
  const categoryInput = args[0] as WhisperCategory | undefined;

  const validCategories: WhisperCategory[] = ["Resource", "Shelter", "Social", "Exploration", "Self-Care", "Wildcard"];

  if (categoryInput && !validCategories.includes(categoryInput)) {
    console.error(`Error: Invalid category "${categoryInput}".`);
    console.error(`Available categories: ${validCategories.join(", ")}`);
    process.exit(1);
  }

  try {
    const whisper = generateWhisper(categoryInput);
    console.log(`\n--- Cosmic Whisper Oracle ---\n`);
    console.log(`Category: ${whisper.category}`);
    console.log(`Prompt: ${whisper.prompt}`);
    console.log(`Action: ${whisper.action}`);
    console.log(`Risk Level: ${whisper.risk}`);
    console.log(`Timestamp: ${new Date(whisper.timestamp).toLocaleString()}`);
    console.log(`\n-----------------------------\n`);
  } catch (error: any) {
    console.error(`An error occurred: ${error.message}`);
    process.exit(1);
  }
}

run();
