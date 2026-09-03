#!/usr/bin/env node

const { getDailySchedule } = require('./scheduler');
const fs = require('fs');
const path = require('path');

const DEFAULT_CONFIG_PATH = path.join(__dirname, '..', 'config.json'); // Default config location
const DEFAULT_SUNRISE = '06:00';
const DEFAULT_SUNSET = '18:00';

function parseArgs() {
    const args = process.argv.slice(2);
    let configPath = DEFAULT_CONFIG_PATH;
    let dateStr = new Date().toISOString().split('T')[0]; // Today's date YYYY-MM-DD

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--config' && args[i + 1]) {
            configPath = args[i + 1];
            i++;
        } else if (args[i] === '--date' && args[i + 1]) {
            dateStr = args[i + 1];
            i++;
        } else if (args[i] === '--help' || args[i] === '-h') {
            console.log(`\nUsage: nightly-luminescence-scheduler [options]\n\nOptions:\n  --config <path>  Path to the JSON configuration file (default: ${DEFAULT_CONFIG_PATH})\n  --date <YYYY-MM-DD> Date for which to generate the schedule (default: today)\n  --help, -h       Show this help message\n            `);
            process.exit(0);
        }
    }
    return { configPath, dateStr };
}

async function main() {
    const { configPath, dateStr } = parseArgs();

    let config = {
        defaultSunrise: DEFAULT_SUNRISE,
        defaultSunset: DEFAULT_SUNSET,
        events: []
    };

    try {
        if (fs.existsSync(configPath)) {
            const configFileContent = fs.readFileSync(configPath, 'utf8');
            const userConfig = JSON.parse(configFileContent);
            config = { ...config, ...userConfig }; // Merge user config
        } else if (configPath !== DEFAULT_CONFIG_PATH) {
            console.error(`Error: Configuration file not found at ${configPath}`);
            process.exit(1);
        }
        // If default config path doesn't exist, we proceed with hardcoded defaults and empty events.
    } catch (error) {
        console.error(`Error reading or parsing configuration file: ${error.message}`);
        process.exit(1);
    }

    const scheduleDate = new Date(dateStr);
    if (isNaN(scheduleDate.getTime())) {
        console.error(`Error: Invalid date format. Please use YYYY-MM-DD.`);
        process.exit(1);
    }

    const dailySchedule = getDailySchedule(config, scheduleDate);

    console.log(`Luminescence Schedule for ${dateStr}:`);
    console.log('------------------------------------');
    if (dailySchedule.length === 0) {
        console.log('No luminescent events scheduled for this day.');
    } else {
        dailySchedule.forEach(event => {
            console.log(`[${event.time}] ${event.name}`);
        });
    }
}

if (require.main === module) {
    main();
}
