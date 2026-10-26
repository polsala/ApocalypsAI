const core = require('@actions/core');

function selectEmoji(message) {
  const len = message.length;
  if (len < 20) return '🚀';
  if (len <= 50) return '🌟';
  return '🐢';
}

function run() {
  try {
    const message = core.getInput('message', { required: true });
    const emoji = selectEmoji(message);
    core.setOutput('emoji', emoji);
    console.log(`Selected emoji: ${emoji}`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

// Export for testing
module.exports = { selectEmoji };

if (require.main === module) {
  run();
}
