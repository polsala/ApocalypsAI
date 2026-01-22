// nightly-chaos-clock
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const chaosMessages = [
  "🌀 Temporal Anomaly Detected!",
  "👽 Alien Time Warp Engaged!",
  "👾 Glitch in the Matrix!",
  "👻 Spooky Time Shift!",
  "🤖 Robot Takeover Imminent!",
  "🦄 Unicorn Invasion Detected!",
  "🌮 Taco Tuesday Forever!",
  "⏰ Time is an illusion.",
  "🕰️ Clock broke. Oops.",
  "🎉 Party Time!",
];

function getRandomChaos() {
  const index = Math.floor(Math.random() * chaosMessages.length);
  return chaosMessages[index];
}

function displayTime() {
  const now = new Date();
  const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
  
  // 10% chance of chaos
  if (Math.random() < 0.1) {
    console.log(getRandomChaos());
  } else {
    console.log(`🕒 ${timeStr}`);
  }
}

console.log(' nightly-chaos-clock started. Press Ctrl+C to exit.');

const timer = setInterval(displayTime, 1000);

rl.on('SIGINT', () => {
  clearInterval(timer);
  console.log('\n\n🕒 Clock stopped. Goodbye!');
  process.exit(0);
});
