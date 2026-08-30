#!/usr/bin/env node

const { program } = require('commander');
const { applyFading, applyGlitch, applyEcho } = require('./distortions');

program
  .name('temporal-text-echoer')
  .description('Applies whimsical temporal distortions to text.')
  .argument('<text>', 'The input text to distort, or "-" to read from stdin.')
  .option('-f, --fading <intensity>', 'Apply fading distortion (0-1, default 0.1)', parseFloat, 0.1)
  .option('-g, --glitch <intensity>', 'Apply glitch distortion (0-1, default 0.05)', parseFloat, 0.05)
  .option('-e, --echo <intensity>', 'Apply echo distortion (0-1, default 0.02)', parseFloat, 0.02)
  .action(async (inputText, options) => {
    let textToProcess = inputText;
    if (inputText === '-') {
      textToProcess = await readStdin();
    }

    let distortedText = textToProcess;
    if (options.fading > 0) {
      distortedText = applyFading(distortedText, options.fading);
    }
    if (options.glitch > 0) {
      distortedText = applyGlitch(distortedText, options.glitch);
    }
    if (options.echo > 0) {
      distortedText = applyEcho(distortedText, options.echo);
    }
    console.log(distortedText);
  });

program.parse(process.argv);

async function readStdin() {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.on('data', (chunk) => {
      data += chunk;
    });
    process.stdin.on('end', () => {
      resolve(data.trim());
    });
    process.stdin.on('error', (err) => {
      console.error('Error reading from stdin:', err);
      resolve('');
    });
  });
}
