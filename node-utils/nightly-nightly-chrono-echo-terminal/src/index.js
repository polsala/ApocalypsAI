#!/usr/bin/env node

const args = process.argv.slice(2);

function parseArgs(args) {
  let message = '';
  let delay = 50;
  let glitchProbability = 0.05;
  let reverseProbability = 0.01;

  // Simple argument parsing
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '-d' || arg === '--delay') {
      delay = parseInt(args[++i], 10);
    } else if (arg === '-g' || arg === '--glitch-probability') {
      glitchProbability = parseFloat(args[++i]);
    } else if (arg === '-r' || arg === '--reverse-probability') {
      reverseProbability = parseFloat(args[++i]);
    } else if (!message) { // First non-option argument is the message
      message = arg;
    } else {
      console.error(`Error: Unknown argument or multiple messages provided: ${arg}`);
      process.exit(1);
    }
  }

  if (!message) {
    console.error('Usage: nightly-chrono-echo-terminal <message> [-d <delay>] [-g <glitch_prob>] [-r <reverse_prob>]');
    process.exit(1);
  }

  return { message, delay, glitchProbability, reverseProbability };
}

async function echoWithTemporalEffects(message, delay, glitchProbability, reverseProbability, stdoutWrite = process.stdout.write) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?/~`';

  const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

  let i = 0;
  while (i < message.length) {
    if (Math.random() < reverseProbability && i + 2 < message.length) { // Reverse a small segment (e.g., 3 chars)
      const segment = message.substring(i, i + 3);
      const reversedSegment = segment.split('').reverse().join('');
      for (let j = 0; j < reversedSegment.length; j++) {
        stdoutWrite(reversedSegment[j]);
        await sleep(delay);
      }
      i += 3;
    } else {
      let char = message[i];
      if (Math.random() < glitchProbability) {
        char = chars[Math.floor(Math.random() * chars.length)]; // Replace with a random char
      }
      stdoutWrite(char);
      await sleep(delay);
      i++;
    }
  }
  stdoutWrite('\n'); // Newline at the end
}

// Main execution block
if (require.main === module) {
  const { message, delay, glitchProbability, reverseProbability } = parseArgs(args);

  if (isNaN(delay) || delay < 0) {
    console.error('Error: Delay must be a non-negative number.');
    process.exit(1);
  }
  if (isNaN(glitchProbability) || glitchProbability < 0 || glitchProbability > 1) {
    console.error('Error: Glitch probability must be between 0 and 1.');
    process.exit(1);
  }
  if (isNaN(reverseProbability) || reverseProbability < 0 || reverseProbability > 1) {
    console.error('Error: Reverse probability must be between 0 and 1.');
    process.exit(1);
  }

  echoWithTemporalEffects(message, delay, glitchProbability, reverseProbability);
}

// For testing purposes, export the core functions
module.exports = { echoWithTemporalEffects, parseArgs };
