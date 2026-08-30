import * as fs from 'fs';
import * as path from 'path';

interface TemporalTask {
    id: string;
    name: string;
    description?: string;
    lastCompletedAt: string | null; // ISO string
    recurrenceDays: number;
    nextDueAt: string | null; // ISO string
}

export class TemporalTaskManager {
    private tasks: TemporalTask[] = [];
    private storagePath: string;
    private currentDateProvider: () => Date;

    constructor(storagePath: string, currentDateProvider: () => Date = () => new Date()) {
        this.storagePath = storagePath;
        this.currentDateProvider = currentDateProvider;
        this.loadTasks();
    }

    private loadTasks(): void {
        try {
            if (fs.existsSync(this.storagePath)) {
                const data = fs.readFileSync(this.storagePath, 'utf8');
                this.tasks = JSON.parse(data);
            }
        } catch (error) {
            console.error('Failed to load tasks:', error);
            this.tasks = [];
        }
    }

    private saveTasks(): void {
        try {
            fs.writeFileSync(this.storagePath, JSON.stringify(this.tasks, null, 2), 'utf8');
        } catch (error) {
            console.error('Failed to save tasks:', error);
        }
    }

    private calculateNextDue(lastCompletedAt: string | null, recurrenceDays: number): string | null {
        if (!lastCompletedAt) {
            return null; // Task has never been completed, no next due date yet
        }
        const lastDate = new Date(lastCompletedAt);
        lastDate.setDate(lastDate.getDate() + recurrenceDays);
        return lastDate.toISOString();
    }

    addTask(name: string, recurrenceDays: number, description?: string): TemporalTask {
        // Using Date.now() for ID generation. While simple, it might not be unique if two tasks are added in the same millisecond.
        const newTask: TemporalTask = {
            id: this.currentDateProvider().getTime().toString(), // More robust ID than Date.now() if using mockDateProvider
            name,
            description,
            lastCompletedAt: null,
            recurrenceDays,
            nextDueAt: null,
        };
        this.tasks.push(newTask);
        this.saveTasks();
        return newTask;
    }

    completeTask(id: string): TemporalTask | undefined {
        const taskIndex = this.tasks.findIndex(task => task.id === id);
        if (taskIndex === -1) {
            return undefined;
        }
        const task = this.tasks[taskIndex];
        task.lastCompletedAt = this.currentDateProvider().toISOString();
        task.nextDueAt = this.calculateNextDue(task.lastCompletedAt, task.recurrenceDays);
        this.saveTasks();
        return task;
    }

    getTasks(): TemporalTask[] {
        // Recalculate nextDueAt for tasks on retrieval to ensure it's always current based on lastCompletedAt
        // and the recurrence rule, especially if the current date context changes (e.g., in tests).
        return this.tasks.map(task => ({
            ...task,
            nextDueAt: task.lastCompletedAt ? this.calculateNextDue(task.lastCompletedAt, task.recurrenceDays) : null
        }));
    }

    getUpcomingTasks(daysAhead: number = 7): TemporalTask[] {
        const now = this.currentDateProvider();
        const futureDate = new Date(now);
        futureDate.setDate(now.getDate() + daysAhead);

        return this.getTasks().filter(task => {
            if (!task.nextDueAt) return false;
            const dueDate = new Date(task.nextDueAt);
            // Check if dueDate is between 'now' (inclusive) and 'futureDate' (inclusive)
            return dueDate.getTime() >= now.getTime() && dueDate.getTime() <= futureDate.getTime();
        }).sort((a, b) => {
            if (!a.nextDueAt || !b.nextDueAt) return 0; // Should not happen with filter
            return new Date(a.nextDueAt).getTime() - new Date(b.nextDueAt).getTime();
        });
    }
}

// CLI Logic
if (require.main === module) {
    const storageFile = path.join(process.cwd(), 'temporal_tasks.json');
    const manager = new TemporalTaskManager(storageFile);

    const args = process.argv.slice(2);
    const command = args[0];

    switch (command) {
        case 'add':
            const name = args[1];
            const recurrenceDays = parseInt(args[2], 10);
            const description = args[3];
            if (!name || isNaN(recurrenceDays) || recurrenceDays <= 0) {
                console.log('Usage: add <name> <recurrence_days> [description]');
                console.log('  <recurrence_days> must be a positive number.');
                process.exit(1);
            }
            const newTask = manager.addTask(name, recurrenceDays, description);
            console.log(`Added task "${newTask.name}" (ID: ${newTask.id}) recurring every ${newTask.recurrenceDays} days.`);
            break;

        case 'complete':
            const taskId = args[1];
            if (!taskId) {
                console.log('Usage: complete <task_id>');
                process.exit(1);
            }
            const completedTask = manager.completeTask(taskId);
            if (completedTask) {
                console.log(`Completed task "${completedTask.name}". Next due: ${completedTask.nextDueAt ? new Date(completedTask.nextDueAt).toLocaleDateString() : 'N/A'}`);
            } else {
                console.log(`Task with ID "${taskId}" not found.`);
            }
            break;

        case 'list':
            const allTasks = manager.getTasks();
            if (allTasks.length === 0) {
                console.log('No temporal tasks registered.');
                break;
            }
            console.log('--- All Temporal Tasks ---');
            allTasks.forEach(task => {
                console.log(`ID: ${task.id}`);
                console.log(`  Name: ${task.name}`);
                if (task.description) console.log(`  Description: ${task.description}`);
                console.log(`  Recurrence: Every ${task.recurrenceDays} days`);
                console.log(`  Last Completed: ${task.lastCompletedAt ? new Date(task.lastCompletedAt).toLocaleDateString() : 'Never'}`);
                console.log(`  Next Due: ${task.nextDueAt ? new Date(task.nextDueAt).toLocaleDateString() : 'N/A'}`);
                console.log('---');
            });
            break;

        case 'upcoming':
            const days = args[1] ? parseInt(args[1], 10) : 7;
            if (isNaN(days) || days < 0) {
                console.log('Usage: upcoming [days_ahead, default 7]');
                console.log('  <days_ahead> must be a non-negative number.');
                process.exit(1);
            }
            const upcomingTasks = manager.getUpcomingTasks(days);
            if (upcomingTasks.length === 0) {
                console.log(`No upcoming tasks in the next ${days} days.`);
                break;
            }
            console.log(`--- Upcoming Temporal Tasks (next ${days} days) ---`);
            upcomingTasks.forEach(task => {
                console.log(`ID: ${task.id}`);
                console.log(`  Name: ${task.name}`);
                console.log(`  Next Due: ${task.nextDueAt ? new Date(task.nextDueAt).toLocaleDateString() : 'N/A'}`);
                console.log('---');
            });
            break;

        default:
            console.log('Usage:');
            console.log('  npm start add <name> <recurrence_days> [description]');
            console.log('  npm start complete <task_id>');
            console.log('  npm start list');
            console.log('  npm start upcoming [days_ahead, default 7]');
            process.exit(1);
    }
}
