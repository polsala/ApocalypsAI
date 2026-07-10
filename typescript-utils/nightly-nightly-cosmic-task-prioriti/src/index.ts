#!/usr/bin/env node
import { Command } from 'commander';
import { prioritizeTasks, Task, PrioritizedTask } from './prioritizer';
import * as fs from 'fs';
import * as path from 'path';

const program = new Command();

program
  .name('cosmic-prioritize')
  .description('A whimsical CLI tool to prioritize tasks with cosmic urgency and assign focus constellations.')
  .version('1.0.0');

program
  .argument('[file]', 'Path to a JSON file containing tasks. If omitted, reads from stdin.')
  .option('-o, --output <file>', 'Output prioritized tasks to a JSON file.')
  .action(async (file, options) => {
    let tasks: Task[] = [];

    try {
      if (file) {
        const filePath = path.resolve(process.cwd(), file);
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        tasks = JSON.parse(fileContent);
      } else {
        // Read from stdin
        const stdinContent = await new Promise<string>((resolve) => {
          let data = '';
          process.stdin.on('data', (chunk) => data += chunk);
          process.stdin.on('end', () => resolve(data));
          if (process.stdin.isTTY) { // If not piped, prompt for input
            console.log("Enter tasks as JSON array (e.g., [{ \"id\": \"1\", \"description\": \"Task 1\" }]) and press Ctrl+D when done:");
          }
        });
        if (stdinContent.trim()) {
          tasks = JSON.parse(stdinContent);
        }
      }
    } catch (error: any) {
      console.error(`Error reading tasks: ${error.message}`);
      process.exit(1);
    }

    if (!Array.isArray(tasks) || tasks.some(t => typeof t !== 'object' || !t.id || !t.description)) {
      console.error('Invalid tasks format. Expected an array of objects with "id" and "description" properties.');
      process.exit(1);
    }

    const prioritized = prioritizeTasks(tasks);

    const outputContent = JSON.stringify(prioritized, null, 2);

    if (options.output) {
      try {
        const outputPath = path.resolve(process.cwd(), options.output);
        fs.writeFileSync(outputPath, outputContent, 'utf-8');
        console.log(`Prioritized tasks written to ${outputPath}`);
      } catch (error: any) {
        console.error(`Error writing output file: ${error.message}`);
        process.exit(1);
      }
    } else {
      console.log(outputContent);
    }
  });

program.parse(process.argv);
