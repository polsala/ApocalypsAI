import { readFileSync } from 'fs';
import { alignTasks } from './taskAligner';
import { Task } from './types';

function printHelp() {
  console.log('Usage: ts-node src/index.ts <path_to_tasks.json>');
  console.log('  <path_to_tasks.json> - Path to a JSON file containing an array of tasks.');
  console.log('\nExample tasks.json:');
  console.log('[
  {\n    "id": "task1",\n    "name": "Defuse temporal anomaly",\n    "urgency": 5,\n    "energyCost": 4\n  },\n  {\n    "id": "task2",\n    "name": "Gather cosmic dust",\n    "urgency": 2,\n    "energyCost": 1\n  }\n]');
}

function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    printHelp();
    process.exit(0);
  }

  const filePath = args[0];

  try {
    const fileContent = readFileSync(filePath, 'utf-8');
    const tasks: Task[] = JSON.parse(fileContent);

    if (!Array.isArray(tasks) || !tasks.every(t => typeof t.id === 'string' && typeof t.name === 'string' && typeof t.urgency === 'number' && typeof t.energyCost === 'number')) {
      console.error('Error: Invalid tasks.json format. Expected an array of tasks with id, name, urgency, and energyCost.');
      process.exit(1);
    }

    console.log('--- Original Tasks ---');
    tasks.forEach(task => console.log(`- ${task.name} (Urgency: ${task.urgency}, Energy: ${task.energyCost})`));
    console.log('\nConsulting the Temporal Alignment Matrix...\n');

    const alignedTasks = alignTasks(tasks);

    console.log('--- Aligned Tasks (Recommended Order) ---');
    alignedTasks.forEach((task, index) => {
      console.log(`${index + 1}. ${task.name} (Urgency: ${task.urgency}, Energy: ${task.energyCost}, Temporal Alignment: ${task.temporalAlignment?.toFixed(2)})`);
    });

  } catch (error: any) {
    if (error.code === 'ENOENT') {
      console.error(`Error: File not found at '${filePath}'`);
    } else if (error instanceof SyntaxError) {
      console.error(`Error: Invalid JSON in '${filePath}': ${error.message}`);
    } else {
      console.error(`An unexpected error occurred: ${error.message}`);
    }
    process.exit(1);
  }
}

main();
