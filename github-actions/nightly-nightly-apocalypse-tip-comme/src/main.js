const core = require('@actions/core');

const tips = [
  "Always keep a spare can of beans in your bunker.",
  "Water is life—purify it before you drink.",
  "Know your escape routes; the shortest path may be underground.",
  "Barter with batteries; they’re the new gold.",
  "Never trust a silent radio transmission.",
  "A well‑maintained flashlight beats a flashlight with fresh batteries.",
  "Map the stars; GPS may be dead.",
  "Learn to start a fire without matches.",
  "Keep a journal; history repeats itself.",
  "Stay calm; panic burns more calories than a fire."
];

// Select random tip
const tip = tips[Math.floor(Math.random() * tips.length)];
core.setOutput('tip', tip);
console.log(`Apocalypse tip: ${tip}`);
