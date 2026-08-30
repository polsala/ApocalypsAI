const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const patternInput = core.getInput('pattern', { required: true });
    const minLength = parseInt(core.getInput('min-length', { required: true }), 10);
    const failOnMismatch = core.getInput('fail-on-mismatch', { required: true }) === 'true';

    const prTitle = github.context.payload.pull_request ? github.context.payload.pull_request.title : null;

    if (!prTitle) {
      const message = 'Could not retrieve PR title. This action only runs on pull_request events.';
      core.setFailed(message);
      core.setOutput('is-whimsical', false);
      core.setOutput('message', message);
      return;
    }

    core.info(`Checking PR title: "${prTitle}"`);
    core.info(`Required pattern: "${patternInput}"`);
    core.info(`Minimum length: ${minLength}`);

    let isWhimsical = true;
    let failureMessages = [];

    // 1. Check pattern
    const regex = new RegExp(patternInput);
    if (!regex.test(prTitle)) {
      isWhimsical = false;
      failureMessages.push(`Title does not match required pattern: "${patternInput}"`);
    }

    // 2. Check minimum length
    if (prTitle.length < minLength) {
      isWhimsical = false;
      failureMessages.push(`Title is too short (${prTitle.length} chars). Minimum required: ${minLength} chars.`);
    }

    let resultMessage;
    if (isWhimsical) {
      resultMessage = `PR title "${prTitle}" is wonderfully whimsical!`;
      core.info(resultMessage);
      core.setOutput('is-whimsical', true);
      core.setOutput('message', resultMessage);
    } else {
      resultMessage = `PR title "${prTitle}" is not whimsical enough: ${failureMessages.join('; ')}`;
      core.warning(resultMessage);
      core.setOutput('is-whimsical', false);
      core.setOutput('message', resultMessage);
      if (failOnMismatch) {
        core.setFailed(resultMessage);
      }
    }

  } catch (error) {
    core.setFailed(error.message);
    core.setOutput('is-whimsical', false);
    core.setOutput('message', `Action failed with error: ${error.message}`);
  }
}

run();
