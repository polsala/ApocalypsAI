import { program } from 'commander';
import { readFile, writeFile } from 'fs/promises';
import { join } from 'path';
import { Task, TaskManager } from './task-manager';

const DATA_FILE = join(process.cwd(), 'whimsical-tasks.json');

async function init() {
  program
    .name('whimsical')
    .description('Whimsical task scheduler')
    .version('1.0.0');

  program
    .command('add <name>')
    .option('--at <time>', 'Task time (HH:mm)')
    .action(async (name, { at }) => {
      const manager = await TaskManager.load(DATA_FILE);
      manager.addTask({ name, time: at });
      await manager.save(DATA_FILE);
      console.log(`Added task: ${name} at ${at}`);
    });

  program
    .command('list')
    .action(async () => {
      const manager = await TaskManager.load(DATA_FILE);
      manager.tasks.forEach((task, index) => {
        console.log(`${index + 1}. ${task.name} @ ${task.time}`);
      });
    });

  program
    .command('remove <id>')
    .action(async (id) => {
      const manager = await TaskManager.load(DATA_FILE);
      manager.removeTask(parseInt(id) - 1);
      await manager.save(DATA_FILE);
      console.log(`Removed task ${id}`);
    });

  await program.parseAsync(process.argv);
}

init();
