const { Command } = require('commander');
const chalk = require('chalk');

const program = new Command();

// # Mock rationale: In a real scenario, this would fetch time from a remote NTP server.
// # For a self-contained, deterministic utility, we simulate this fetch.
async function fetchTemporalAnchorTime(serverUrl) {
    // Simulate network latency and a slightly varying time
    // For deterministic testing, this will be mocked externally.
    // const simulatedDelay = Math.random() * 1000; // 0-1 second delay
    // await new Promise(resolve => setTimeout(resolve, simulatedDelay));

    // Simulate a time that is slightly ahead or behind current system time
    // For deterministic testing, this will be mocked.
    const anchorTime = new Date(Date.now() + (Math.random() * 10000 - 5000)); // +/- 5 seconds from current
    return anchorTime;
}

function formatTime(date) {
    return date.toISOString();
}

function formatSuggestedCommand(targetDate) {
    const year = targetDate.getFullYear();
    const month = String(targetDate.getMonth() + 1).padStart(2, '0');
    const day = String(targetDate.getDate()).padStart(2, '0');
    const hours = String(targetDate.getHours()).padStart(2, '0');
    const minutes = String(targetDate.getMinutes()).padStart(2, '0');
    const seconds = String(targetDate.getSeconds()).padStart(2, '0');

    // This command is for Linux/macOS. Windows would use 'date /T' and 'time /T' or 'Set-Date'.
    // For simplicity and common server environments, we provide the Linux/macOS command.
    return `sudo date -s "${year}-${month}-${day} ${hours}:${minutes}:${seconds}"`;
}

program
    .name('chrono-compass')
    .description('A whimsical utility to synchronize system time with a simulated Temporal Anchor.')
    .option('-s, --server <url>', 'URL of the Temporal Anchor NTP server', 'https://apocalypsai.time.anchor')
    .option('-d, --distort', 'Enable whimsical temporal distortion', false)
    .action(async (options) => {
        console.log(chalk.blue('[Chrono-Compass] Calibrating with Temporal Anchor: ') + chalk.cyan(options.server));

        const localTime = new Date();
        console.log(chalk.yellow('[Chrono-Compass] Local Time: ') + formatTime(localTime));

        let anchorTime = await exports.fetchTemporalAnchorTime(options.server); // Call through exports
        console.log(chalk.green('[Chrono-Compass] Anchor Time: ') + formatTime(anchorTime));

        if (options.distort) {
            const distortionMagnitude = (Math.random() * 10 - 5) * 1000; // +/- 5 seconds in milliseconds
            console.log(chalk.magenta(`[Chrono-Compass] Applying whimsical temporal distortion... (${(distortionMagnitude / 1000).toFixed(3)} seconds)`));
            anchorTime = new Date(anchorTime.getTime() + distortionMagnitude);
            console.log(chalk.magenta('[Chrono-Compass] Effective Anchor Time: ') + formatTime(anchorTime));
        }

        const timeDifferenceMs = anchorTime.getTime() - localTime.getTime();
        const timeDifferenceSeconds = (timeDifferenceMs / 1000).toFixed(3);
        console.log(chalk.blue('[Chrono-Compass] Time difference: ') + chalk.white(`${timeDifferenceSeconds} seconds.`));

        const suggestedSyncTime = new Date(localTime.getTime() + timeDifferenceMs);
        console.log(chalk.blue('[Chrono-Compass] Suggested command to synchronize:'));
        console.log(chalk.gray(`    ${formatSuggestedCommand(suggestedSyncTime)}`));

        console.log(chalk.white('\n[Chrono-Compass] Calibration complete. May your chronometers be ever-so-slightly-accurate.'));
    });

// Export for testing purposes
exports.program = program;
exports.fetchTemporalAnchorTime = fetchTemporalAnchorTime;
