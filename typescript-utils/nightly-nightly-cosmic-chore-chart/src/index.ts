import { Task, CosmicFactor, PrioritizedTask } from './types';

/**
 * Calculates the cosmic priority score for a single task.
 * @param task The task to evaluate.
 * @param cosmicFactors An array of current cosmic factors.
 * @returns The calculated cosmic priority score.
 */
export function calculateCosmicPriority(task: Task, cosmicFactors: CosmicFactor[]): number {
  let score = task.basePriority;

  for (const factor of cosmicFactors) {
    const taskSpecificModifier = task.cosmicModifiers?.[factor.name] ?? 1; // Default to 1 if not specified
    score += factor.value * factor.impactMultiplier * taskSpecificModifier;
  }

  return score;
}

/**
 * Prioritizes a list of tasks based on cosmic factors.
 * @param tasks An array of tasks to prioritize.
 * @param cosmicFactors An array of current cosmic factors.
 * @returns A new array of tasks, sorted by cosmic priority score (highest first).
 */
export function prioritizeTasks(tasks: Task[], cosmicFactors: CosmicFactor[]): PrioritizedTask[] {
  const prioritized = tasks.map(task => ({
    ...task,
    cosmicPriorityScore: calculateCosmicPriority(task, cosmicFactors)
  }));

  // Sort in descending order of cosmicPriorityScore (higher score = more urgent)
  return prioritized.sort((a, b) => b.cosmicPriorityScore - a.cosmicPriorityScore);
}

// Example Usage (for CLI or direct execution)
if (require.main === module) {
  const exampleCosmicFactors: CosmicFactor[] = [
    { name: 'LunarAlignment', value: 0.8, impactMultiplier: 2 }, // High impact
    { name: 'SolarFlareActivity', value: 0.2, impactMultiplier: 5 }, // Moderate impact
    { name: 'NebulaDrift', value: 0.1, impactMultiplier: -1 }, // Slightly reduces urgency
    { name: 'VoidWhisperIntensity', value: 0.9, impactMultiplier: 3 } // Very high impact
  ];

  const exampleTasks: Task[] = [
    {
      id: 'task-001',
      name: 'Stabilize Temporal Flux Capacitor',
      basePriority: 10,
      cosmicModifiers: {
        'LunarAlignment': 1.5, // More affected by lunar alignment
        'VoidWhisperIntensity': 2.0 // Doubly affected by void whispers
      },
      description: 'Critical system maintenance.'
    },
    {
      id: 'task-002',
      name: 'Recalibrate Chrono-Synthesizer',
      basePriority: 7,
      cosmicModifiers: {
        'SolarFlareActivity': 0.5 // Less affected by solar flares
      },
      description: 'Routine calibration for time travel.'
    },
    {
      id: 'task-003',
      name: 'Inventory Ration Supplies',
      basePriority: 5,
      description: 'Check food and water reserves.'
    },
    {
      id: 'task-004',
      name: 'Decode Ancient Alien Broadcast',
      basePriority: 3,
      cosmicModifiers: {
        'NebulaDrift': 0.5 // Less affected by nebula drift
      },
      description: 'Ongoing research project.'
    }
  ];

  console.log('--- Current Cosmic Factors ---');
  exampleCosmicFactors.forEach(f => console.log(`- ${f.name}: Value=${f.value}, Multiplier=${f.impactMultiplier}`));
  console.log('\n--- Unprioritized Tasks ---');
  exampleTasks.forEach(task => console.log(`- ${task.name} (Base Priority: ${task.basePriority})`));

  const prioritized = prioritizeTasks(exampleTasks, exampleCosmicFactors);

  console.log('\n--- Prioritized Cosmic Chore Chart ---');
  prioritized.forEach((task, index) => {
    console.log(`${index + 1}. ${task.name}`);
    console.log(`   ID: ${task.id}`);
    console.log(`   Description: ${task.description}`);
    console.log(`   Base Priority: ${task.basePriority}`);
    console.log(`   Cosmic Priority Score: ${task.cosmicPriorityScore.toFixed(2)}`);
    console.log('---');
  });
}
