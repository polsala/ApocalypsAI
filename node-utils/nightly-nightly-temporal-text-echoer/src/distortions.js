const GLITCH_SYMBOLS = '!@#$%^&*()_+-=[]{}|;:\'",.<>/?~';

function applyFading(text, intensity = 0.1) {
  if (intensity <= 0) return text;
  let result = '';
  for (const char of text) {
    if (Math.random() > intensity) {
      result += char;
    }
  }
  return result;
}

function applyGlitch(text, intensity = 0.05) {
  if (intensity <= 0) return text;
  let result = '';
  for (const char of text) {
    if (Math.random() < intensity) {
      result += GLITCH_SYMBOLS[Math.floor(Math.random() * GLITCH_SYMBOLS.length)];
    } else {
      result += char;
    }
  }
  return result;
}

function applyEcho(text, intensity = 0.02) {
  if (intensity <= 0) return text;
  const words = text.split(/(\s+)/); // Split by whitespace, keeping delimiters
  let resultParts = [];
  for (let i = 0; i < words.length; i++) {
    const word = words[i];
    resultParts.push(word);
    // Only echo if it's a non-empty word and contains alphanumeric characters
    if (word.trim().length > 1 && /[a-zA-Z0-9]/.test(word) && Math.random() < intensity) {
      resultParts.push('...', word);
    }
  }
  return resultParts.join('');
}

module.exports = {
  applyFading,
  applyGlitch,
  applyEcho,
  GLITCH_SYMBOLS
};
