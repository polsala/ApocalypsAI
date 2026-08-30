import { Command } from 'commander';
import { applyShifts } from './index';
import { ChronoShift } from './types';

const program = new Command();

program
  .name('nightly-chrono-shift-calc')
  .description('Calculates future dates and times by applying a series of defined temporal shifts.')
  .version('1.0.0');

program
  .requiredOption('--start-date <date-string>', 'The initial date and time (ISO 8601 format, e.g., "2023-10-26T10:00:00")')
  .requiredOption('--shifts <json-array-string>', 'A JSON string representing an array of temporal shifts to apply.')
  .action((options) => {
    try {
      const startDate = new Date(options.startDate);
      if (isNaN(startDate.getTime())) {
        throw new Error('Invalid start date provided. Please use a valid ISO 8601 format.');
      }

      const shifts: ChronoShift[] = JSON.parse(options.shifts);
      if (!Array.isArray(shifts)) {
        throw new Error('Shifts must be a JSON array.');
      }
      // Basic validation for shifts structure (more detailed validation could be added)
      for (const shift of shifts) {
        if (!shift || typeof shift.type !== 'string') {
          throw new Error('Each shift must have a "type" property.');
        }
      }

      const resultDate = applyShifts(startDate, shifts);
      console.log(resultDate.toISOString());
    } catch (error: any) {
      console.error(`Error: ${error.message}`);
      process.exit(1);
    }
  });

program.parse(process.argv);
