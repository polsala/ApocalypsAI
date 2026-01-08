const { CosmicRelay } = require('./cosmicRelay');
const { defineDialects } = require('./dialects');

// Define some whimsical dialects
const dialects = defineDialects({
  starlight_whisper: {
    prefix: "✨ ",
    suffix: " ✨",
    transform: (message) => message.toUpperCase()
  },
  void_mumble: {
    prefix: "(Mumbling from the abyss) ",
    suffix: "...",
    transform: (message) => {
      const words = message.split(' ');
      return words.reverse().join(' ');
    }
  },
  quantum_chatter: {
    prefix: "[Quantum Entanglement] ",
    suffix: " [Observer Effect]",
    transform: (message) => {
      // Adds a random character to each letter
      return message.split('').map(char => char + String.fromCharCode(Math.floor(Math.random() * 26) + 97)).join('');
    }
  }
});

// Initialize the relay with the defined dialects
const relay = new CosmicRelay(dialects);

// Register some cosmic entities
relay.registerEntity('Orion', 'starlight_whisper');
relay.registerEntity('Nebula', 'void_mumble');
relay.registerEntity('Quasar', 'quantum_chatter');
relay.registerEntity('CosmicDust', 'starlight_whisper'); // Can share dialects

// --- Demonstration ---
console.log("--- Cosmic Communication Relay Activated ---");

// Send a message from Orion to Nebula
console.log("\nSending message from Orion to Nebula...");
const orionMessage = "Greetings, dwellers of the void.";
const translatedOrionMessage = relay.sendMessage('Orion', 'Nebula', orionMessage);
console.log(`Orion says: "${orionMessage}"`);
console.log(`Nebula receives: "${translatedOrionMessage}"`);

// Send a message from Nebula to Quasar
console.log("\nSending message from Nebula to Quasar...");
const nebulaMessage = "The silence is deafening.";
const translatedNebulaMessage = relay.sendMessage('Nebula', 'Quasar', nebulaMessage);
console.log(`Nebula says: "${nebulaMessage}"`);
console.log(`Quasar receives: "${translatedNebulaMessage}"`);

// Send a message from Quasar to CosmicDust
console.log("\nSending message from Quasar to CosmicDust...");
const quasarMessage = "Is anyone out there?";
const translatedQuasarMessage = relay.sendMessage('Quasar', 'CosmicDust', quasarMessage);
console.log(`Quasar says: "${quasarMessage}"`);
console.log(`CosmicDust receives: "${translatedQuasarMessage}"`);

console.log("\n--- Cosmic Communication Relay Deactivated ---");
