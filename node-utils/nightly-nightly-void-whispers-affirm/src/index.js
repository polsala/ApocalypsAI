#!/usr/bin/env node

const affirmations = [
  "Amidst the ruins, your resilience echoes louder than the silence.",
  "Even in the void, your light outshines the darkness.",
  "You are the architect of hope in a world of echoes.",
  "The wasteland trembles not before you, but because of you.",
  "In every step, you rewrite the end of the world.",
  "Your courage is the last magic the apocalypse couldn't break.",
  "Scars are just stories of how you refused to fall.",
  "You don't survive the end—you redefine it."
];

function getRandomAffirmation() {
  const index = Math.floor(Math.random() * affirmations.length);
  return affirmations[index];
}

console.log(getRandomAffirmation());
