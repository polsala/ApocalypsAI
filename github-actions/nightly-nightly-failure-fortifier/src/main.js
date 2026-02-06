const core = require('@actions/core');

async function run() {
  try {
    const messagesInput = core.getInput('messages', { required: true });
    const fallbackMessage = core.getInput('fallback_message');

    const messageList = messagesInput
      .split(/\r?\n/)
      .map(line => line.trim())
      .filter(line => line.length > 0)
      .map(line => line.replace(/^"|"$/g, '')); // Remove surrounding quotes if present

    let chosenMessage;

    if (messageList.length === 0) {
      chosenMessage = fallbackMessage;
      core.info('No valid messages provided. Using fallback message.');
    } else {
      const randomIndex = Math.floor(Math.random() * messageList.length);
      chosenMessage = messageList[randomIndex];
      core.info(`Selected message: \"${chosenMessage}\"`)
    }

    core.summary.addRaw(`### 🌌 Wasteland Wisdom:\n\n${chosenMessage}\n\n`);
    core.info('Fortifying message added to workflow summary.');

  } catch (error) {
    core.setFailed(`Action failed with error: ${error.message}`);
  }
}

run();
