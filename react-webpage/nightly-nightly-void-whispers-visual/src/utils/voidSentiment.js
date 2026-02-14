// Mock rationale: This utility simulates sentiment analysis without external APIs
// to ensure deterministic and offline testing. The logic is intentionally whimsical
// and based on simple string matching and text properties.

export function analyzeVoidSentiment(text) {
  const lowerText = text.toLowerCase();
  let hope = 0;
  let despair = 0;
  let whimsy = 0;
  let dread = 0;

  // Whimsical keyword matching
  if (lowerText.includes('hope') || lowerText.includes('future') || lowerText.includes('light')) {
    hope += 0.7;
  }
  if (lowerText.includes('star') || lowerText.includes('dream') || lowerText.includes('spark')) {
    hope += 0.5;
  }
  if (lowerText.includes('void') || lowerText.includes('dark') || lowerText.includes('end')) {
    despair += 0.8;
  }
  if (lowerText.includes('doom') || lowerText.includes('gloom') || lowerText.includes('abyss')) {
    despair += 0.6;
  }
  if (lowerText.includes('cat') || lowerText.includes('fluffy') || lowerText.includes('giggle')) {
    whimsy += 0.9;
  }
  if (lowerText.includes('banana') || lowerText.includes('wobble') || lowerText.includes('sparkle')) {
    whimsy += 0.7;
  }
  if (lowerText.includes('fear') || lowerText.includes('terror') || lowerText.includes('shiver')) {
    dread += 0.8;
  }
  if (lowerText.includes('unknown') || lowerText.includes('whisper') || lowerText.includes('shadow')) {
    dread += 0.5;
  }

  // Length and character-based modifiers
  const textLength = text.length;
  if (textLength > 50) {
    despair += 0.2; // Long texts can be daunting
    dread += 0.1;
  } else if (textLength < 10 && textLength > 0) {
    whimsy += 0.3; // Short texts can be punchy or silly
  }

  // Presence of punctuation
  if (/[!?]/.test(text)) {
    whimsy += 0.1;
  }
  if (/[...]/.test(text)) {
    dread += 0.1;
  }

  // Normalize scores to a 0-10 range for display
  const normalize = (score) => Math.min(10, Math.max(0, score * 2)); // No random for determinism

  return {
    hope: normalize(hope),
    despair: normalize(despair),
    whimsy: normalize(whimsy),
    dread: normalize(dread)
  };
}
