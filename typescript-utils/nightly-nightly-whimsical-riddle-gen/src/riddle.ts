export interface Riddle {
  question: string;
  answer: string;
}

const riddles: Riddle[] = [
  {
    question: 'What has keys but can’t open locks?',
    answer: 'A piano.'
  },
  {
    question: 'I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?',
    answer: 'An echo.'
  },
  {
    question: 'What can travel around the world while staying in a corner?',
    answer: 'A stamp.'
  }
];

export function generateRiddle(): Riddle {
  const idx = Math.floor(Math.random() * riddles.length);
  return riddles[idx];
}
