import { CosmicTask } from './types';
import { cosmicTasks } from './tasks';

/**
 * Generates a numeric hash from a string seed.
 * @param seed The string to hash.
 * @returns A non-negative integer hash.
 */
function generateHash(seed: string): number {
  let hash = 0;
  for (let i = 0; i < seed.length; i++) {
    const char = seed.charCodeAt(i);
    hash = ((hash << 5) - hash) + char; // Simple hash function
    hash |= 0; // Convert to 32bit integer
  }
  return Math.abs(hash); // Ensure non-negative
}

/**
 * Selects a "cosmically aligned" task based on a seed.
 * @param seed The input seed (e.g., current time, mood, a random string).
 * @param tasks The list of available tasks.
 * @returns A selected CosmicTask.
 * @throws Error if no tasks are provided.
 */
export function alignTask(seed: string, tasks: CosmicTask[]): CosmicTask {
  if (tasks.length === 0) {
    throw new Error("No cosmic tasks available for alignment.");
  }

  const hash = generateHash(seed);
  const index = hash % tasks.length;
  return tasks[index];
}

/**
 * Gets a default seed based on current time.
 * @returns A string representing the current date and time.
 */
export function getDefaultSeed(): string {
  // # Mock rationale: This function uses Date.now() which is non-deterministic.
  // # For tests, this function will be mocked to return a fixed string.
  return new Date().toISOString();
}

/**
 * Main function to run the task alignment.
 * @param seed Optional seed string. If not provided, a default seed is used.
 * @param taskList Optional list of tasks. Defaults to `cosmicTasks`.
 * @returns The selected task.
 */
export function runAlignment(seed?: string, taskList: CosmicTask[] = cosmicTasks): CosmicTask {
  const effectiveSeed = seed || getDefaultSeed();
  const selectedTask = alignTask(effectiveSeed, taskList);
  return selectedTask;
}
