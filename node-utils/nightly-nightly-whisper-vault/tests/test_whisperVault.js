const WhisperVault = require('../src/whisperVault');
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const crypto = require('crypto');

// Mock rationale: To ensure deterministic tests without actual file system interaction
// and to control time for TTL expiry tests, fs and Date.now() are mocked.
// The encryption key is fixed for test consistency.

const VAULT_TEST_FILE = path.join(__dirname, '.test_whisper_vault.json');
const TEST_ENCRYPTION_KEY = 'a_very_secret_test_key_32_bytes_long'; // 32 bytes

let mockVaultContent = null;

// Mock fs module
const originalFs = { ...fs };
fs.existsSync = (filePath) => filePath === VAULT_TEST_FILE && mockVaultContent !== null;
fs.readFileSync = (filePath, encoding) => {
    if (filePath === VAULT_TEST_FILE) {
        return mockVaultContent;
    }
    return originalFs.readFileSync(filePath, encoding);
};
fs.writeFileSync = (filePath, content, encoding) => {
    if (filePath === VAULT_TEST_FILE) {
        mockVaultContent = content;
    } else {
        originalFs.writeFileSync(filePath, content, encoding);
    }
};

// Mock Date.now() for time-based tests
const originalDateNow = Date.now;
let mockDateNow = originalDateNow();
Date.now = () => mockDateNow;

function resetMocks() {
    mockVaultContent = null;
    mockDateNow = originalDateNow();
}

function runTest(name, testFunction) {
    resetMocks();
    try {
        testFunction();
        console.log(`\u2713 ${name}`);
    } catch (error) {
        console.error(`\u2717 ${name}`);
        console.error(error);
        process.exit(1);
    }
}

runTest('should initialize an empty vault if file does not exist', () => {
    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    assert.deepStrictEqual(vault.vault, { whispers: [] });
});

runTest('should load existing vault content', () => {
    const testWhisper = {
        id: 'test-id-1',
        encryptedContent: 'encrypted-data-1',
        createdAt: 1678886400000,
        expiresAt: null,
        iv: 'test-iv-1'
    };
    // Mock the encryption process for the initial load
    const mockEncrypt = (text) => ({
        iv: 'mock-iv-for-vault-content',
        encryptedData: 'mock-encrypted-vault-content'
    });
    const mockDecrypt = (encryptedData, ivHex) => {
        if (encryptedData === 'mock-encrypted-vault-content') {
            return JSON.stringify({ whispers: [testWhisper] });
        }
        throw new Error('Unexpected decryption call');
    };

    const originalEncrypt = WhisperVault.prototype._encrypt;
    const originalDecrypt = WhisperVault.prototype._decrypt;
    WhisperVault.prototype._encrypt = mockEncrypt;
    WhisperVault.prototype._decrypt = mockDecrypt;

    mockVaultContent = JSON.stringify({
        iv: 'mock-iv-for-vault-content',
        encryptedData: 'mock-encrypted-vault-content'
    });

    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    assert.strictEqual(vault.vault.whispers.length, 1);
    assert.strictEqual(vault.vault.whispers[0].id, 'test-id-1');

    WhisperVault.prototype._encrypt = originalEncrypt;
    WhisperVault.prototype._decrypt = originalDecrypt;
});

runTest('should add a new whisper', () => {
    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    const message = 'Hello, secret world!';
    const id = vault.addWhisper(message);

    assert.strictEqual(vault.vault.whispers.length, 1);
    assert.strictEqual(typeof id, 'string');
    assert.ok(vault.vault.whispers[0].encryptedContent);
    assert.ok(vault.vault.whispers[0].iv);
    assert.strictEqual(vault.vault.whispers[0].expiresAt, null);

    // Verify content is encrypted and can be decrypted
    const decrypted = vault._decrypt(vault.vault.whispers[0].encryptedContent, vault.vault.whispers[0].iv);
    assert.strictEqual(decrypted, message);
});

runTest('should add a whisper with TTL', () => {
    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    const message = 'Temporary thought.';
    const ttlHours = 1;
    const id = vault.addWhisper(message, ttlHours);

    assert.strictEqual(vault.vault.whispers.length, 1);
    assert.ok(vault.vault.whispers[0].expiresAt);
    assert.strictEqual(vault.vault.whispers[0].expiresAt, mockDateNow + ttlHours * 60 * 60 * 1000);
});

runTest('should list active whispers', () => {
    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    vault.addWhisper('Whisper 1');
    vault.addWhisper('Whisper 2', 2);

    const listed = vault.listWhispers();
    assert.strictEqual(listed.length, 2);
    assert.ok(listed[0].id);
    assert.ok(listed[1].id);
});

runTest('should not list expired whispers', () => {
    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    vault.addWhisper('Active whisper');
    vault.addWhisper('Expired whisper', 1); // Expires in 1 hour

    mockDateNow += 2 * 60 * 60 * 1000; // Advance time by 2 hours

    const listed = vault.listWhispers();
    assert.strictEqual(listed.length, 1);
    assert.ok(listed[0].createdAt.includes(new Date(originalDateNow()).getFullYear())); // Check year to ensure date format
});

runTest('should reveal a specific whisper', () => {
    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    const message = 'Secret content to reveal.';
    const id = vault.addWhisper(message);

    const revealedContent = vault.revealWhisper(id);
    assert.strictEqual(revealedContent, message);
});

runTest('should return null for non-existent whisper', () => {
    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    const content = vault.revealWhisper('non-existent-id');
    assert.strictEqual(content, null);
});

runTest('should return null and purge expired whisper when revealed', () => {
    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    const message = 'Expired secret.';
    const id = vault.addWhisper(message, 1); // Expires in 1 hour

    mockDateNow += 2 * 60 * 60 * 1000; // Advance time by 2 hours

    const content = vault.revealWhisper(id);
    assert.strictEqual(content, null);
    assert.strictEqual(vault.vault.whispers.length, 0); // Should be purged
});

runTest('should purge all expired whispers', () => {
    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    vault.addWhisper('Active 1');
    vault.addWhisper('Expired 1', 1);
    vault.addWhisper('Active 2');
    vault.addWhisper('Expired 2', 0.5);

    mockDateNow += 1.5 * 60 * 60 * 1000; // Advance time past both expired whispers

    const purgedCount = vault.purgeExpired();
    assert.strictEqual(purgedCount, 2);
    assert.strictEqual(vault.vault.whispers.length, 2);
    assert.ok(vault.vault.whispers.every(w => !w.expiresAt || w.expiresAt > mockDateNow));
});

runTest('should handle empty vault during purge', () => {
    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    const purgedCount = vault.purgeExpired();
    assert.strictEqual(purgedCount, 0);
    assert.strictEqual(vault.vault.whispers.length, 0);
});

runTest('should derive a 32-byte key from a shorter key', () => {
    const shortKey = 'short';
    const vault = new WhisperVault(VAULT_TEST_FILE, shortKey);
    assert.strictEqual(vault.encryptionKey.length, 32);
    assert.ok(vault.encryptionKey instanceof Buffer);
});

runTest('should derive a 32-byte key from a longer key', () => {
    const longKey = 'this_is_a_very_long_key_that_is_definitely_more_than_32_bytes_long';
    const vault = new WhisperVault(VAULT_TEST_FILE, longKey);
    assert.strictEqual(vault.encryptionKey.length, 32);
    assert.ok(vault.encryptionKey instanceof Buffer);
});

runTest('should use the key directly if it is 32 bytes', () => {
    const key = 'a_perfectly_32_byte_key_exactly!';
    const vault = new WhisperVault(VAULT_TEST_FILE, key);
    assert.strictEqual(vault.encryptionKey, key);
});

runTest('should handle corrupted vault file gracefully', () => {
    mockVaultContent = 'not valid json';
    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    assert.deepStrictEqual(vault.vault, { whispers: [] });
});

runTest('should handle vault file with invalid encrypted content gracefully', () => {
    mockVaultContent = JSON.stringify({
        iv: crypto.randomBytes(16).toString('hex'),
        encryptedData: 'invalid-encrypted-data'
    });
    const vault = new WhisperVault(VAULT_TEST_FILE, TEST_ENCRYPTION_KEY);
    assert.deepStrictEqual(vault.vault, { whispers: [] });
});
