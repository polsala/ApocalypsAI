class CosmicCommRelay {
  constructor(options = {}) {
    this.distance = options.distance || 100;
    this.baseDelayPerUnit = 50; // milliseconds per arbitrary distance unit
  }

  async sendMessage(message) {
    return new Promise((resolve, reject) => {
      const totalDelay = this.distance * this.baseDelayPerUnit + Math.random() * 500; // Add some random fluctuation

      setTimeout(() => {
        let processedMessage = message;
        // Simulate cosmic static
        if (Math.random() < 0.3) { // 30% chance of static
          const staticNoise = ['...crackle...', '...hiss...', '...static...', '...bzzt...'];
          processedMessage = staticNoise[Math.floor(Math.random() * staticNoise.length)] + ' ' + processedMessage;
        }
        // Simulate signal degradation
        if (Math.random() < 0.1) { // 10% chance of signal degradation
          processedMessage = processedMessage.split('').map(char => {
            if (Math.random() < 0.1) return String.fromCharCode(char.charCodeAt(0) + (Math.random() < 0.5 ? 1 : -1)); // Slightly alter character
            return char;
          }).join('');
        }

        resolve(processedMessage);
      }, totalDelay);
    });
  }
}

// CLI part
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: node src/main.js "<message>" [--distance <value>]');
    process.exit(1);
  }

  const message = args[0];
  let distance = 100;

  const distanceIndex = args.indexOf('--distance');
  if (distanceIndex !== -1 && args.length > distanceIndex + 1) {
    const parsedDistance = parseInt(args[distanceIndex + 1], 10);
    if (!isNaN(parsedDistance) && parsedDistance > 0) {
      distance = parsedDistance;
    } else {
      console.error('Invalid distance value. Please provide a positive number.');
      process.exit(1);
    }
  }

  const relay = new CosmicCommRelay({ distance });
  relay.sendMessage(message)
    .then(receivedMessage => {
      console.log(`Transmission successful (distance: ${distance}):`);
      console.log(`Received: ${receivedMessage}`);
    })
    .catch(err => {
      console.error('Transmission failed:', err);
      process.exit(1);
    });
}

module.exports = { CosmicCommRelay };
