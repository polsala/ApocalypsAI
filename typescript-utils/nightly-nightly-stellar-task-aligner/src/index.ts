import { Command } from 'commander';
import { Task, AlignmentType, ALIGNMENT_PRESETS, CosmicAlignmentWeights } from './types';
import { v4 as uuidv4 } from 'uuid'; // For unique task IDs

export function calculateTaskScore(task: Task, weights: CosmicAlignmentWeights): number {
  return (task.urgency * weights.urgencyWeight) +
         (task.reward * weights.rewardWeight) -
         (task.effort * weights.effortWeight);
}

export function alignTasks(tasks: Task[], alignmentType: AlignmentType): Task[] {
  const weights = ALIGNMENT_PRESETS[alignmentType];
  if (!weights) {
    throw new Error(`Unknown alignment type: ${alignmentType}`);
  }

  // Calculate scores and sort in descending order
  const scoredTasks = tasks.map(task => ({
    task,
    score: calculateTaskScore(task, weights),
  }));

  // Sort by score in descending order. If scores are equal, maintain original order (stable sort).
  scoredTasks.sort((a, b) => b.score - a.score);

  return scoredTasks.map(st => st.task);
}

// CLI setup
const program = new Command();

program
  .name('stellar-aligner')
  .description('Aligns your post-apocalyptic tasks with cosmic energies for optimal prioritization.')
  .version('1.0.0');

program
  .command('align')
  .description('Prioritize a list of tasks based on a cosmic alignment.')
  .option('-a, --alignment <type>', 'Cosmic alignment type (Aggressive, Balanced, Relaxed, Strategic)', 'Balanced')
  .requiredOption('-t, --tasks <json>', 'JSON string of tasks to align. Example: \'[{"name":"Scavenge","urgency":4,"effort":3,"reward":5}]\'')
  .action((options) => {
    try {
      const tasks: Task[] = JSON.parse(options.tasks).map((t: Omit<Task, 'id'>) => ({ ...t, id: uuidv4() }));
      const alignmentType: AlignmentType = options.alignment as AlignmentType;

      if (!Object.keys(ALIGNMENT_PRESETS).includes(alignmentType)) {
        console.error(`Error: Invalid alignment type "${alignmentType}". Choose from: ${Object.keys(ALIGNMENT_PRESETS).join(', ')}`);
        process.exit(1);
      }

      if (!Array.isArray(tasks) || tasks.some(t => !t.name || typeof t.urgency !== 'number' || typeof t.effort !== 'number' || typeof t.reward !== 'number' || t.urgency < 1 || t.urgency > 5 || t.effort < 1 || t.effort > 5 || t.reward < 1 || t.reward > 5)) {
        console.error('Error: Invalid tasks format. Each task must have name, urgency, effort, and reward (1-5).');
        process.exit(1);
      }

      const aligned = alignTasks(tasks, alignmentType);

      console.log(`\n--- Stellar Task Alignment (${alignmentType}) ---`);
      aligned.forEach((task, index) => {
        const score = calculateTaskScore(task, ALIGNMENT_PRESETS[alignmentType]);
        console.log(`${index + 1}. ${task.name} (U:${task.urgency}, E:${task.effort}, R:${task.reward}) [Score: ${score.toFixed(2)}] ${task.cosmicInfluence ? `[Influence: ${task.cosmicInfluence}]` : ''}`);
      });
      console.log('------------------------------------------');

    } catch (error: any) {
      console.error(`Error: ${error.message}`);
      process.exit(1);
    }
  });

// If running directly, parse arguments
if (require.main === module) {
  program.parse(process.argv);
}
