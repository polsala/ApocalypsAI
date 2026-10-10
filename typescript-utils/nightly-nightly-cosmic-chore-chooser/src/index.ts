import { chooseCosmicChore } from './cosmicChooser';
import { CosmicChoreConfig, CosmicChoreSuggestion } from './types';

function parseArgs(args: string[]): CosmicChoreConfig {
  const tasks: string[] = [];
  let seed: number | undefined;

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--seed' || arg === '-s') {
      if (i + 1 < args.length) {
        seed = parseInt(args[++i], 10);
        if (isNaN(seed)) {
          console.error("Error: --seed must be a number.");
          process.exit(1);
        }
      } else {
        console.error("Error: --seed requires a value.");
        process.exit(1);
      }
    } else if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    } else {
      tasks.push(arg);
    }
  }
  return { tasks, seed };
}

function printHelp() {
  console.log(`
Usage: cosmic-chore-chooser [tasks...] [--seed <number>]

A whimsical CLI tool to help you choose your next task based on "cosmic alignment".

Arguments:
  [tasks...]      A space-separated list of tasks to choose from.
                  If no tasks are provided, a default cosmic contemplation is suggested.

Options:
  --seed, -s <number>  Provide a numeric seed for deterministic cosmic alignment.
                       Useful for reproducible suggestions or if you feel a specific
                       cosmic vibration.
  --help, -h           Display this help message.

Examples:
  cosmic-chore-chooser "Scavenge for parts" "Repair the comms array" "Fortify the perimeter"
  cosmic-chore-chooser "Read ancient texts" "Meditate on the void" --seed 42
`);
}

function main() {
  const config = parseArgs(process.argv.slice(2));
  const suggestion: CosmicChoreSuggestion = chooseCosmicChore(config);

  console.log("\n✨ Cosmic Chore Suggestion ✨");
  console.log("-----------------------------");
  console.log(`Task: ${suggestion.chosenTask}`);
  console.log(`Rationale: ${suggestion.rationale}`);
  console.log(`Cosmic Alignment Score: ${suggestion.cosmicAlignmentScore}`);
  console.log("-----------------------------\n");
}

if (require.main === module) {
  main();
}
