import * as readline from 'readline';

interface DistortionOptions {
  charOmissionChance?: number; // Chance to omit a character (0-1)
  charDuplicationChance?: number; // Chance to duplicate a character (0-1)
  wordEchoChance?: number; // Chance to echo a word (0-1)
  staticInsertionChance?: number; // Chance to insert static (0-1)
  staticContent?: string[]; // Array of strings to insert as static
  minEchoLength?: number; // Minimum length of word to echo for it to be eligible for echoing
}

const defaultOptions: Required<DistortionOptions> = {
  charOmissionChance: 0.02,
  charDuplicationChance: 0.01,
  wordEchoChance: 0.05,
  staticInsertionChance: 0.03,
  staticContent: ['[...void static...]', '[...temporal hum...]', '[...echo fade...]'],
  minEchoLength: 3,
};

/**
 * Distorts a given text to simulate an echo through a void.
 * Applies character omissions, duplications, word echoes, and static insertions.
 * @param text The input text to distort.
 * @param options Configuration for distortion.
 * @returns The distorted text.
 */
export function distortText(text: string, options?: DistortionOptions): string {
  const opts = { ...defaultOptions, ...options };
  let distortedWords: string[] = [];
  const words = text.split(/(\s+)/).filter(s => s.length > 0); // Split by whitespace, keeping whitespace as separate elements

  for (let i = 0; i < words.length; i++) {
    const segment = words[i];

    if (segment.match(/^\s+$/)) {
      // If it's just whitespace, add it directly without distortion
      distortedWords.push(segment);
      continue;
    }

    let currentSegmentChars: string[] = [];
    for (const char of segment) {
      if (Math.random() < opts.charOmissionChance) {
        continue; // Omit character
      }
      currentSegmentChars.push(char);
      if (Math.random() < opts.charDuplicationChance) {
        currentSegmentChars.push(char); // Duplicate character
      }
    }

    let processedSegment = currentSegmentChars.join('');

    if (processedSegment.length >= opts.minEchoLength && Math.random() < opts.wordEchoChance) {
      // Echo word: take a prefix and append it in lowercase
      const echoPart = processedSegment.substring(0, Math.min(processedSegment.length, 3)).toLowerCase();
      processedSegment += `...${echoPart}`;
    }

    distortedWords.push(processedSegment);

    if (Math.random() < opts.staticInsertionChance) {
      // Insert static after a word/segment (but not after trailing whitespace)
      if (!segment.match(/^\s+$/) && i + 1 < words.length && words[i+1].match(/^\s+$/)) {
        // If next segment is whitespace, insert static before it
        const staticFragment = opts.staticContent[Math.floor(Math.random() * opts.staticContent.length)];
        distortedWords.push(staticFragment);
        distortedWords.push(words[i+1]); // Add the whitespace after static
        i++; // Skip next segment as it's already handled
      } else if (!segment.match(/^\s+$/)) {
        // If no trailing whitespace, just add static
        const staticFragment = opts.staticContent[Math.floor(Math.random() * opts.staticContent.length)];
        distortedWords.push(staticFragment);
      }
    }
  }

  return distortedWords.join('');
}

// CLI execution
if (require.main === module) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  console.log("ApocalypsAI Nightly Echo-Text Distorter");
  console.log("Enter text to send through the void (Ctrl+D or Ctrl+C to finish):\n");

  let inputText = '';
  rl.on('line', (line) => {
    inputText += line + '\n';
  });

  rl.on('close', () => {
    if (inputText.trim().length > 0) {
      const distorted = distortText(inputText.trim());
      console.log('\n--- Transmitted through the void ---');
      console.log(distorted);
      console.log('------------------------------------');
    } else {
      console.log('No text entered. Exiting.');
    }
    process.exit(0);
  });
}
