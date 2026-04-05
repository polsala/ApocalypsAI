import { Task } from './types';

// Weights for calculation
const URGENCY_WEIGHT = 3;
const ENERGY_BENEFIT_WEIGHT = 2; // Higher benefit for lower energy cost
const COSMIC_ALIGNMENT_WEIGHT = 1;

/**
 * Calculates the temporal alignment score for a given task.
 * @param task The task to calculate the score for.
 * @param randomFactor A random number (e.g., 0-10) to introduce whimsy.
 * @returns The calculated temporal alignment score.
 */
export function calculateTemporalAlignment(task: Task, randomFactor: number): number {
  // Invert energy cost: 1 (low energy) -> 5, 5 (high energy) -> 1
  const energyBenefit = 6 - task.energyCost;

  return (task.urgency * URGENCY_WEIGHT) +
         (energyBenefit * ENERGY_BENEFIT_WEIGHT) +
         (randomFactor * COSMIC_ALIGNMENT_WEIGHT);
}

/**
 * Aligns a list of tasks based on their calculated temporal alignment scores.
 * Tasks with higher scores are considered more aligned and come first.
 * @param tasks An array of tasks to align.
 * @param randomGenerator A function that generates a random number (default: Math.random).
 * @returns A new array of tasks, sorted by temporal alignment in descending order.
 */
export function alignTasks(tasks: Task[], randomGenerator: () => number = Math.random): Task[] {
  if (!tasks || tasks.length === 0) {
    return [];
  }

  return tasks
    .map(task => {
      // Scale random factor for more impact, e.g., 0-10
      const temporalAlignment = calculateTemporalAlignment(task, randomGenerator() * 10);
      return { ...task, temporalAlignment };
    })
    .sort((a, b) => (b.temporalAlignment || 0) - (a.temporalAlignment || 0));
}
