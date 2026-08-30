const { Command } = require('commander');
const chalk = require('chalk');
const { calculateDrift } = require('./chronoDrift');

const program = new Command();

program
  .name('chrono-drift-adjuster')
  .description('Calculates and suggests temporal clock adjustments based on simulated cosmic drift.')
  .version('1.0.0');

program
  .option('-s, --seed <number>', 'A numerical seed for drift calculation (e.g., current day of year)', (value) => parseInt(value, 10), null)
  .action((options) => {
    const now = new Date();
    // Default seed: days since epoch, ensuring a daily-changing drift if no seed is provided.
    const seed = options.seed !== null ? options.seed : Math.floor(now.getTime() / (1000 * 60 * 60 * 24));

    const {
      currentTime,
      adjustmentSeconds,
      adjustedTime,
      stabilityMessage
    } = calculateDrift(seed, now);

    console.log(chalk.blue('\n--- Nightly Chrono-Drift Adjuster ---'));
    console.log(`Current Local Time: ${chalk.cyan(currentTime.toLocaleTimeString())}`);
    console.log(`Temporal Seed Used: ${chalk.magenta(seed)}`);
    console.log(`Detected Chrono-Drift: ${chalk.yellow(adjustmentSeconds > 0 ? '+' : '')}${chalk.yellow(adjustmentSeconds)} seconds`);
    console.log(`Recommended Adjustment: ${chalk.bold(adjustmentSeconds > 0 ? 'ADD' : 'SUBTRACT')} ${chalk.bold(Math.abs(adjustmentSeconds))} seconds`);
    console.log(`Calibrated Local Time (approx): ${chalk.green(adjustedTime.toLocaleTimeString())}`);
    console.log(`\nTemporal Stability Forecast: ${chalk.blue(stabilityMessage)}`);
    console.log(chalk.blue('-------------------------------------\n'));
  });

program.parse(process.argv);
