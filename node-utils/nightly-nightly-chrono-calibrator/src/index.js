#!/usr/bin/env node

const fetch = require('node-fetch');
const chalk = require('chalk');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

const API_URL = 'http://worldtimeapi.org/api/ip';

async function getTrueUnixTime() {
    try {
        const response = await fetch(API_URL);
        if (!response.ok) {
            throw new Error(`Temporal Beacon Network error: ${response.statusText}`);
        }
        const data = await response.json();
        return data.unixtime;
    } catch (error) {
        console.error(chalk.red(`\n🚨 Failed to contact Temporal Beacon Network: ${error.message}`));
        console.error(chalk.yellow('Please check your internet connection or try again later.'));
        process.exit(1);
    }
}

function getLocalUnixTime() {
    return Math.floor(Date.now() / 1000);
}

function calculateDrift(trueTime, localTime) {
    return localTime - trueTime; // Positive if local is ahead, negative if local is behind
}

async function main() {
    const argv = yargs(hideBin(process.argv))
        .option('no-color', {
            type: 'boolean',
            description: 'Disable colored output',
            default: false
        })
        .help()
        .alias('h', 'help')
        .argv;

    if (argv['no-color']) {
        chalk.level = 0;
    }

    console.log(chalk.cyan('\n🌌 Initiating Chrono-Compass Calibration...'));
    console.log(chalk.blue('📡 Contacting Temporal Beacon Network...'));

    const trueTime = await getTrueUnixTime();
    const localTime = getLocalUnixTime();
    const driftSeconds = calculateDrift(trueTime, localTime);

    console.log(chalk.green(`✅ Temporal Beacon Network responded with true time: ${trueTime} (Unix Epoch)`));
    console.log(chalk.yellow(`⏳ Your local Chrono-Compass reads: ${localTime} (Unix Epoch)`));

    if (Math.abs(driftSeconds) < 1) { // Less than 1 second drift
        console.log(chalk.green('\n✨ Your Chrono-Compass is perfectly aligned! No significant Temporal Drift Anomalies detected.'));
    } else {
        const driftDirection = driftSeconds > 0 ? 'ahead of' : 'behind';
        const driftMagnitude = Math.abs(driftSeconds).toFixed(3);
        const driftColor = driftSeconds > 0 ? chalk.red : chalk.magenta;

        console.log(driftColor(`\n⚠️ Temporal Drift Anomaly Detected!`));
        console.log(driftColor(`Your Chrono-Compass is drifting by ${driftSeconds > 0 ? '+' : ''}${driftMagnitude} seconds (${driftDirection} true time).`));

        console.log(chalk.gray('\nTo re-harmonize your Chrono-Compass, consider these actions:'));
        console.log(chalk.gray('- On Linux/macOS: `sudo ntpdate -u pool.ntp.org` or `sudo systemctl restart systemd-timesyncd`'));
        console.log(chalk.gray('- On Windows: Open \'Date & Time settings\' and click \'Sync now\' or run `w32tm /resync` in an elevated command prompt.'));
    }
    console.log(''); // Newline for cleaner output
}

if (require.main === module) {
    main();
}

// Export for testing
module.exports = {
    getTrueUnixTime,
    getLocalUnixTime,
    calculateDrift,
    main,
    API_URL
};
