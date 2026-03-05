#!/usr/bin/env node

const { selectWeightedTask, getCosmicAlignment, getCosmicIntroduction, getCosmicConclusion } = require('./weaver');
const fs = require('fs');
const path = require('path');

function parseArgs(args) {
  const options = {
    tasks: [],
    file: null,
    alignment: false,
    count: 1
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '-f' || arg === '--file') {
      options.file = args[++i];
    } else if (arg === '-a' || arg === '--alignment') {
      options.alignment = true;
    } else if (arg === '-c' || arg === '--count') {
      options.count = parseInt(args[++i], 10);
      if (isNaN(options.count) || options.count < 1) {
        console.error("Error: --count must be a positive integer.");
        process.exit(1);
      }
    } else if (arg.startsWith('-')) {
      console.error(`Error: Unknown option '${arg}'`);
      process.exit(1);
    } else {
      // Assume remaining args are tasks
      options.tasks.push(arg);
    }
  }
  return options;
}

function loadTasksFromFile(filePath) {
  try {
    const fullPath = path.resolve(process.cwd(), filePath);
    const content = fs.readFileSync(fullPath, 'utf8');
    const parsed = JSON.parse(content);
    if (!Array.isArray(parsed)) {
      console.error("Error: Task file must contain a JSON array of tasks.");
      process.exit(1);
    }
    return parsed.map(task => {
      if (typeof task === 'string') {
        return { name: task, weight: 1 };
      } else if (typeof task === 'object' && task !== null && typeof task.name === 'string' && (typeof task.weight === 'number' || task.weight === undefined)) {
        return { name: task.name, weight: task.weight || 1 };
      } else {
        console.warn(`Warning: Invalid task format in file: ${JSON.stringify(task)}. Skipping.`);
        return null;
      }
    }).filter(Boolean);
  } catch (error) {
    console.error(`Error reading or parsing task file '${filePath}': ${error.message}`);
    process.exit(1);
  }
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  let tasks = [];

  if (options.file) {
    tasks = loadTasksFromFile(options.file);
  } else if (options.tasks.length > 0) {
    tasks = options.tasks.map(task => {
      const parts = task.split(':');
      const name = parts[0];
      const weight = parts.length > 1 ? parseFloat(parts[1]) : 1;
      if (isNaN(weight) || weight <= 0) {
        console.warn(`Warning: Invalid weight for task '${name}'. Using default weight 1.`);
        return { name, weight: 1 };
      }
      return { name, weight };
    });
  }

  if (tasks.length === 0) {
    console.log("No tasks provided. Use 'cosmic-weaver <task1> <task2>' or 'cosmic-weaver -f <file.json>'.");
    process.exit(0);
  }

  console.log(getCosmicIntroduction());
  if (options.alignment) {
    console.log(`\n${getCosmicAlignment()}\n`);
  }

  const selectedTasks = new Set();
  for (let i = 0; i < options.count; i++) {
    let selectedTask = null;
    let attempts = 0;
    const maxAttempts = tasks.length * 2; // Prevent infinite loops if all tasks are already selected

    // Try to select a unique task if count > 1
    while (selectedTask === null || (options.count > 1 && selectedTasks.has(selectedTask))) {
      selectedTask = selectWeightedTask(tasks);
      attempts++;
      if (attempts > maxAttempts) {
        // Fallback: if we can't find unique tasks after many attempts, just pick one.
        // This can happen if tasks.length is small and count is large.
        selectedTask = selectWeightedTask(tasks);
        break;
      }
    }
    if (selectedTask) {
      selectedTasks.add(selectedTask);
    }
  }

  console.log("\nThe cosmic dice have rolled, revealing your path:");
  selectedTasks.forEach((task, index) => {
    console.log(`  ${index + 1}. ${task}`);
  });

  console.log(`\n${getCosmicConclusion()}`);
}

if (require.main === module) {
  main();
}
