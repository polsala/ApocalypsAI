const core = require('@actions/core');

try {
  const prTitle = core.getInput('pr-title');
  const commitMessagesInput = core.getInput('commit-messages');
  const commitMessages = commitMessagesInput.split('\n').filter(msg => msg.trim() !== '');
  const inputCurrentYear = core.getInput('current-year');
  const currentYear = inputCurrentYear ? parseInt(inputCurrentYear, 10) : new Date().getFullYear();

  const temporalKeywords = [
    'time travel', 'paradox', 'flux capacitor', 'chronal', 'temporal rift',
    'future past', 'past future', 'time-warp', 'event horizon', 'pre-emptive fix',
    'retroactive patch', 'anachronism'
  ];

  const yearRegex = /\b(19|20)\d{2}\b/g; // Matches 19xx or 20xx years

  let isAnomalous = false;
  const anomalyDetails = [];

  const checkText = (text, source) => {
    // Check for keywords
    for (const keyword of temporalKeywords) {
      if (text.toLowerCase().includes(keyword)) {
        isAnomalous = true;
        anomalyDetails.push(`Keyword anomaly detected in ${source}: "${keyword}" found.`);
      }
    }

    // Check for year discrepancies
    let match;
    while ((match = yearRegex.exec(text)) !== null) {
      const yearInText = parseInt(match[0], 10);
      const yearDifference = yearInText - currentYear;

      if (yearDifference > 2) { // More than 2 years in the future
        isAnomalous = true;
        anomalyDetails.push(`Future year anomaly detected in ${source}: "${yearInText}" is ${yearDifference} years in the future.`);
      } else if (yearDifference < -5) { // More than 5 years in the past
        isAnomalous = true;
        anomalyDetails.push(`Past year anomaly detected in ${source}: "${yearInText}" is ${Math.abs(yearDifference)} years in the past.`);
      }
    }
  };

  checkText(prTitle, 'PR Title');
  commitMessages.forEach((msg, index) => checkText(msg, `Commit Message #${index + 1}`));

  core.setOutput('is-anomalous', isAnomalous);
  core.setOutput('anomaly-details', anomalyDetails.join('\n'));

  if (isAnomalous) {
    core.warning('Temporal anomalies detected! Please review the PR for chronological consistency.');
  } else {
    core.info('No temporal anomalies detected. Chronology is stable.');
  }

} catch (error) {
  core.setFailed(error.message);
}
