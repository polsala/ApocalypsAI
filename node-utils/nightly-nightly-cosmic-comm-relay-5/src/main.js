const readline = require('readline');

// Simple XOR encryption/decryption function
function xorEncryptDecrypt(text, key) {
    let result = '';
    for (let i = 0; i < text.length; i++) {
        result += String.fromCharCode(text.charCodeAt(i) ^ key.charCodeAt(i % key.length));
    }
    return result;
}

// Simulate cosmic delay
function simulateCosmicDelay(distance) {
    return new Promise(resolve => {
        const delay = Math.log(distance + 1) * 50; // Logarithmic delay for a more 'cosmic' feel
        console.log(`Simulated travel time: ${delay.toFixed(0)}ms.`);
        setTimeout(resolve, delay);
    });
}

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

async function runCosmicCommRelay() {
    console.log('Welcome to the Cosmic Comm Relay!');

    rl.question('Choose mode (send/receive): ', async (mode) => {
        if (mode.toLowerCase() !== 'send' && mode.toLowerCase() !== 'receive') {
            console.log('Invalid mode. Please choose "send" or "receive".');
            rl.close();
            return;
        }

        rl.question('Enter your secret key: ', async (key) => {
            if (!key) {
                console.log('A secret key is required.');
                rl.close();
                return;
            }

            if (mode.toLowerCase() === 'send') {
                rl.question('Enter your message: ', async (message) => {
                    rl.question('Enter simulated cosmic distance (e.g., 10000): ', async (distanceStr) => {
                        const distance = parseInt(distanceStr, 10);
                        if (isNaN(distance) || distance <= 0) {
                            console.log('Invalid distance. Please enter a positive number.');
                            rl.close();
                            return;
                        }

                        console.log('\nTransmitting message...');
                        const encryptedMessage = xorEncryptDecrypt(message, key);
                        await simulateCosmicDelay(distance);
                        console.log('Message encrypted and sent across the void!');
                        console.log('Transmission complete.');
                        rl.close();
                    });
                });
            } else { // receive mode
                console.log('\nListening for transmissions...');
                // In a real scenario, this would involve network listeners.
                // For this standalone utility, we'll mock a received message after a delay.
                const mockDistance = Math.floor(Math.random() * 100000) + 1000; // Simulate a random distance
                await simulateCosmicDelay(mockDistance);

                // Mock received encrypted message (replace with actual network reception if applicable)
                const mockEncryptedMessage = xorEncryptDecrypt('Greetings from a distant star!', key);
                console.log('Incoming transmission detected!');
                const decryptedMessage = xorEncryptDecrypt(mockEncryptedMessage, key);
                console.log(`Message decrypted: ${decryptedMessage}`);
                rl.close();
            }
        });
    });
}

runCosmicCommRelay();
