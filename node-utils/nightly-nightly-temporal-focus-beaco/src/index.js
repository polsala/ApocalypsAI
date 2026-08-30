const process = require('process');

const messages = {
  workStart: [
    "The void demands your attention! Focus, survivor!",
    "Initiating temporal focus sequence. Engage!",
    "The digital wasteland awaits your input. Concentrate!"
  ],
  workEnd: [
    "Your temporal focus has stabilized. Time for a brief respite from the data storms.",
    "Work cycle complete. Data streams are momentarily calm.",
    "Task segment concluded. Prepare for recalibration."
  ],
  breakStart: [
    "Seek solace in the quiet hum of the server racks. Recharge your neural pathways.",
    "Temporal respite initiated. Breathe, survivor.",
    "Short break protocol active. Disconnect from the matrix."
  ],
  breakEnd: [
    "The temporal currents shift. Return to your duties, for the digital wasteland awaits.",
    "Break over. Re-engage with the temporal flow.",
    "Recalibration complete. Resume operations."
  ],
  longBreakStart: [
    "A longer temporal distortion detected. Indulge in extended recalibration, survivor.",
    "Long break protocol engaged. Deep system reset recommended.",
    "Extended respite granted. Reflect on the vastness of the digital cosmos."
  ]
};

function getRandomMessage(type) {
  const msgs = messages[type];
  if (!msgs || msgs.length === 0) return "";
  return msgs[Math.floor(Math.random() * msgs.length)];
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}

function parseArgs(args) {
  const options = {
    work: 25,
    break: 5,
    longBreak: 15,
    cycles: 4,
    help: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '-w':
      case '--work':
        options.work = parseInt(args[++i], 10);
        break;
      case '-b':
      case '--break':
        options.break = parseInt(args[++i], 10);
        break;
      case '-l':
      case '--long-break':
        options.longBreak = parseInt(args[++i], 10);
        break;
      case '-c':
      case '--cycles':
        options.cycles = parseInt(args[++i], 10);
        break;
      case '-h':
      case '--help':
        options.help = true;
        break;
      default:
        // Ignore unknown args for now
        break;
    }
  }
  return options;
}

function displayHelp() {
  console.log("\nUsage: node src/index.js [options]");
  console.log("\nOptions:");
  console.log("  -w, --work <minutes>      Duration of the work session in minutes (default: 25)");
  console.log("  -b, --break <minutes>     Duration of the short break session in minutes (default: 5)");
  console.log("  -l, --long-break <minutes>  Duration of the long break session in minutes (default: 15)");
  console.log("  -c, --cycles <number>     Number of work/short-break cycles before a long break (default: 4)");
  console.log("  -h, --help                Display help information\n");
}

async function startTimer(durationMinutes, type, cycleCount, totalCycles, isLongBreak = false) {
  const durationSeconds = durationMinutes * 60;
  let remainingSeconds = durationSeconds;

  const messageType = isLongBreak ? 'longBreakStart' : (type === 'work' ? 'workStart' : 'breakStart');
  console.log(`\n${getRandomMessage(messageType)}`);
  console.log(`--- ${type.toUpperCase()} (${cycleCount}/${totalCycles}) ---`);

  return new Promise(resolve => {
    if (durationSeconds <= 0) {
      const endMessageType = type === 'work' ? 'workEnd' : 'breakEnd';
      console.log(`\n${getRandomMessage(endMessageType)}`);
      resolve();
      return;
    }

    const interval = setInterval(() => {
      remainingSeconds--;
      process.stdout.write(`\rTime remaining: ${formatTime(remainingSeconds)}`);

      if (remainingSeconds <= 0) {
        clearInterval(interval);
        const endMessageType = type === 'work' ? 'workEnd' : 'breakEnd';
        console.log(`\n${getRandomMessage(endMessageType)}`);
        resolve();
      }
    }, 1000);
  });
}

async function run() {
  const options = parseArgs(process.argv.slice(2));

  if (options.help) {
    displayHelp();
    return;
  }

  console.log("\nNightly Temporal Focus Beacon Activated!");
  console.log(`Work: ${options.work} min, Break: ${options.break} min, Long Break: ${options.longBreak} min, Cycles: ${options.cycles}`);

  let currentCycle = 0;
  while (true) { // Loop indefinitely until user stops it
    currentCycle++;
    await startTimer(options.work, 'work', currentCycle, options.cycles);

    if (currentCycle % options.cycles === 0) {
      await startTimer(options.longBreak, 'long break', currentCycle, options.cycles, true);
      currentCycle = 0; // Reset cycles after a long break
    } else {
      await startTimer(options.break, 'break', currentCycle, options.cycles);
    }
  }
}

// Only run if executed directly
if (require.main === module) {
  run().catch(err => {
    console.error("An error occurred:", err);
    process.exit(1);
  });
}

// Export for testing
module.exports = {
  messages,
  getRandomMessage,
  formatTime,
  parseArgs,
  startTimer,
  run,
  displayHelp
};
