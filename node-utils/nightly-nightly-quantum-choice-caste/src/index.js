#!/usr/bin/env node

function runQuantumChoiceCaster(options, logFn = console.log, exitFn = process.exit) {
  if (options.length === 0) {
    logFn("🌌 ApocalypsAI Quantum Choice Caster 🌌");
    logFn("Usage: nightly-quantum-choice-caster <option1> <option2> [option3...]");
    logFn("\nExample: nightly-quantum-choice-caster \"Explore the ruins\" \"Scavenge for supplies\" \"Rest and repair\"");
    exitFn(1); // Still exit for the CLI, but can be mocked in tests
    return; // Ensure no further execution in CLI context after exit
  }

  const randomIndex = Math.floor(Math.random() * options.length);
  const chosenOption = options[randomIndex];

  const whimsicalMessages = [
    "The cosmic dice have rolled, revealing your path...",
    "A whisper from the void suggests...",
    "Ripples of possibility coalesce, and the universe points to...",
    "The Quantum Choice Caster hums, and your destiny unfolds as...",
    "Through the swirling nebulae, a clear choice emerges...",
    "The fabric of spacetime bends to reveal...",
    "Behold! The oracle has spoken, and it decrees..."
  ];

  const randomMessageIndex = Math.floor(Math.random() * whimsicalMessages.length);
  const chosenMessage = whimsicalMessages[randomMessageIndex];

  logFn(`\n${chosenMessage}\n`);
  logFn(`✨ ${chosenOption} ✨`);
  logFn("\nMay your choice lead to optimal temporal stability.");
}

// Only run if this file is executed directly (as a CLI)
if (require.main === module) {
  runQuantumChoiceCaster(process.argv.slice(2));
}

module.exports = runQuantumChoiceCaster; // Export for testing
