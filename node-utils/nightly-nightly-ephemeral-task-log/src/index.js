#!/usr/bin/env node

const { addTask, listTasks, forgetTask } = require('./taskManager');

async function main() {
    const args = process.argv.slice(2);
    const command = args[0];

    switch (command) {
        case 'add':
            const description = args.slice(1).join(' ');
            if (!description) {
                console.error('Error: Please provide a description for the task.');
                process.exit(1);
            }
            const id = await addTask(description);
            console.log(`Ephemeral task added with ID: ${id}`);
            break;
        case 'list':
            const tasks = await listTasks();
            if (tasks.length === 0) {
                console.log('No ephemeral tasks currently lingering.');
            } else {
                console.log('Ephemeral Tasks:');
                tasks.forEach(task => {
                    console.log(`- [ID: ${task.id}] ${task.description}`);
                });
            }
            break;
        case 'forget':
            const taskId = args[1];
            if (!taskId) {
                console.error('Error: Please provide the ID of the task to forget.');
                process.exit(1);
            }
            const forgotten = await forgetTask(taskId);
            if (forgotten) {
                console.log(`Task ${taskId} has faded into the ether.`);
            } else {
                console.error(`Error: Task with ID ${taskId} not found.`);
                process.exit(1);
            }
            break;
        default:
            console.log('Usage:');
            console.log('  node src/index.js add \"<description>\" - Add a new ephemeral task');
            console.log('  node src/index.js list              - List all ephemeral tasks');
            console.log('  node src/index.js forget <id>       - Forget a task by its ID');
            process.exit(1);
    }
}

main().catch(error => {
    console.error('An unexpected error occurred:', error.message);
    process.exit(1);
});
