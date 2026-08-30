#!/usr/bin/env node
import { program } from 'commander';
import { processTasks } from './index';
import { UrgencyCategory, Task } from './types';

program
  .name('chrono-categorizer')
  .description('Categorize your apocalyptic tasks by temporal urgency.')
  .argument('<tasks...>', 'One or more tasks to categorize (e.g., "Fix the reactor" "Ponder the void")')
  .action((tasks: string[]) => {
    const processed = processTasks(tasks);

    console.log('Categorized Tasks:\n');

    const groupedTasks = processed.reduce((acc, task) => {
      if (!acc[task.category]) {
        acc[task.category] = [];
      }
      acc[task.category].push(task);
      return acc;
    }, {} as Record<UrgencyCategory, Task[]>);

    const categoryOrder: UrgencyCategory[] = [
      UrgencyCategory.IMMEDIATE_IMPLOSION,
      UrgencyCategory.NEAR_TERM_NUISANCE,
      UrgencyCategory.FUTURE_FOLLY,
      UrgencyCategory.COSMIC_CONTEMPLATION
    ];

    for (const category of categoryOrder) {
      if (groupedTasks[category] && groupedTasks[category].length > 0) {
        console.log(`--- ${category} ---`);
        groupedTasks[category].forEach(task => console.log(`- ${task.description}`));
        console.log('');
      }
    }
  });

program.parse(process.argv);
