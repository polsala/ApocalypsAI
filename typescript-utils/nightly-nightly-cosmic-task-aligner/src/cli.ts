#!/usr/bin/env node
import { runAlignment } from './index';
import { CosmicTask } from './types';
import { cosmicTasks } from './tasks'; // Import for default tasks

function parseArgs(args: string[]): { seed?: string; help: boolean } {
  let seed: string | undefined;
  let help = false;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--seed' || arg === '-s') {
      seed = args[++i];
    } else if (arg === '--help' || arg === '-h') {
      help = true;
    }
  }
  return { seed, help };
}

function displayHelp() {
  console.log(`\nCosmic Task Aligner\n\nA whimsical CLI tool to help you pick a task when overwhelmed.\nIt suggests a "cosmically aligned" task based on a seed.\n\nUsage:\n  cosmic-align [options]\n\nOptions:\n  -s, --seed <string>  Provide a custom seed for task alignment.\n                       (e.g., your current mood, a favorite word, a number)\n                       If not provided, the current date/time is used.\n  -h, --help           Display this help message.\n\nExamples:\n  cosmic-align\n  cosmic-align --seed "feeling productive"\n  cosmic-align -s "monday morning vibes"\n`);
}

async function main() {
  const { seed, help } = parseArgs(process.argv.slice(2));

  if (help) {
    displayHelp();
    process.exit(0);
  }

  try {
    const selectedTask: CosmicTask = runAlignment(seed, cosmicTasks); // Pass default tasks explicitly
    console.log("\n✨ Your Cosmic Alignment for today ✨");
    console.log(`------------------------------------`);
    console.log(`Task: ${selectedTask.description}`);
    console.log(`Guidance: ${selectedTask.alignmentMessage}`);
    console.log(`Tags: ${selectedTask.tags.join(', ')}`);
    console.log(`------------------------------------`);
    console.log(`\nMay your path be clear and your energy aligned!`);
  } catch (error: any) {
    console.error(`\n🌌 Cosmic disturbance detected: ${error.message}`);
    process.exit(1);
  }
}

main();
