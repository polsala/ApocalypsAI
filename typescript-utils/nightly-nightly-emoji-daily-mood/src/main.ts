export interface Mood {
  emoji: string;
  phrase: string;
}

const moods: Mood[] = [
  { emoji: '😀', phrase: 'You are awesome! Keep going!' },
  { emoji: '😢', phrase: 'It’s okay to feel down. Tomorrow is a new day.' },
  { emoji: '😎', phrase: 'Stay cool and keep coding!' },
  { emoji: '😴', phrase: 'Take a break, recharge, and return refreshed.' },
  { emoji: '🤔', phrase: 'Think big, dream bigger, and act boldly.' }
];

export function getMood(): Mood {
  const idx = Math.floor(Math.random() * moods.length);
  return moods[idx];
}

if (require.main === module) {
  const mood = getMood();
  console.log(`${mood.emoji} ${mood.phrase}`);
}
