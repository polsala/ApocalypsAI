const parseArgs = require('minimist');

const SNOOZE_TYPES = {
  power: { min: 20, max: 25 },
  light: { min: 45, max: 50 },
  full: { min: 90, max: 100 },
};

const WHIMSICAL_MESSAGES = [
  "The temporal currents have been recalibrated. Rise, survivor, and seize the fleeting present!",
  "A brief journey through the ether concludes. Your mind is now a sharper blade against the encroaching void.",
  "The fabric of time bends to your will. Awaken, for destiny awaits your refreshed gaze.",
  "Your internal chronometer is reset. The wasteland beckons, and you are ready.",
  "From the depths of slumber, a new clarity emerges. Go forth and conquer the day's anomalies!",
  "Temporal distortion stabilized. Your consciousness returns, sharper than ever.",
  "The whispers of the void recede. Embrace the now, for it is your only true possession.",
  "Recharged and re-aligned. The universe awaits your next move.",
  "Your spirit has traversed the dream-streams. Return, and bring forth your renewed vigor.",
  "The cosmic clock ticks anew for you. Awaken with purpose!"
];

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min; // The maximum is inclusive and the minimum is inclusive
}

function getSnoozeDuration(type, customDuration) {
  if (customDuration) {
    const duration = parseInt(customDuration, 10);
    if (isNaN(duration) || duration <= 0) {
      throw new Error("Custom duration must be a positive number of minutes.");
    }
    return duration;
  }

  const snoozeType = SNOOZE_TYPES[type];
  if (!snoozeType) {
    throw new Error(`Invalid snooze type: '${type}'. Valid types are: ${Object.keys(SNOOZE_TYPES).join(', ')}.`);
  }
  return getRandomInt(snoozeType.min, snoozeType.max);
}

function formatDateTime(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

function main(argv) {
  argv = argv || parseArgs(process.argv.slice(2));
  const type = argv.type || 'power';
  const durationArg = argv.duration;

  try {
    const snoozeDuration = getSnoozeDuration(type, durationArg);
    const startTime = new Date();
    const wakeUpTime = new Date(startTime.getTime() + snoozeDuration * 60 * 1000);

    let snoozeDescription = `a ${type} Chrono-Snooze`;
    if (durationArg) {
      snoozeDescription = `a Custom Chrono-Snooze (${snoozeDuration} minutes)`;
    }

    const message = WHIMSICAL_MESSAGES[getRandomInt(0, WHIMSICAL_MESSAGES.length - 1)];

    console.log(`Initiating ${snoozeDescription}...`);
    console.log(`Current time: ${formatDateTime(startTime)}`);
    console.log(`Wake-up time: ${formatDateTime(wakeUpTime)}`);
    console.log(`Message: ${message}`);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

// Export for testing and direct execution
if (require.main === module) {
  main();
}

module.exports = {
  getSnoozeDuration,
  formatDateTime,
  WHIMSICAL_MESSAGES,
  SNOOZE_TYPES,
  getRandomInt,
  main
};
