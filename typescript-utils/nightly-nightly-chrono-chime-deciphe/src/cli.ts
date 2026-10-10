import { decipherChronoChime } from './index';

function runCli() {
  const args = process.argv.slice(2);
  const input = args.join(' ').trim();

  const result = decipherChronoChime(input);

  console.log(`\n--- Nightly Chrono-Chime Decipherer ---`);
  console.log(`Input: "${input || '[No Input]'}"`);
  console.log(`\nChrono-Chime: ${result.chime}`);
  console.log(`Whimsical Advice: ${result.advice}`);
  console.log(`---------------------------------------\n`);
}

runCli();
