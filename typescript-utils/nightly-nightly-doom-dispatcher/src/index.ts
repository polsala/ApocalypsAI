import * as readline from 'readline';

// Define Doom Levels and their associated scores for prioritization
enum DoomLevel {
  MinorGlitch = 1,
  ImpendingCatastrophe = 2,
  ExistentialThreat = 3,
}

// Define Whimsy Bonuses and their associated scores
enum WhimsyBonus {
  FaintSparkle = 1,
  GentleGiggle = 2,
  CosmicJoke = 3,
}

interface PrioritizedTask {
  task: string;
  doomLevel: DoomLevel;
  whimsyBonus: WhimsyBonus;
  score: number;
}

/**
 * Randomly assigns a Doom Level and Whimsy Bonus to a given task.
 * @param task The task string.
 * @returns A PrioritizedTask object with assigned levels and a calculated score.
 */
export function assignDoomAndWhimsy(task: string): PrioritizedTask {
  const doomLevels = Object.values(DoomLevel).filter(v => typeof v === 'number') as DoomLevel[];
  const whimsyBonuses = Object.values(WhimsyBonus).filter(v => typeof v === 'number') as WhimsyBonus[];

  const randomDoomIndex = Math.floor(Math.random() * doomLevels.length);
  const randomWhimsyIndex = Math.floor(Math.random() * whimsyBonuses.length);

  const doomLevel = doomLevels[randomDoomIndex];
  const whimsyBonus = whimsyBonuses[randomWhimsyIndex];

  // Calculate score: Higher doom is worse, higher whimsy is better (but doom dominates)
  // We want higher doom to be higher priority, so we use its raw value.
  // Whimsy adds a secondary sorting factor, making tasks with the same doom level
  // sorted by whimsy (higher whimsy first for a bit of fun).
  const score = doomLevel * 10 + whimsyBonus; // Doom has a higher weight

  return {
    task,
    doomLevel,
    whimsyBonus,
    score,
  };
}

/**
 * Converts an enum value to its string representation.
 * @param enumType The enum type (e.g., DoomLevel).
 * @param value The numeric enum value.
 * @returns The string name of the enum value.
 */
function getEnumName<T extends object>(enumType: T, value: number): string {
  const name = Object.keys(enumType).find(key => enumType[key as keyof T] === value);
  return name || String(value);
}

/**
 * Main function to process tasks and print prioritized list.
 * @param tasks An array of task strings.
 */
export function dispatchTasks(tasks: string[]): void {
  if (tasks.length === 0) {
    console.log("No tasks provided. The apocalypse awaits your input!");
    return;
  }

  const prioritizedTasks = tasks
    .map(assignDoomAndWhimsy)
    .sort((a, b) => {
      // Primary sort: Higher score (more doom) comes first
      if (b.score !== a.score) {
        return b.score - a.score;
      }
      // Secondary sort: If scores are equal, sort by whimsy (higher whimsy first)
      return b.whimsyBonus - a.whimsyBonus;
    });

  console.log("\n--- Daily Doom Dispatch ---\n");
  prioritizedTasks.forEach((pTask, index) => {
    const doomName = getEnumName(DoomLevel, pTask.doomLevel);
    const whimsyName = getEnumName(WhimsyBonus, pTask.whimsyBonus);
    console.log(`${index + 1}. [${doomName.replace(/([A-Z])/g, ' $1').trim()} + ${whimsyName.replace(/([A-Z])/g, ' $1').trim()}] ${pTask.task}`);
  });
  console.log("\nMay your efforts avert total annihilation... or at least make it amusing.\n");
}

// Entry point for the CLI
async function main() {
  let tasks: string[] = [];

  // Check if tasks are provided as command-line arguments
  if (process.argv.length > 2) {
    tasks = process.argv.slice(2);
    dispatchTasks(tasks);
  } else {
    // If no arguments, read from stdin
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      terminal: false
    });

    rl.on('line', (line) => {
      const trimmedLine = line.trim();
      if (trimmedLine) {
        tasks.push(trimmedLine);
      }
    });

    rl.on('close', () => {
      dispatchTasks(tasks);
    });

    // If stdin is not a TTY and no data is piped, it might just close immediately.
    // This handles cases where the script is run without args and without piping.
    if (process.stdin.isTTY) {
      console.log("Enter tasks one per line, press Ctrl+D (or Ctrl+Z then Enter on Windows) when done:");
    }
  }
}

if (require.main === module) {
  main();
}
