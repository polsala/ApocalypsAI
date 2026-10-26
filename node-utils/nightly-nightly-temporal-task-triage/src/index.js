const fs = require('fs');
const path = require('path');

// Define weights for temporal resonance categories
const RESONANCE_WEIGHTS = {
    "Rumbles of the Imminent": 5,
    "Whispers of Now": 4,
    "Shadows of Tomorrow": 3,
    "Echoes of Yesteryear": 2,
    "Flickers of the Distant": 1,
    "unknown": 0 // Default for invalid/missing resonance
};

// Define weights for priority levels
const PRIORITY_WEIGHTS = {
    "critical": 5,
    "high": 4,
    "medium": 3,
    "low": 2,
    "none": 1,
    "unknown": 0 // Default for invalid/missing priority
};

/**
 * Calculates a triage score for a given task.
 * @param {object} task - The task object with 'resonance' and 'priority' fields.
 * @returns {number} The calculated triage score.
 */
function calculateTriageScore(task) {
    const resonance = task.resonance || 'unknown';
    const priority = task.priority || 'unknown';

    const resonanceWeight = RESONANCE_WEIGHTS[resonance] !== undefined ? RESONANCE_WEIGHTS[resonance] : RESONANCE_WEIGHTS.unknown;
    const priorityWeight = PRIORITY_WEIGHTS[priority] !== undefined ? PRIORITY_WEIGHTS[priority] : PRIORITY_WEIGHTS.unknown;

    // Combine weights: resonance has a higher impact
    return (resonanceWeight * 10) + priorityWeight;
}

/**
 * Reads tasks from a JSON file.
 * @param {string} filePath - The path to the JSON file.
 * @returns {Array<object>} An array of task objects.
 * @throws {Error} If the file cannot be read or parsed.
 */
function readTasksFromFile(filePath) {
    try {
        const fileContent = fs.readFileSync(filePath, 'utf8');
        const tasks = JSON.parse(fileContent);
        if (!Array.isArray(tasks)) {
            throw new Error('Invalid JSON format: Expected an array of tasks.');
        }
        return tasks;
    } catch (error) {
        if (error.code === 'ENOENT') {
            throw new Error(`Error: Task file not found at '${filePath}'.`);
        } else if (error instanceof SyntaxError) {
            throw new Error(`Error: Invalid JSON in '${filePath}'. Details: ${error.message}`);
        } else {
            throw new Error(`Error reading or parsing tasks: ${error.message}`);
        }
    }
}

/**
 * Triage and sort tasks based on their calculated scores.
 * @param {Array<object>} tasks - An array of task objects.
 * @returns {Array<object>} The sorted array of tasks, with scores added.
 */
function triageTasks(tasks) {
    const triagedTasks = [];
    for (const task of tasks) {
        if (!task.id || !task.description) {
            console.warn(`Warning: Skipping malformed task (missing id or description): ${JSON.stringify(task)}`);
            continue;
        }
        const score = calculateTriageScore(task);
        triagedTasks.push({ ...task, score });
    }

    // Sort in descending order of score
    triagedTasks.sort((a, b) => b.score - a.score);

    return triagedTasks;
}

/**
 * Main function to run the CLI utility.
 */
function main() {
    const args = process.argv.slice(2);
    if (args.length === 0) {
        console.error('Usage: node src/index.js <path_to_tasks.json>');
        process.exit(1);
    }

    const filePath = args[0];

    try {
        const tasks = readTasksFromFile(filePath);
        const sortedTasks = triageTasks(tasks);

        console.log('\n--- Temporal Task Triage Report ---\n');
        if (sortedTasks.length === 0) {
            console.log('No tasks to triage or all tasks were malformed.');
        } else {
            sortedTasks.forEach((task, index) => {
                console.log(`${index + 1}. [${task.score}] ${task.description} (${task.resonance || 'unknown'}, ${task.priority || 'unknown'})`);
            });
        }
        console.log('\n-----------------------------------');

    } catch (error) {
        console.error(error.message);
        process.exit(1);
    }
}

// Only run main if this script is executed directly
if (require.main === module) {
    main();
}

// Export for testing
module.exports = {
    calculateTriageScore,
    readTasksFromFile,
    triageTasks,
    RESONANCE_WEIGHTS,
    PRIORITY_WEIGHTS
};
