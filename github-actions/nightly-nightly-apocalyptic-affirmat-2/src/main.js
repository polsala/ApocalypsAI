const core = require('@actions/core');

try {
  const target = core.getInput('target');

  const affirmations = [
    "Even in the digital wasteland, your code compiles. That's a win.",
    "The servers may be burning, but your commit history is pristine.",
    "A single line of well-tested code can rebuild a civilization. Or at least fix a bug.",
    "When the world ends, your README will still be there. Make it count.",
    "Your pull request is a beacon of hope in the encroaching darkness. Merge it with pride.",
    "The void whispers, but your tests shout 'PASS!'",
    "Amidst the ruins, your logic stands tall. Keep building.",
    "The apocalypse is just a refactor away. You've got this.",
    "Your debugging skills are sharper than any scavenged blade.",
    "May your dependencies be few and your uptime eternal.",
    "In the face of cosmic dread, your CI/CD pipeline remains green.",
    "The future is uncertain, but your functions are pure."
  ];

  const randomAffirmation = affirmations[Math.floor(Math.random() * affirmations.length)];

  core.setOutput('affirmation', randomAffirmation);

  if (target === 'summary') {
    core.summary.addRaw(`### 🌌 Apocalyptic Affirmation\n\n> _\"${randomAffirmation}\"_`).write();
  } else {
    core.info(`Apocalyptic Affirmation: "${randomAffirmation}"`);
  }

} catch (error) {
  core.setFailed(error.message);
}
