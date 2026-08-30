import { program } from 'commander';
import { CosmicPlanner } from './cosmicPlanner';
import { defaultCosmicEvents } from './data/defaultEvents';
import { defaultAlignmentRules } from './data/defaultRules';
import { Task, CosmicEvent, AlignmentRule, TaskAlignmentResult } from './types';

// Example tasks
const defaultTasks: Task[] = [
  { description: 'Review code for new feature' },
  { description: 'Deploy to Production' },
  { description: 'Brainstorm new ideas' },
  { description: 'Update documentation' },
  { description: 'Communicate project status to stakeholders' },
  { description: 'Resource Allocation for Q4' },
  { description: 'Launch marketing campaign' },
];

program
  .version('1.0.0')
  .description('A type-safe CLI utility to plan tasks and avoid cosmic mishaps.')
  .option('-d, --date <date>', 'Specify the date for planning (YYYY-MM-DD). Defaults to today.', (value) => {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) {
      console.error('Error: Date must be in YYYY-MM-DD format.');
      process.exit(1);
    }
    return value;
  })
  .parse(process.argv);

const options = program.opts();
const targetDate = options.date || new Date().toISOString().slice(0, 10); // YYYY-MM-DD

const planner = new CosmicPlanner(defaultCosmicEvents, defaultAlignmentRules);

console.log(`\n🌌 Cosmic Alignment Report for ${targetDate} 🌌\n`);

const activeEvents = planner.getActiveEvents(targetDate);
if (activeEvents.length > 0) {
  console.log('Active Cosmic Events:');
  activeEvents.forEach(event => {
    console.log(`- ${event.name} (Impact: ${event.impacts.join(', ')})`);
  });
} else {
  console.log('No significant cosmic events detected.');
}

console.log('\nTask Alignment:');
const results: TaskAlignmentResult[] = planner.planTasks(targetDate, defaultTasks);

results.forEach(result => {
  let statusEmoji = '';
  switch (result.status) {
    case 'ALLOW':
      statusEmoji = '✅';
      break;
    case 'AVOID':
      statusEmoji = '⚠️';
      break;
    case 'RECOMMEND':
      statusEmoji = '✨';
      break;
  }
  console.log(`- Task: "${result.task.description}"`);
  console.log(`  Status: ${statusEmoji} ${result.status} (${result.reason})`);
});

console.log('\n');
