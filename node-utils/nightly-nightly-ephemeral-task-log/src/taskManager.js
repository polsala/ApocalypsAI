const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto'); // For generating unique IDs

const DATA_FILE = path.join(__dirname, '..', 'tasks.json'); // Store in the root of the util directory

async function readTasks() {
    try {
        const data = await fs.readFile(DATA_FILE, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        if (error.code === 'ENOENT') {
            return []; // File doesn't exist, return empty array
        }
        throw error;
    }
}

async function writeTasks(tasks) {
    await fs.writeFile(DATA_FILE, JSON.stringify(tasks, null, 2), 'utf8');
}

async function addTask(description) {
    const tasks = await readTasks();
    const id = crypto.randomBytes(3).toString('hex'); // Generate a short, unique ID
    tasks.push({ id, description, timestamp: new Date().toISOString() });
    await writeTasks(tasks);
    return id;
}

async function listTasks() {
    return await readTasks();
}

async function forgetTask(id) {
    let tasks = await readTasks();
    const initialLength = tasks.length;
    tasks = tasks.filter(task => task.id !== id);
    if (tasks.length < initialLength) {
        await writeTasks(tasks);
        return true; // Task forgotten
    }
    return false; // Task not found
}

module.exports = {
    addTask,
    listTasks,
    forgetTask
};
