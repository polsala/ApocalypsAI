// Nightly Apocalypse Survival Tip Action
// Selects a random tip and sets it as the `tip` output.

const tips = [
  "Always keep a spare can‑of‑beans in your bunker.",
  "Never trust a solar panel that shines at night.",
  "Water is precious – drink it only after boiling.",
  "A well‑maintained radio can be louder than a herd of mutants.",
  "Map your escape routes; walls have ears."
];

// Allow deterministic selection via FORCE_RANDOM env var (0‑1 range).
let rand;
if (process.env.FORCE_RANDOM !== undefined) {
  const val = parseFloat(process.env.FORCE_RANDOM);
  rand = isNaN(val) ? Math.random() : Math.min(Math.max(val, 0), 1);
} else {
  rand = Math.random();
}

const index = Math.floor(rand * tips.length);
const selected = tips[index];

// Emit output using the GitHub Actions command syntax.
console.log(`::set-output name=tip::${selected}`);
