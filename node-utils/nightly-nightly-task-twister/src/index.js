#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const defaultTasksPath = path.join(__dirname, 'tasks.json');

/**
 * Loads tasks from a specified JSON file.
 * @param {string} filePath - The path to the JSON file containing tasks.
 * @returns {string[]} An array of tasks (strings), or an empty array if loading fails.
 */
function loadTasks(filePath) {
  try {
    const rawData = fs.readFileSync(filePath, 'utf8');
    const tasks = JSON.parse(rawData);
    if (!Array.isArray(tasks) || tasks.some(t => typeof t !== 'string')) {
      throw new Error('Task file must contain an array of strings.');
    }
    return tasks;
  } catch (error) {
    if (error.code === 'ENOENT') {
      console.error(`\nError: Task file not found at ${filePath}`);
    } else if (error instanceof SyntaxError) {
      console.error(`\nError: Invalid JSON in task file at ${filePath}`);
    } else {
      console.error(`\nError loading tasks from ${filePath}: ${error.message}`);
    }
    return [];
  }
}

/**
 * Selects a random task from a given list.
 * @param {string[]} tasks - An array of tasks.
 * @returns {string} A randomly chosen task, or a default message if the list is empty.
 */
function getRandomTask(tasks) {
  if (tasks.length === 0) {
    return "No tasks available. Perhaps it's time for a coffee break?";
  }
  const randomIndex = Math.floor(Math.random() * tasks.length);
  return tasks[randomIndex];
}

/**
 * Main function to execute the CLI utility.
 */
function main() {
  let tasks = loadTasks(defaultTasksPath);

  // Simple CLI argument parsing for --file
  const args = process.argv.slice(2);
  const fileArgIndex = args.indexOf('--file');
  if (fileArgIndex !== -1 && args[fileArgIndex + 1]) {
    const customFilePath = path.resolve(process.cwd(), args[fileArgIndex + 1]);
    const customTasks = loadTasks(customFilePath);
    if (customTasks.length > 0) {
      tasks = customTasks; // Override with custom tasks if valid and non-empty
    } else {
      console.warn("\nWarning: Custom task file was empty or invalid. Using default tasks.\n");
    }
  }

  const chosenTask = getRandomTask(tasks);
  console.log("\n✨ The ApocalypsAI Nightly Integrator's Task Twister reveals your destiny: ✨");
  console.log(`\n  ➡️  ${chosenTask}\n`);
  console.log("May your code be bug-free and your commits meaningful. Happy hacking!\n");
}

// Only run main if this file is executed directly
if (require.main === module) {
  main();
}

// Export for testing
module.exports = { loadTasks, getRandomTask, main };
