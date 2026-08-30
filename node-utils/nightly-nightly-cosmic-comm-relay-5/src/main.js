const EventEmitter = require('events');

class CosmicRelay extends EventEmitter {
    constructor() {
        super();
        this.messageQueue = [];
        this.isRelayActive = false;
        this.MAX_RETRIES = 3;
        this.ANOMALY_CHANCE = 0.3; // 30% chance of an anomaly
    }

    async sendMessage(message, destination = 'Galactic Hub') {
        if (!this.isRelayActive) {
            this.emit('error', 'Relay is offline. Cannot send message.');
            return;
        }

        console.log(`\n🚀 Transmitting message to ${destination}: "${message}"`);
        let retries = 0;

        while (retries < this.MAX_RETRIES) {
            try {
                const transmissionTime = this.simulateTransmissionTime();
                await this.delay(transmissionTime);

                if (this.simulateCosmicAnomaly()) {
                    throw new Error('Cosmic anomaly detected! Signal degraded.');
                }

                console.log(`✅ Message successfully delivered to ${destination} after ${transmissionTime}ms.`);
                this.emit('messageSent', { message, destination, time: new Date().toISOString() });
                return;
            } catch (error) {
                retries++;
                console.warn(`⚠️ Transmission failed (${retries}/${this.MAX_RETRIES}): ${error.message}. Retrying...`);
                await this.delay(1000); // Wait before retrying
            }
        }

        console.error(`❌ Failed to deliver message to ${destination} after multiple retries.`);
        this.emit('transmissionFailed', { message, destination });
    }

    receiveMessage(sender = 'Unknown Star System') {
        if (!this.isRelayActive) {
            console.log('Relay is offline. No messages can be received.');
            return;
        }

        const message = this.messageQueue.shift();
        if (message) {
            console.log(`\n🌌 Received message from ${sender}: "${message.message}" (Sent at: ${message.time})`);
            this.emit('messageReceived', message);
        } else {
            // console.log('No new messages in the queue.');
        }
    }

    startRelay() {
        console.log('✨ Cosmic Communication Relay is powering up...');
        this.isRelayActive = true;
        this.relayInterval = setInterval(() => {
            this.receiveMessage();
        }, 5000); // Check for messages every 5 seconds
        console.log('Cosmic Communication Relay is ONLINE and ready for transmissions!');
        this.emit('relayStarted');
    }

    stopRelay() {
        console.log('\n🔌 Cosmic Communication Relay is powering down...');
        this.isRelayActive = false;
        clearInterval(this.relayInterval);
        console.log('Cosmic Communication Relay is OFFLINE.');
        this.emit('relayStopped');
    }

    // --- Simulation Helpers ---

    simulateTransmissionTime() {
        // Simulate transmission times between 1s and 5s
        return Math.floor(Math.random() * 4000) + 1000;
    }

    simulateCosmicAnomaly() {
        return Math.random() < this.ANOMALY_CHANCE;
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// --- Main Execution ---

const relay = new CosmicRelay();

// Event listeners for feedback
relay.on('relayStarted', () => {
    console.log('Relay has successfully initiated its cosmic journey.');
});

relay.on('messageSent', (data) => {
    console.log(`Log: Message to ${data.destination} sent successfully.`);
});

relay.on('messageReceived', (data) => {
    console.log(`Log: Message from ${data.sender || 'Unknown'} processed.`);
});

relay.on('transmissionFailed', (data) => {
    console.error(`Log: Critical failure sending message to ${data.destination}.`);
});

relay.on('error', (errorMessage) => {
    console.error(`System Error: ${errorMessage}`);
});

// Start the relay and listen for user input
relay.startRelay();

process.stdin.setEncoding('utf8');
process.stdin.on('data', (input) => {
    const message = input.trim();
    if (message.toLowerCase() === 'exit') {
        relay.stopRelay();
        process.exit(0);
    } else if (message) {
        relay.messageQueue.push({ message, time: new Date().toISOString() });
        console.log('Message queued for transmission.');
    }
});

process.on('SIGINT', () => {
    relay.stopRelay();
    process.exit(0);
});
