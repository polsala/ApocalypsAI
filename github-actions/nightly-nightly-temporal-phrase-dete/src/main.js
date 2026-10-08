const core = require('@actions/core');

async function run() {
  try {
    const message = core.getInput('message', { required: true });
    const failOnParadox = core.getInput('fail-on-paradox') === 'true';

    const temporalPhrases = [
      'fixed a bug from next week',
      'reverted a future change',
      'applied a patch from 2077',
      'this commit is from another timeline',
      'pre-emptively fixed',
      'retroactively applied',
      'from the future',
      'from the past that hasn\'t happened',
      'temporal anomaly',
      'time warp',
      'chronal distortion'
    ];

    let paradoxDetected = false;
    const detectedPhrases = [];

    const lowerCaseMessage = message.toLowerCase();

    for (const phrase of temporalPhrases) {
      if (lowerCaseMessage.includes(phrase)) {
        paradoxDetected = true;
        detectedPhrases.push(phrase);
      }
    }

    core.setOutput('paradox-detected', paradoxDetected.toString());
    core.setOutput('detected-phrases', detectedPhrases.join(', '));

    if (paradoxDetected && failOnParadox) {
      core.setFailed(`Temporal paradox detected in message: "${message}". Phrases: ${detectedPhrases.join(', ')}`);
    } else if (paradoxDetected) {
      core.warning(`Temporal paradox detected in message: "${message}". Phrases: ${detectedPhrases.join(', ')}`);
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
