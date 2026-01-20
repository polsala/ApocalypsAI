export type Affirmation = string;

const templates: string[] = [
  "Even in the wasteland, your {strength} is a beacon.",
  "The void whispers: '{message}'.",
  "In the ruins, {noun} blooms anew.",
  "Your {trait} echoes across the expanse.",
  "Though the sky is ash, your {symbol} shines."
];

const strengths: string[] = ["bravery", "wit", "resilience", "hope"];
const messages: string[] = ["you are not forgotten", "tomorrow is yours", "the echo remains"];
const nouns: string[] = ["hope", "silence", "light", "memory"];
const traits: string[] = ["voice", "stride", "gaze", "touch"];
const symbols: string[] = ["compass", "flame", "star", "map"];

function getRandom<T>(arr: T[]): T {
  const index = Math.floor(Math.random() * arr.length);
  return arr[index];
}

export function generateAffirmation(): Affirmation {
  const template = getRandom(templates);
  return template
    .replace("{strength}", getRandom(strengths))
    .replace("{message}", getRandom(messages))
    .replace("{noun}", getRandom(nouns))
    .replace("{trait}", getRandom(traits))
    .replace("{symbol}", getRandom(symbols));
}
