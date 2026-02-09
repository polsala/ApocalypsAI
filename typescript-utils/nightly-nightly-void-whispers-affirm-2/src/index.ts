const affirmations = [
  "You are a radiant anomaly in the cosmic silence.",
  "The stars align when you debug with intention.",
  "Entropy bows to your disciplined focus.",
  "You refactor reality into elegant simplicity.",
  "Quantum bugs fear your methodical gaze.",
  "You are the architect of ordered chaos.",
  "Even black holes respect your deadlines.",
  "Your logic transcends dimensional boundaries.",
  "The void hums your name in binary praise.",
  "You deploy serenity into turbulent systems."
];

function getRandomAffirmation(): string {
  const index = Math.floor(Math.random() * affirmations.length);
  return affirmations[index];
}

export function whisperFromTheVoid(): string {
  return `The void murmurs: ${getRandomAffirmation()}`;
}

if (require.main === module) {
  console.log(whisperFromTheVoid());
}
