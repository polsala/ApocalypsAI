import * as fs from 'fs';
import * as path from 'path';
import { Task, PrioritizedTask } from './types';
import { prioritizeTasks } from './taskOracle';

function parseTasks(args: string[]): Task[] {
  const tasks: Task[] = [];
  let fileMode = false;
  let filePath = '';

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--file') {
      fileMode = true;
      filePath = args[++i]; // Get the next argument as the file path
      break;
    } else {
      tasks.push({ id: `task-${i + 1}`, description: arg });
    }
  }

  if (fileMode && filePath) {
    try {
      const fileContent = fs.readFileSync(path.resolve(process.cwd(), filePath), 'utf8');
      const fileTasks = fileContent.split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0 && !line.startsWith('#')) // Ignore empty lines and comments
        .map((description, index) => ({ id: `file-task-${index + 1}`, description }));
      return fileTasks;
    } catch (error: any) {
      console.error(`Error reading file ${filePath}: ${error.message}`);
      process.exit(1);
    }
  }

  return tasks;
}

function displayResult(prioritizedTask: PrioritizedTask) {
  console.log('\n✨ The Cosmic Task Oracle has spoken! ✨\n');
  console.log('Your next task, aligned with the cosmos, is:');
  console.log('------------------------------------------');
  console.log(`Task: ${prioritizedTask.description}`);
  console.log(`Cosmic Score: ${prioritizedTask.cosmicScore}`);
  console.log(`Rationale: ${prioritizedTask.rationale}`);
  console.log('------------------------------------------');
  console.log('May your efforts be cosmically productive!\n');
}

export async function main() {
  const args = process.argv.slice(2); // Remove 'node' and 'index.ts'

  if (args.length === 0) {
    console.log('Usage: npm start "Task 1" "Task 2" ...');
    console.log('Or:    npm start -- --file <path/to/tasks.txt>');
    process.exit(0);
  }

  const tasks = parseTasks(args);

  if (tasks.length === 0) {
    console.log('No tasks provided to the Cosmic Task Oracle. What shall I prioritize?');
    process.exit(0);
  }

  const prioritized = prioritizeTasks(tasks);

  if (prioritized.length > 0) {
    displayResult(prioritized[0]);
  } else {
    console.log('The oracle pondered, but found no tasks to prioritize.');
  }
}

if (require.main === module) {
  main();
}
