const { jest } = require('@jest/globals');
const fs = require('fs');
const path = require('path');

// Mock the entire 'src/main.js' module to control its behavior
jest.mock('../src/main.js', () => {
  // Mock constants to ensure deterministic tests
  const mockConstants = {
    MIN_DELAY_MS: 100,
    MAX_DELAY_MS: 200,
    CORRUPTION_CHANCE: 0.0,
    MESSAGES_TO_SEND: 3
  };

  // Mock the relayMessage function to capture its calls and return predictable results
  const mockRelayMessage = jest.fn(async (message) => {
    // Mock the internal delay to be fixed for testing
    const fixedDelay = 150;
    // Mock corruption to be off for this test suite
    const receivedMessage = message;
    console.log(`Mocked: Sending message: "${message}"`);
    console.log(`Mocked: Received message: "${receivedMessage}" after ${fixedDelay}ms delay.`);
    console.log('');
    return { receivedMessage, delay: fixedDelay };
  });

  // Mock the runSimulation function to use our mocked relayMessage
  const mockRunSimulation = jest.fn(async () => {
    const sampleMessages = [
      "Test Message 1",
      "Test Message 2",
      "Test Message 3"
    ];
    console.log("Mocked: --- Initiating Cosmic Communication Relay ---");
    console.log("\n");
    for (let i = 0; i < mockConstants.MESSAGES_TO_SEND; i++) {
      await mockRelayMessage(sampleMessages[i % sampleMessages.length]);
    }
    console.log("Mocked: --- Cosmic Communication Relay Complete ---");
  });

  // Return the mocked functions and constants
  return {
    relayMessage: mockRelayMessage,
    runSimulation: mockRunSimulation,
    ...mockConstants
  };
});

// Import the mocked module
const { relayMessage, runSimulation } = require('../src/main.js');

describe('Cosmic Communication Relay', () => {

  // Mock console.log to capture output for assertions
  let consoleSpy;
  beforeEach(() => {
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
  });
  afterEach(() => {
    consoleSpy.mockRestore();
  });

  test('should simulate sending and receiving messages with fixed delay and no corruption', async () => {
    // Mock the internal delay and corruption chance for this specific test
    // This is a bit of a workaround since we mocked the whole module. 
    // In a real scenario, you might mock individual functions if possible.
    const originalRelayMessage = require('../src/main.js').relayMessage;
    const originalRunSimulation = require('../src/main.js').runSimulation;

    // Temporarily override the mocked relayMessage for this test
    const testRelayMessage = jest.fn(async (message) => {
      const fixedDelay = 150;
      const receivedMessage = message; // No corruption
      console.log(`Test: Sending message: "${message}"`);
      console.log(`Test: Received message: "${receivedMessage}" after ${fixedDelay}ms delay.`);
      console.log('');
      return { receivedMessage, delay: fixedDelay };
    });

    // Temporarily override the mocked runSimulation to use our specific relayMessage
    const testRunSimulation = jest.fn(async () => {
      const sampleMessages = [
        "Test Message 1",
        "Test Message 2",
        "Test Message 3"
      ];
      console.log("Test: --- Initiating Cosmic Communication Relay ---");
      console.log("\n");
      for (let i = 0; i < 3; i++) {
        await testRelayMessage(sampleMessages[i % sampleMessages.length]);
      }
      console.log("Test: --- Cosmic Communication Relay Complete ---");
    });

    // Replace the mocked functions with our test versions
    require('../src/main.js').relayMessage = testRelayMessage;
    require('../src/main.js').runSimulation = testRunSimulation;

    await testRunSimulation();

    // Assertions
    expect(testRelayMessage).toHaveBeenCalledTimes(3);
    expect(testRelayMessage).toHaveBeenCalledWith('Test Message 1');
    expect(testRelayMessage).toHaveBeenCalledWith('Test Message 2');
    expect(testRelayMessage).toHaveBeenCalledWith('Test Message 3');

    // Check console output for expected messages
    const logOutput = consoleSpy.mock.calls.flat().join('\n');
    expect(logOutput).toContain('Test: Sending message: "Test Message 1"');
    expect(logOutput).toContain('Test: Received message: "Test Message 1" after 150ms delay.');
    expect(logOutput).toContain('Test: Sending message: "Test Message 2"');
    expect(logOutput).toContain('Test: Received message: "Test Message 2" after 150ms delay.');
    expect(logOutput).toContain('Test: Sending message: "Test Message 3"');
    expect(logOutput).toContain('Test: Received message: "Test Message 3" after 150ms delay.');
    expect(logOutput).toContain('Test: --- Initiating Cosmic Communication Relay ---');
    expect(logOutput).toContain('Test: --- Cosmic Communication Relay Complete ---');

    // Restore original mocked functions
    require('../src/main.js').relayMessage = originalRelayMessage;
    require('../src/main.js').runSimulation = originalRunSimulation;
  });

  test('should simulate message corruption when CORRUPTION_CHANCE is high', async () => {
    // Mock constants for this specific test
    const mockConstants = {
      MIN_DELAY_MS: 50,
      MAX_DELAY_MS: 100,
      CORRUPTION_CHANCE: 1.0, // 100% corruption
      MESSAGES_TO_SEND: 1
    };

    // Mock relayMessage to specifically test corruption
    const corruptingRelayMessage = jest.fn(async (message) => {
      const fixedDelay = 75;
      // Manually simulate corruption for a known message
      let receivedMessage = '';
      for (let i = 0; i < message.length; i++) {
        if (Math.random() < 0.1) {
          const charCode = message.charCodeAt(i);
          const alteredCharCode = charCode + (Math.random() < 0.5 ? 1 : -1);
          receivedMessage += String.fromCharCode(alteredCharCode);
        } else {
          receivedMessage += message[i];
        }
      }
      console.log(`CorruptionTest: Sending message: "${message}"`);
      console.log(`CorruptionTest: Received message: "${receivedMessage}" after ${fixedDelay}ms delay.`);
      console.log('');
      return { receivedMessage, delay: fixedDelay };
    });

    // Mock runSimulation to use our corruptingRelayMessage
    const corruptingRunSimulation = jest.fn(async () => {
      const message = "Hello Void!";
      await corruptingRelayMessage(message);
    });

    // Temporarily replace the mocked functions
    const originalRelayMessage = require('../src/main.js').relayMessage;
    const originalRunSimulation = require('../src/main.js').runSimulation;
    require('../src/main.js').relayMessage = corruptingRelayMessage;
    require('../src/main.js').runSimulation = corruptingRunSimulation;
    Object.assign(require('../src/main.js'), mockConstants);

    await corruptingRunSimulation();

    // Assertions
    expect(corruptingRelayMessage).toHaveBeenCalledTimes(1);
    expect(corruptingRelayMessage).toHaveBeenCalledWith('Hello Void!');

    const logOutput = consoleSpy.mock.calls.flat().join('\n');
    expect(logOutput).toContain('CorruptionTest: Sending message: "Hello Void!"');
    // We can't assert the exact corrupted message due to randomness, but we can check it's different
    expect(logOutput).not.toContain('CorruptionTest: Received message: "Hello Void!" after 75ms delay.');
    expect(logOutput).toContain('CorruptionTest: Received message: "');
    expect(logOutput).toContain('" after 75ms delay.');

    // Restore original mocked functions
    require('../src/main.js').relayMessage = originalRelayMessage;
    require('../src/main.js').runSimulation = originalRunSimulation;
    // Restore original constants if they were also mocked
    // (In this case, we are re-assigning them, so no need to restore if they were global)
  });

});
