const core = require('@actions/core');

try {
  const status = core.getInput('status', { required: true }).toLowerCase();
  const defaultEmoji = core.getInput('default-emoji');

  let emoji;
  switch (status) {
    case 'success':
      emoji = '🎉'; // Party popper
      break;
    case 'failure':
      emoji = '💥'; // Collision
      break;
    case 'cancelled':
      emoji = '🛑'; // Stop sign
      break;
    case 'skipped':
      emoji = '⏭️'; // Next track button
      break;
    case 'neutral': // For jobs that are just 'neutral'
      emoji = '⚪'; // White circle
      break;
    case 'waiting': // For jobs that are waiting
      emoji = '⏳'; // Hourglass not done
      break;
    case 'pending': // For jobs that are pending
      emoji = '⏳'; // Hourglass not done
      break;
    case 'running': // For jobs that are running
      emoji = '🏃'; // Running person
      break;
    default:
      emoji = defaultEmoji;
  }

  core.setOutput('emoji', emoji);
  core.info(`Status '${status}' translated to emoji: ${emoji}`);

} catch (error) {
  core.setFailed(error.message);
}
