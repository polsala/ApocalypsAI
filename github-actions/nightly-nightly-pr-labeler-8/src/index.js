const fs = require('fs');

// Path to the event payload provided by GitHub Actions
const eventPath = process.env.GITHUB_EVENT_PATH;
let title = '';
if (eventPath && fs.existsSync(eventPath)) {
  try {
    const payload = JSON.parse(fs.readFileSync(eventPath, 'utf8'));
    title = (payload.pull_request && payload.pull_request.title) || '';
  } catch (e) {
    // If parsing fails, keep title empty
  }
}

const labels = [];
if (/bug/i.test(title)) labels.push('bug');
if (/feature/i.test(title)) labels.push('enhancement');
if (/doc|documentation/i.test(title)) labels.push('documentation');

const emojis = ['🚀', '🐛', '✨', '📚', '⚡'];
const randomEmoji = emojis[Math.floor(Math.random() * emojis.length)];
labels.push(randomEmoji);

// Emit the output in the format expected by GitHub Actions
console.log(`::set-output name=labels::${labels.join(',')}`);
