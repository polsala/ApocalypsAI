"use strict";

const { Command } = require('commander');
const { spawn } = require('child_process');

const program = new Command();

program
  .name('chaos-monkey-scheduler')
  .description('Inject whimsical chaos into your system')
  .version('1.0.0')
  .option('--chaos <type>', 'type of chaos to inject (banana-peel, sneaky-cat, power-outage)')
  .option('--interval <time>', 'chaos interval (e.g. 10s, 1m)', '30s')
  .option('--dry-run', 'preview without executing')
  .action((options) => {
    const { chaos, interval, dryRun } = options;
    if (!chaos) {
      console.error('Error: --chaos <type> is required');
      process.exit(1);
    }

    console.log(`\n🌀 Chaos Monkey activated: ${chaos}`);
    console.log(`⏱️  Interval: ${interval}`);
    if (dryRun) console.log('🧪 Dry-run mode enabled\n');

    const ms = parseTime(interval);
    if (isNaN(ms)) {
      console.error('Invalid interval format');
      process.exit(1);
    }

    setInterval(() => {
      triggerChaos(chaos, dryRun);
    }, ms);
  });

function parseTime(str) {
  const match = str.match(/^(\d+)([smh])$/);
  if (!match) return NaN;
  const num = parseInt(match[1]);
  const unit = match[2];
  switch (unit) {
    case 's': return num * 1000;
    case 'm': return num * 60 * 1000;
    case 'h': return num * 3600 * 1000;
    default: return NaN;
  }
}

function triggerChaos(type, dryRun) {
  const actions = {
    'banana-peel': () => console.log('🍌 Slipped on a banana peel! Simulated service hiccup.'),
    'sneaky-cat': () => console.log('🐱 Sneaky cat unplugged the server! Simulated power loss.'),
    'power-outage': () => console.log('🔌 Power outage! Simulated network partition.')
  };

  const action = actions[type];
  if (!action) {
    console.error(`Unknown chaos type: ${type}`);
    return;
  }

  if (dryRun) {
    console.log(`[DRY RUN] Triggering: ${type}`);
  } else {
    action();
  }
}

program.parse();
