const { execSync } = require('child_process');

// Helper to emit GitHub Action outputs (compatible with older syntax)
function setOutput(name, value) {
  console.log(`::set-output name=${name}::${value}`);
}

// Retrieve the latest commit hash and message
function getLatestCommitMessage() {
  const hash = execSync('git rev-parse HEAD').toString().trim();
  const message = execSync(`git log -1 --pretty=%B ${hash}`).toString().trim();
  return { hash, message };
}

// List of emojis to choose from
const EMOJIS = [
  '🚀', '✨', '🔥', '🌟', '🛸', '🤖', '🧩', '🎉', '💡', '🦄'
];

function pickEmoji() {
  const idx = Math.floor(Math.random() * EMOJIS.length);
  return EMOJIS[idx];
}

function run() {
  const { hash, message } = getLatestCommitMessage();
  const emoji = pickEmoji();
  const newMessage = `${message} ${emoji}`;

  // Emit the new message as an output
  setOutput('new_message', newMessage);

  // If the user requested a new commit, amend the latest commit
  const commitFlag = (process.env.INPUT_COMMIT || 'false').toLowerCase();
  if (commitFlag === 'true') {
    // Amend the commit without changing the author/date
    execSync(`git commit --amend -m "${newMessage.replace(/"/g, '\\"')}"`);
    // Push the amended commit (force-with-lease) – optional, omitted for safety
  }
}

try {
  run();
} catch (error) {
  console.error('Error in Commit Emoji Enhancer:', error.message);
  process.exit(1);
}
