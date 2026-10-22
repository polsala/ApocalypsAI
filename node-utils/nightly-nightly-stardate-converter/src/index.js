#!/usr/bin/env node

const { program } = require('commander');

// Default constants
const DEFAULT_EPOCH_DATE = new Date('2000-01-01T00:00:00Z'); // January 1, 2000, UTC
const MS_PER_DAY = 1000 * 60 * 60 * 24;
const DEFAULT_BASE_STARDATE = 40000.0; // Starting Stardate for the epoch

/**
 * Calculates a Stardate from an Earth date string.
 * @param {string} inputDateString - The Earth date string (e.g., "2024-07-21").
 * @param {Date} epochDate - The epoch date for Stardate 0.0.
 * @param {number} baseStardate - The base Stardate to add to the calculated days.
 * @returns {string} The calculated Stardate, formatted to two decimal places.
 * @throws {Error} If the input date string is invalid.
 */
function calculateStardate(inputDateString, epochDate, baseStardate) {
  const inputDate = new Date(inputDateString);

  if (isNaN(inputDate.getTime())) {
    throw new Error(`Invalid date format: "${inputDateString}". Please use YYYY-MM-DD or a valid date string.`);
  }

  // Calculate difference in milliseconds
  const diffMs = inputDate.getTime() - epochDate.getTime();

  // Convert milliseconds to days
  const diffDays = diffMs / MS_PER_DAY;

  // Calculate Stardate
  const stardate = baseStardate + diffDays;

  return stardate.toFixed(2); // Format to two decimal places
}

program
  .name('stardate-converter')
  .description('Converts Earth dates to a whimsical Stardate format.')
  .version('1.0.0');

program
  .argument('<date>', 'The Earth date to convert (e.g., "2024-07-21", "July 21, 2024")')
  .option('-e, --epoch <date>', 'Custom epoch date (YYYY-MM-DD). Defaults to 2000-01-01.', '2000-01-01')
  .option('-b, --base <number>', 'Custom base stardate. Defaults to 40000.', parseFloat, DEFAULT_BASE_STARDATE)
  .action((dateString, options) => {
    try {
      const epoch = options.epoch ? new Date(options.epoch + 'T00:00:00Z') : DEFAULT_EPOCH_DATE;
      const base = options.base !== undefined ? options.base : DEFAULT_BASE_STARDATE;

      const stardate = calculateStardate(dateString, epoch, base);
      console.log(`Earth Date: ${dateString}`);
      console.log(`Stardate: ${stardate}`);
    } catch (error) {
      console.error(`Error: ${error.message}`);
      process.exit(1);
    }
  });

// If running as a script, parse arguments
if (require.main === module) {
  program.parse(process.argv);
}

// Export for testing
module.exports = { calculateStardate, DEFAULT_EPOCH_DATE, MS_PER_DAY, DEFAULT_BASE_STARDATE };
