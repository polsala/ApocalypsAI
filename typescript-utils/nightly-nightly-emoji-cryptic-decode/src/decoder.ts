export const emojiMap: Record<string, string[]> = {
  "🐱": ["cat"],
  "🚀": ["rocket"],
  "❤️": ["love", "heart"],
  "🌧️": ["rain"],
  "☀️": ["sun", "sunny"],
  "🍎": ["apple"],
  "⚡": ["lightning", "energy"],
  "🧠": ["brain", "mind"],
  "💧": ["water", "drop"],
  "🔥": ["fire", "hot"]
};

/**
 * Decode a whitespace‑separated string of emojis into possible meanings.
 *
 * @param input - Emoji string, tokens separated by whitespace.
 * @returns An array where each element corresponds to a token and contains
 *          an array of possible textual meanings (empty if unknown).
 */
export function decodeEmojis(input: string): string[][] {
  if (!input) {
    return [];
  }
  const tokens = input.trim().split(/\s+/);
  return tokens.map(token => emojiMap[token] ?? []);
}
