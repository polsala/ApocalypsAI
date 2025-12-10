const core = require('@actions/core');

try {
  const tip = core.getInput('added_tip');
  core.info(`✅ Successfully added survival tip: ${tip}`);
} catch (error) {
  core.warning(`No tip added: ${error.message}`);
}
