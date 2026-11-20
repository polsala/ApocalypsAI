#!/usr/bin/env node

const priorityMap = {
    'critical': 3,
    'urgent': 2,
    'normal': 1,
    'low': 0
};

const impactMap = {
    'high': 3,
    'medium': 2,
    'low': 1
};

const doomDescriptors = [
    'Imminent', 'Urgent', 'Pressing', 'Lingering',
    'Mildly Concerning', 'Somewhat Distant', 'Hypothetical',
    'Cataclysmic', 'Apocalyptic', 'Dire', 'Crucial', 'Minor Glitch'
];

const chaosEmojis = [
    '💥', '🔥', '🌪️', '⚡', '💀', '☢️', '☣️', '⚠️', '🚨', '⏳', '🌑', '🌌', '👾', '🤖', '🛸'
];

function parseTaskString(taskString) {
    let name = taskString;
    let priority = 'normal';
    let impact = 'medium';

    const parts = taskString.split(' --');
    if (parts.length > 1) {
        name = parts[0].trim();
        for (let i = 1; i < parts.length; i++) {
            const [key, value] = parts[i].split(' ').map(s => s.trim());
            if (key === 'priority' && priorityMap.hasOwnProperty(value)) {
                priority = value;
            } else if (key === 'impact' && impactMap.hasOwnProperty(value)) {
                impact = value;
            }
        }
    }

    return { name, priority, impact };
}

function generateChaosFactors() {
    const chaosRating = Math.floor(Math.random() * 10) + 1; // 1-10
    const descriptor = doomDescriptors[Math.floor(Math.random() * doomDescriptors.length)];
    const emoji = chaosEmojis[Math.floor(Math.random() * chaosEmojis.length)];
    return { chaosRating, descriptor, emoji };
}

function calculateScore(task) {
    const priorityValue = priorityMap[task.priority] || priorityMap['normal'];
    const impactValue = impactMap[task.impact] || impactMap['medium'];
    // Weighted score: priority has higher weight than impact, chaos adds a random element
    return (priorityValue * 100) + (impactValue * 50) + task.chaosRating;
}

function main(args) {
    const tasks = [];
    
    const rawArgs = args.slice(2);

    if (rawArgs.length === 0) {
        console.log("No tasks provided. Usage: doom-list \"Task 1 --priority urgent\" \"Task 2\"");
        // In test environment, we throw an error to simulate exit, but in real run, it exits.
        if (process.env.NODE_ENV !== 'test') {
            process.exit(0);
        } else {
            throw new Error('Simulated process exit with code 0');
        }
    }

    rawArgs.forEach(arg => {
        const parsedTask = parseTaskString(arg);
        const chaos = generateChaosFactors();
        tasks.push({
            ...parsedTask,
            ...chaos,
            score: 0 // Will be calculated after chaos factors are assigned
        });
    });

    tasks.forEach(task => {
        task.score = calculateScore(task);
    });

    tasks.sort((a, b) => b.score - a.score); // Sort descending by score

    console.log("\n--- Apocalyptic Doom List Prioritization ---");
    tasks.forEach((task, index) => {
        const priorityColor = {
            'critical': '\x1b[31m', // Red
            'urgent': '\x1b[33m',   // Yellow
            'normal': '\x1b[32m',   // Green
            'low': '\x1b[34m'       // Blue
        }[task.priority] || '\x1b[0m'; // Reset

        const resetColor = '\x1b[0m';

        console.log(
            `${index + 1}. ${task.emoji} ${priorityColor}[${task.priority.toUpperCase()}]${resetColor} ` +
            `(${task.impact.toUpperCase()} Impact, Chaos: ${task.chaosRating}/10, ${task.descriptor}): ` +
            `${task.name}`
        );
    });
    console.log("------------------------------------------\n");
}

// Export for testing
module.exports = {
    main,
    parseTaskString,
    generateChaosFactors,
    calculateScore,
    priorityMap,
    impactMap,
    doomDescriptors,
    chaosEmojis
};

// Run main function only if executed directly (not imported as a module)
if (require.main === module && process.env.NODE_ENV !== 'test') {
    main(process.argv);
}
