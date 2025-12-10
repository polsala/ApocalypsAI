type HaikuLine = {
  syllables: 5 | 7 | 5;
  words: string[];
};

const wordBanks = {
  5: ["Skies bleed crimson light,", "Zombie hordes march with drum,", "Hope drowns in silence."],
  7: ["Radiation blooms in fractured skies,", "Chaos dances on broken spines,", "Silent screams through hollow eyes."],
};

export function generateHaiku(theme: 'zombies' | 'radiation' | 'chaos'): string {
  const lines = [5, 7, 5];
  return lines.map(s => wordBanks[s][Math.floor(Math.random() * wordBanks[s].length)]).join('\n');
}
