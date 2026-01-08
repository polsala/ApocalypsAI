const assert = require('assert');
const { CosmicRelay } = require('../src/cosmicRelay');
const { defineDialects } = require('../src/dialects');

// Mock rationale: Using a simple object for dialects to avoid external dependencies.
const mockDialects = defineDialects({
  mock_sender: {
    prefix: "(S) ",
    transform: (msg) => `TRANSFORMED(${msg})`
  },
  mock_receiver: {
    suffix: " (R)"
  },
  mock_identity: {
    // No prefix, suffix, or transform
  }
});

describe('CosmicRelay', () => {
  it('should register an entity with a dialect', () => {
    const relay = new CosmicRelay(mockDialects);
    relay.registerEntity('TestEntity', 'mock_sender');
    assert.strictEqual(relay.entities['TestEntity'].dialectName, 'mock_sender', 'Entity not registered correctly');
  });

  it('should throw an error if dialect not found during registration', () => {
    const relay = new CosmicRelay(mockDialects);
    assert.throws(() => {
      relay.registerEntity('BadEntity', 'non_existent_dialect');
    }, /Dialect 'non_existent_dialect' not found./, 'Should throw dialect not found error');
  });

  it('should send a message with sender transformation and receiver prefix/suffix', () => {
    const relay = new CosmicRelay(mockDialects);
    relay.registerEntity('Sender', 'mock_sender');
    relay.registerEntity('Receiver', 'mock_receiver');
    const message = "Hello";
    const expected = "(S) TRANSFORMED(Hello) (R)";
    const actual = relay.sendMessage('Sender', 'Receiver', message);
    assert.strictEqual(actual, expected, 'Message not relayed and transformed correctly');
  });

  it('should handle entities with only identity dialects', () => {
    const relay = new CosmicRelay(mockDialects);
    relay.registerEntity('EntityA', 'mock_identity');
    relay.registerEntity('EntityB', 'mock_identity');
    const message = "Plain text";
    const expected = "Plain text";
    const actual = relay.sendMessage('EntityA', 'EntityB', message);
    assert.strictEqual(actual, expected, 'Identity dialect message not handled correctly');
  });

  it('should throw an error if sender entity is not registered', () => {
    const relay = new CosmicRelay(mockDialects);
    relay.registerEntity('Receiver', 'mock_receiver'); // Only register receiver
    assert.throws(() => {
      relay.sendMessage('UnregisteredSender', 'Receiver', 'Hi');
    }, /Sender entity 'UnregisteredSender' not registered./, 'Should throw unregistered sender error');
  });

  it('should throw an error if receiver entity is not registered', () => {
    const relay = new CosmicRelay(mockDialects);
    relay.registerEntity('Sender', 'mock_sender'); // Only register sender
    assert.throws(() => {
      relay.sendMessage('Sender', 'UnregisteredReceiver', 'Hi');
    }, /Receiver entity 'UnregisteredReceiver' not registered./, 'Should throw unregistered receiver error');
  });

  it('should apply sender transform and receiver prefix if only sender has transform and receiver has prefix', () => {
    const relay = new CosmicRelay(mockDialects);
    relay.registerEntity('SenderWithTransform', 'mock_sender');
    relay.registerEntity('ReceiverWithPrefix', 'mock_receiver'); // mock_receiver only has suffix
    relay.dialects['ReceiverWithPrefix'] = { prefix: '[P] ' }; // Override for this test
    const message = "Test";
    const expected = "(S) TRANSFORMED(Test) [P] "; // Note: mock_receiver has suffix, but we overrode it
    const actual = relay.sendMessage('SenderWithTransform', 'ReceiverWithPrefix', message);
    assert.strictEqual(actual, expected, 'Should apply sender transform and receiver prefix correctly');
  });

  it('should apply sender transform and receiver suffix if only sender has transform and receiver has suffix', () => {
    const relay = new CosmicRelay(mockDialects);
    relay.registerEntity('SenderWithTransform', 'mock_sender');
    relay.registerEntity('ReceiverWithSuffix', 'mock_receiver');
    const message = "Test";
    const expected = "(S) TRANSFORMED(Test) (R)";
    const actual = relay.sendMessage('SenderWithTransform', 'ReceiverWithSuffix', message);
    assert.strictEqual(actual, expected, 'Should apply sender transform and receiver suffix correctly');
  });
});
