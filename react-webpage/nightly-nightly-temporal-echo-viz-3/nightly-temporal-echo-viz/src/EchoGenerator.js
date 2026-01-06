const WHISPER_WORDS = ['...', ' (fades)', ' (distant)', ' (barely audible)'];
const SHIFT_WORDS = {
  'time': ['era', 'epoch', 'chronos', 'moment'],
  'future': ['tomorrow', 'beyond', 'eventuality'],
  'past': ['yesterday', 'before', 'history'],
  'void': ['abyss', 'emptiness', 'nothingness'],
  'message': ['whisper', 'signal', 'transmission', 'utterance'],
  'world': ['realm', 'domain', 'sphere', 'existence']
};
const VOID_PHRASES = ['[STATIC]', '[DISTORTION]', '[UNINTELLIGIBLE]', '[ECHOES FROM THE VOID]', '[FRAGMENTED]'];

/**
 * Generates a temporal echo of the input text based on the specified distortion type.
 * @param {string} text The original text to echo.
 * @param {'whisper' | 'shift' | 'void' | 'reverb'} type The type of distortion to apply.
 * @returns {string} The distorted echo text.
 */
export function generateEcho(text, type) {
  const words = text.split(/(\s+)/);
  let echoedText = [];

  switch (type) {
    case 'whisper':
      // Randomly remove words or replace with ellipses
      for (let i = 0; i < words.length; i++) {
        if (words[i].trim() === '') {
          echoedText.push(words[i]); // Preserve spaces
          continue;
        }
        if (Math.random() < 0.3) {
          echoedText.push(WHISPER_WORDS[Math.floor(Math.random() * WHISPER_WORDS.length)]);
        } else if (Math.random() < 0.1) {
          // Skip word entirely
        } else {
          echoedText.push(words[i]);
        }
      }
      return echoedText.join('').replace(/\s\.\.\./g, '...'); // Clean up spaces before ellipses

    case 'shift':
      // Replace certain words with synonyms or thematic alternatives
      for (let i = 0; i < words.length; i++) {
        const lowerWord = words[i].toLowerCase().replace(/[^a-z]/g, ''); // Clean word for lookup
        if (SHIFT_WORDS[lowerWord] && Math.random() < 0.6) {
          const replacements = SHIFT_WORDS[lowerWord];
          echoedText.push(replacements[Math.floor(Math.random() * replacements.length)] + words[i].replace(/[^a-z]/gi, ''));
        } else {
          echoedText.push(words[i]);
        }
      }
      return echoedText.join('');

    case 'void':
      // Add random cryptic phrases and heavily fragment text
      for (let i = 0; i < words.length; i++) {
        if (words[i].trim() === '') {
          echoedText.push(words[i]);
          continue;
        }
        if (Math.random() < 0.2) {
          echoedText.push(VOID_PHRASES[Math.floor(Math.random() * VOID_PHRASES.length)] + ' ');
        } else if (Math.random() < 0.4) {
          echoedText.push(words[i].slice(0, Math.floor(words[i].length / 2)) + '...');
        } else {
          echoedText.push(words[i]);
        }
      }
      return echoedText.join('');

    case 'reverb':
      // Repeat parts of the text or add echoes of words
      for (let i = 0; i < words.length; i++) {
        echoedText.push(words[i]);
        if (words[i].trim() !== '' && Math.random() < 0.15) {
          echoedText.push(`...${words[i].trim().toLowerCase()}...`);
        }
      }
      return echoedText.join('');

    default:
      return text;
  }
}
