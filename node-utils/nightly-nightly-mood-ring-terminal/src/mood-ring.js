#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// ANSI escape codes for colors
const colors = {
    reset: "\x1b[0m",
    bright: "\x1b[1m",
    dim: "\x1b[2m",
    underscore: "\x1b[4m",
    blink: "\x1b[5m",
    reverse: "\x1b[7m",
    hidden: "\x1b[8m",

    black: "\x1b[30m",
    red: "\x1b[31m",
    green: "\x1b[32m",
    yellow: "\x1b[33m",
    blue: "\x1b[34m",
    magenta: "\x1b[35m",
    cyan: "\x1b[36m",
    white: "\x1b[37m",

    bgBlack: "\x1b[40m",
    bgRed: "\x1b[41m",
    bgGreen: "\x1b[42m",
    bgYellow: "\x1b[43m",
    bgBlue: "\x1b[44m",
    bgMagenta: "\x1b[45m",
    bgCyan: "\x1b[46m",
    bgWhite: "\x1b[47m"
};

const moodKeywords = {
    angry: {
        color: colors.red,
        keywords: ['error', 'fail', 'panic', 'critical', 'exception', 'denied', 'abort', 'fatal']
    },
    anxious: {
        color: colors.yellow,
        keywords: ['warn', 'warning', 'timeout', 'retry', 'attention', 'pending', 'stalled', 'delay']
    },
    happy: {
        color: colors.green,
        keywords: ['success', 'complete', 'done', 'deployed', 'ok', 'pass', 'ready', 'up']
    },
    calm: {
        color: colors.blue,
        keywords: ['info', 'status', 'check', 'running', 'idle', 'healthy', 'monitor']
    },
    mysterious: {
        color: colors.magenta,
        keywords: ['unknown', 'mystery', 'anomaly', 'unidentified', 'strange', 'void']
    }
};

function getMood(logContent) {
    const lowerContent = logContent.toLowerCase();
    let moodScores = {
        angry: 0,
        anxious: 0,
        happy: 0,
        calm: 0,
        mysterious: 0
    };

    for (const mood in moodKeywords) {
        for (const keyword of moodKeywords[mood].keywords) {
            const regex = new RegExp(`\\b${keyword}\\b`, 'g'); // Whole word match
            const matches = lowerContent.match(regex);
            if (matches) {
                moodScores[mood] += matches.length;
            }
        }
    }

    let dominantMood = 'calm'; // Default mood
    let maxScore = 0;
    let totalScore = 0;

    for (const mood in moodScores) {
        totalScore += moodScores[mood];
        if (moodScores[mood] > maxScore) {
            maxScore = moodScores[mood];
            dominantMood = mood;
        }
    }

    // If no keywords found, or scores are very low, default to calm or mysterious
    if (totalScore === 0) {
        return { name: 'calm', color: moodKeywords.calm.color, message: 'The digital winds are calm.' };
    }
    
    // If scores are very mixed (e.g., multiple moods with similar high scores), lean towards mysterious or anxious
    const sortedScores = Object.values(moodScores).sort((a, b) => b - a);
    if (sortedScores.length >= 2 && sortedScores[0] > 0 && sortedScores[0] === sortedScores[1]) {
        return { name: 'mysterious', color: moodKeywords.mysterious.color, message: 'A strange aura permeates the logs...' };
    }

    const { color } = moodKeywords[dominantMood];
    let message = '';

    switch (dominantMood) {
        case 'angry':
            message = 'The logs are seething with digital rage!';
            break;
        case 'anxious':
            message = 'A nervous energy hums through the data streams.';
            break;
        case 'happy':
            message = 'A wave of digital serenity washes over the system.';
            break;
        case 'calm':
            message = 'The digital winds are calm.';
            break;
        case 'mysterious':
            message = 'A strange aura permeates the logs... what secrets do they hold?';
            break;
    }

    return { name: dominantMood, color, message };
}

function run() {
    const args = process.argv.slice(2);
    const filePath = args[0];

    if (!filePath) {
        console.error(`${colors.red}Usage: mood-ring <path-to-log-file>${colors.reset}`);
        process.exit(1);
    }

    try {
        const absolutePath = path.resolve(process.cwd(), filePath);
        const logContent = fs.readFileSync(absolutePath, 'utf8');
        const { color, message } = getMood(logContent);
        console.log(`${color}${colors.bright}Mood Ring Terminal: ${message}${colors.reset}`);
    } catch (error) {
        if (error.code === 'ENOENT') {
            console.error(`${colors.red}Error: File not found at '${filePath}'${colors.reset}`);
        } else {
            console.error(`${colors.red}Error reading file: ${error.message}${colors.reset}`);
        }S
        process.exit(1);
    }
}

// Export for testing
if (require.main === module) {
    run();
} else {
    module.exports = { getMood, colors, moodKeywords };
}
