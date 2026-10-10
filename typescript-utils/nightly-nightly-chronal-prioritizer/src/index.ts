import { Task, PrioritizedTask } from './task';

const URGENCY_WEIGHT = 3;
const IMPORTANCE_WEIGHT = 2;
const WHIMSY_WEIGHT = 1;

/**
 * Prioritizes a list of tasks based on urgency, importance, and a whimsical factor.
 * @param tasks An array of Task objects.
 * @returns An array of PrioritizedTask objects, sorted by priorityScore in descending order.
 */
export function prioritizeTasks(tasks: Task[]): PrioritizedTask[] {
  const prioritized = tasks.map(task => {
    const whimsy = task.whimsyFactor !== undefined ? task.whimsyFactor : 0.5;
    // Introduce a "temporal distortion" for whimsy, mocked for deterministic tests
    const temporalDistortion = Math.random() * 0.5 + 0.75; // Random factor between 0.75 and 1.25

    const priorityScore =
      (task.urgency * URGENCY_WEIGHT) +
      (task.importance * IMPORTANCE_WEIGHT) +
      (whimsy * WHIMSY_WEIGHT * temporalDistortion);

    return { ...task, priorityScore };
  });

  return prioritized.sort((a, b) => b.priorityScore - a.priorityScore);
}

// CLI logic (simplified for a standalone utility)
// This part would typically use a library like 'commander' or 'yargs' for robust CLI parsing.
// For this self-contained utility, we'll simulate basic input.
if (require.main === module) {
  // Example usage if run directly
  const exampleTasks: Task[] = [
    { name: 'Calibrate Chronometer', urgency: 5, importance: 5, whimsyFactor: 0.1 },
    { name: 'Polish Temporal Lenses', urgency: 3, importance: 4, whimsyFactor: 0.8 },
    { name: 'Gather Quantum Dust', urgency: 2, importance: 3, whimsyFactor: 0.9 },
    { name: 'Re-align Reality Flux', urgency: 4, importance: 5, whimsyFactor: 0.3 },
    { name: 'Brew Cosmic Tea', urgency: 1, importance: 2, whimsyFactor: 1.0 },
    { name: 'Inspect Time-Space Fabric', urgency: 4, importance: 4 }, // No whimsyFactor
  ];

  console.log("--- Unprioritized Tasks ---");
  exampleTasks.forEach(task => console.log(`- ${task.name} (U:${task.urgency}, I:${task.importance}, W:${task.whimsyFactor || '0.5'})`));

  const prioritized = prioritizeTasks(exampleTasks);

  console.log("\n--- Chronally Prioritized Tasks ---");
  prioritized.forEach((task, index) => {
    console.log(`${index + 1}. ${task.name} (Score: ${task.priorityScore.toFixed(2)})`);
  });
}
