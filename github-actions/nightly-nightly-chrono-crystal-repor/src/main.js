const core = require('@actions/core');
const github = require('@actions/github');

try {
  const status = core.getInput('status', { required: true });
  const repoToken = core.getInput('repo-token', { required: true });

  const successOmens = [
    "The Chrono-Crystal hums with harmonious resonance. All temporal threads are aligned. Stability achieved!",
    "A shimmering aura emanates from the Chrono-Crystal. The future is bright, the past is secure. Success is etched in time!",
    "The Chrono-Crystal pulses with vibrant energy. No temporal distortions detected. The cosmic dance continues flawlessly!",
    "Whispers of triumph echo through the Chrono-Crystal. The fabric of reality holds firm. A perfect temporal alignment!",
    "The Chrono-Crystal glows with serene light. The timelines are pristine, the anomalies banished. All is well in the temporal realm!"
  ];

  const failureOmens = [
    "The Chrono-Crystal shudders, emitting a discordant hum. Temporal anomalies detected! The fabric of reality is stressed!",
    "Dark fissures appear within the Chrono-Crystal. A ripple in the timeline, a shadow of chaos. Recalibration is urgently needed!",
    "The Chrono-Crystal flickers erratically. Temporal echoes of failure reverberate. The cosmic balance is disturbed!",
    "A chilling silence falls upon the Chrono-Crystal. The threads of fate are tangled. The future is uncertain, the past fractured!",
    "The Chrono-Crystal cracks, threatening to shatter. A grave omen of instability. Immediate temporal intervention required!"
  ];

  const cancelledOmens = [
    "The Chrono-Crystal dims, its purpose unfulfilled. Temporal flow halted by external forces. The path diverged, the outcome unknown.",
    "A faint echo lingers in the Chrono-Crystal. The journey was cut short, the prophecy unwritten. A pause in the temporal tapestry.",
    "The Chrono-Crystal enters a state of temporal stasis. No conclusion, merely an interruption. The cosmic clock awaits restart."
  ];

  let reportMessage;
  let emoji;

  switch (status.toLowerCase()) {
    case 'success':
      reportMessage = successOmens[Math.floor(Math.random() * successOmens.length)];
      emoji = '✨';
      break;
    case 'failure':
      reportMessage = failureOmens[Math.floor(Math.random() * failureOmens.length)];
      emoji = '🚨';
      break;
    case 'cancelled':
      reportMessage = cancelledOmens[Math.floor(Math.random() * cancelledOmens.length)];
      emoji = '⏸️';
      break;
    case 'skipped':
      reportMessage = "The Chrono-Crystal observes a skipped temporal path. No omens are revealed for this untraveled timeline.";
      emoji = '⏭️';
      break;
    case 'neutral':
      reportMessage = "The Chrono-Crystal remains neutral, observing the temporal flow without strong omens. All is in balance.";
      emoji = '😐';
      break;
    default:
      reportMessage = `The Chrono-Crystal observes an unknown temporal state: '${status}'. Its omens are yet unwritten.`;
      emoji = '❓';
  }

  const finalReport = `${emoji} **Chrono-Crystal Status Report:** ${reportMessage}`;

  // Post as workflow summary
  core.summary.addRaw(finalReport).write();

  // Set output for other steps
  core.setOutput('report-message', finalReport);

  console.log(finalReport);

} catch (error) {
  core.setFailed(error.message);
}
