#!/usr/bin/env node

const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

/**
 * Determines the temporal guidance based on a given Date object.
 * @param {Date} date - The date object to base the guidance on.
 * @returns {{dayName: string, hour: number, direction: string, activity: string}}
 */
const getTemporalGuidance = (date) => {
  const hour = date.getHours();
  const day = date.getDay(); // 0 = Sunday, 1 = Monday, ..., 6 = Saturday

  let direction;
  let activity;

  // Weekday logic (Monday-Friday)
  if (day >= 1 && day <= 5) {
    if (hour >= 6 && hour < 11) { // Morning (6 AM - 10:59 AM)
      direction = "Plan for the Future";
      activity = "Sketch out tomorrow's survival route.";
    } else if (hour >= 11 && hour < 17) { // Afternoon (11 AM - 4:59 PM)
      direction = "Live in the Present";
      activity = "Tend to your immediate surroundings.";
    } else if (hour >= 17 && hour < 22) { // Evening (5 PM - 9:59 PM)
      direction = "Reflect on the Past";
      activity = "Journal about today's discoveries.";
    } else { // Late Night/Early Morning (10 PM - 5:59 AM)
      direction = "Embrace the Void";
      activity = "Contemplate the vastness of the cosmos.";
    }
  } else { // Weekend logic (Saturday & Sunday)
    if (hour >= 8 && hour < 13) { // Morning/Late Morning (8 AM - 12:59 PM)
      direction = "Explore New Horizons";
      activity = "Scavenge for forgotten knowledge or resources.";
    } else if (hour >= 13 && hour < 19) { // Afternoon/Evening (1 PM - 6:59 PM)
      direction = "Rejuvenate Your Spirit";
      activity = "Engage in a calming, non-essential task.";
    } else { // Late Night/Early Morning (7 PM - 7:59 AM)
      direction = "Dream of What Was";
      activity = "Recall a cherished memory from before.";
    }
  }

  const dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const currentDayName = dayNames[day];

  return {
    dayName: currentDayName,
    hour: hour,
    direction: direction,
    activity: activity
  };
};

const argv = yargs(hideBin(process.argv))
  .command('$0', 'Get your temporal guidance for the current moment.', (yargs) => {
    yargs
      .option('hour', {
        alias: 'h',
        type: 'number',
        description: 'Specify an hour (0-23) for guidance.',
        choices: Array.from({ length: 24 }, (_, i) => i)
      })
      .option('day', {
        alias: 'd',
        type: 'string',
        description: 'Specify a day (e.g., "Monday", "Sunday") for guidance.',
        choices: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
      });
  })
  .help()
  .alias('help', 'H')
  .argv;

const run = () => {
  let date;
  if (argv.hour !== undefined || argv.day !== undefined) {
    // Mock rationale: Allow specifying hour/day for deterministic testing and future features.
    // Create a base date (Jan 1, 2023 was a Sunday) to consistently calculate the day of the month.
    const now = new Date();

    let targetHour = argv.hour !== undefined ? argv.hour : now.getHours();
    let targetDayIndex = now.getDay(); // Default to current day index

    if (argv.day !== undefined) {
      const dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
      const specifiedDayIndex = dayNames.indexOf(argv.day);
      if (specifiedDayIndex !== -1) {
        targetDayIndex = specifiedDayIndex;
      }
    }

    // Calculate the day of the month for the targetDayIndex relative to Jan 1, 2023 (Sunday).
    // Jan 1, 2023 (day 0) -> day of month 1
    // Jan 2, 2023 (day 1) -> day of month 2
    // ...
    // Jan 7, 2023 (day 6) -> day of month 7
    const targetDayOfMonth = 1 + targetDayIndex;

    // Create a new Date object with the specified year, month, day, and hour.
    // Using a fixed year/month/day for the mock ensures consistency across runs.
    date = new Date(2023, 0, targetDayOfMonth, targetHour); // Month is 0-indexed (Jan=0)
  } else {
    date = new Date(); // Use current date if no arguments are provided
  }

  const { dayName, hour, direction, activity } = getTemporalGuidance(date);

  console.log("\n🧭 Nightly Chrono-Compass 🧭\n");
  console.log(`It's a ${dayName} ${hour >= 12 ? 'afternoon' : 'morning'}.`);
  console.log(`Your temporal direction: ${direction}.`);
  console.log(`Suggested activity: ${activity}.\n`);
};

// Export for testing
module.exports = { getTemporalGuidance, run };

// If run directly, execute the main function
if (require.main === module) {
  run();
}
