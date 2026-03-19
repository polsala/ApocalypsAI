#!/usr/bin/env node

const { Command } = require('commander');
const fs = require('fs');
const path = require('path');

/**
 * Calculates a triage score for a given task.
 * @param {object} task - The task object.
 * @param {number} [task.urgency=5] - The base urgency of the task (1-10).
 * @param {string} [task.decay_rate='medium'] - How quickly the task loses relevance ('fast', 'medium', 'slow').
 * @returns {object} A new task object with 'urgency', 'decay_rate', and 'triage_score' properties.
 */
function calculateTriageScore(task) {
    const defaultUrgency = 5;
    const defaultDecayRate = 'medium';

    let urgency = task.urgency !== undefined ? parseInt(task.urgency, 10) : defaultUrgency;
    let decayRate = task.decay_rate || defaultDecayRate;

    if (isNaN(urgency) || urgency < 1 || urgency > 10) {
        console.warn(`Warning: Invalid urgency '${task.urgency}' for task '${task.description}'. Using default: ${defaultUrgency}.`);
        urgency = defaultUrgency;
    }

    const decayMultipliers = {
        'fast': 1.5,
        'medium': 1.0,
        'slow': 0.5
    };

    let multiplier = decayMultipliers[decayRate.toLowerCase()];
    if (!multiplier) {
        console.warn(`Warning: Invalid decay_rate '${task.decay_rate}' for task '${task.description}'. Using default: ${defaultDecayRate}.`);
        decayRate = defaultDecayRate;
        multiplier = decayMultipliers[defaultDecayRate];
    } else {
        decayRate = decayRate.toLowerCase();
    }

    const triage_score = urgency * multiplier;
    return { ...task, urgency, decay_rate: decayRate, triage_score };
}

/**
 * Sorts tasks by their triage score in descending order.
 * @param {Array<object>} tasks - An array of task objects.
 * @returns {Array<object>} The sorted array of tasks, each with an added 'triage_score'.
 */
function triageTasks(tasks) {
    if (!Array.isArray(tasks)) {
        throw new Error("Input must be an array of tasks.");
    }

    const scoredTasks = tasks.map(task => calculateTriageScore(task));

    // Sort by triage_score descending
    scoredTasks.sort((a, b) => b.triage_score - a.triage_score);

    return scoredTasks;
}

// CLI setup
const program = new Command();

program
    .name('temporal-triage')
    .description('Prioritizes tasks based on urgency and temporal decay.')
    .version('1.0.0');

program
    .option('-f, --file <path>', 'Path to a JSON file containing tasks.')
    .action(async (options) => {
        let tasks = [];

        if (options.file) {
            try {
                const filePath = path.resolve(options.file);
                const fileContent = fs.readFileSync(filePath, 'utf8');
                tasks = JSON.parse(fileContent);
            } catch (error) {
                console.error(`Error reading or parsing file ${options.file}: ${error.message}`);
                process.exit(1);
            }
        } else {
            console.error('Error: No input file specified. Use -f or --file to provide a task file.');
            program.help();
            process.exit(1);
        }

        try {
            const sortedTasks = triageTasks(tasks);

            console.log('\n--- Triage Report ---\n');
            sortedTasks.forEach((task, index) => {
                console.log(`${index + 1}. ${task.description} (Urgency: ${task.urgency}, Decay: ${task.decay_rate}, Score: ${task.triage_score.toFixed(1)})`);
            });
            console.log('\n');
        } catch (error) {
            console.error(`Error during task triage: ${error.message}`);
            process.exit(1);
        }
    });

// If this script is run directly, parse arguments
if (require.main === module) {
    program.parse(process.argv);
} else {
    // Export for testing purposes
    module.exports = {
        calculateTriageScore,
        triageTasks,
        program // Export the commander program for CLI testing
    };
}
