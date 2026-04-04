const core = require('@actions/core');
const github = require('@actions/github');

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

function isInOffPeak(currentHour, startHour, endHour) {
  if (startHour <= endHour) {
    return currentHour >= startHour && currentHour < endHour;
  } else {
    return currentHour >= startHour || currentHour < endHour;
  }
}

async function run() {
  try {
    const probability = parseFloat(core.getInput('probability'));
    const startHour = parseInt(core.getInput('start_hour'), 10);
    const endHour = parseInt(core.getInput('end_hour'), 10);
    const dryRun = core.getBooleanInput('dry_run');

    const now = new Date();
    const currentHour = now.getUTCHours();
    
    console.log(`Current UTC time: ${now.toISOString()}, Hour: ${currentHour}`);
    console.log(`Checking if within off-peak hours (${startHour} to ${endHour})`);
    
    if (!isInOffPeak(currentHour, startHour, endHour)) {
      console.log('Not within off-peak window. Skipping chaos event.');
      core.setOutput('event_scheduled', 'false');
      return;
    }

    const shouldSchedule = Math.random() < probability;
    
    if (shouldSchedule) {
      const eventType = ['network-latency', 'cpu-throttle', 'memory-leak'][getRandomInt(3)];
      console.log(`🎲 Chaos event scheduled: ${eventType}`);
      
      if (!dryRun) {
        // In a real implementation, this would trigger actual chaos
        console.log(`💥 Triggering ${eventType} in production environment.`);
      } else {
        console.log('(Dry run mode - no actual disruption occurred)');
      }
      
      core.setOutput('event_scheduled', 'true');
    } else {
      console.log('🎲 No chaos event scheduled this time.');
      core.setOutput('event_scheduled', 'false');
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
