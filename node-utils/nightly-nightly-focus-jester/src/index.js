const { execSync } = require('child_process');
const jokes = [
  'Why did the developer go broke? Because they used up all their cache!',
  'Why do programmers prefer dark mode? Because light attracts bugs!',
  'Why did the API break up? It needed space!'
];

function tellJoke() {
  const joke = jokes[Math.floor(Math.random() * jokes.length)];
  console.log(`\n⏰ Break Time! Here's a joke: ${joke}\n`);
}

function focusSession(minutes = 25) {
  console.log(`\n⏳ Starting ${minutes}-minute focus session...`);
  setTimeout(tellJoke, minutes * 60 * 1000);
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.includes('--help')) {
    console.log('Usage: focusjester [minutes]');
    process.exit(0);
  }
  const minutes = isNaN(args[0]) ? 25 : parseInt(args[0]);
  focusSession(minutes);
}

module.exports = { focusSession, tellJoke };
