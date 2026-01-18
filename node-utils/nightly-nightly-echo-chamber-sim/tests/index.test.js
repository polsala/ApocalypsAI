const { applyDistortion, simulateWhisper } = require('../src/index');
const assert = require('assert');

// Mock rationale: We need to capture console output for simulateWhisper to verify its behavior.
// By mocking console.log, we can inspect what would have been printed to the console.
let consoleOutput = [];
const mockConsoleLog = (message) => consoleOutput.push(message);
const originalConsoleLog = console.log;

describe('Echo Chamber Simulator', () => {
    beforeEach(() => {
        consoleOutput = [];
        console.log = mockConsoleLog; // Mock console.log before each test
    });

    afterEach(() => {
        console.log = originalConsoleLog; // Restore console.log after each test
    });

    describe('applyDistortion', () => {
        it('should truncate the message based on the truncation factor', () => {
            const message = "This is a long message that needs to be shortened."; // 10 words
            const truncated = applyDistortion(message, 0.5, {});
            const words = truncated.split(/\s+/);
            // Original: 10 words. 0.5 factor -> 5 words.
            assert.strictEqual(words.length, 5, `Expected 5 words, got ${words.length}: \"${truncated}\"`)
            assert.strictEqual(truncated, "This is a long message", `Expected \"This is a long message\", got \"${truncated}\"`)
        });

        it('should apply word replacements', () => {
            const message = "The old world is gone, a new era begins.";
            const replacements = { "old": "ancient", "gone": "lost" };
            const distorted = applyDistortion(message, 1.0, replacements); // No truncation
            assert.strictEqual(distorted, "The ancient world is lost, a new era begins.", `Expected \"The ancient world is lost, a new era begins.\", got \"${distorted}\"`)
        });

        it('should apply both truncation and replacements', () => {
            const message = "The ancient scrolls speak of a hidden bunker beneath the old city ruins, filled with pre-collapse tech and sustenance for a thousand years.";
            const replacements = { "scrolls": "papers", "bunker": "shelter", "old": "forgotten" };
            const distorted = applyDistortion(message, 0.7, replacements); // Original: 25 words. 0.7 factor -> 17.5 -> 17 words.
            // Expected: "The ancient papers speak of a hidden shelter beneath the forgotten city ruins, filled with pre-collapse tech and sustenance for a thousand"
            assert.strictEqual(distorted.split(/\s+/).length, 17, `Expected 17 words, got ${distorted.split(/\s+/).length}: \"${distorted}\"`)
            assert.strictEqual(distorted, "The ancient papers speak of a hidden shelter beneath the forgotten city ruins, filled with pre-collapse tech and sustenance for a thousand", `Expected specific output, got \"${distorted}\"`)
        });

        it('should handle empty message', () => {
            const message = "";
            const distorted = applyDistortion(message, 0.5, {});
            assert.strictEqual(distorted, "", `Expected empty string, got \"${distorted}\"`)
        });

        it('should handle no replacements', () => {
            const message = "Hello world";
            const distorted = applyDistortion(message, 1.0, {});
            assert.strictEqual(distorted, "Hello world", `Expected \"Hello world\", got \"${distorted}\"`)
        });

        it('should handle truncation to 1 word', () => {
            const message = "Many words here"; // 3 words
            const distorted = applyDistortion(message, 0.1, {}); // 3 words * 0.1 = 0.3 -> 1 word (Math.max(1, ...))
            assert.strictEqual(distorted, "Many", `Expected \"Many\", got \"${distorted}\"`)
        });

        it('should handle case-insensitive word replacement', () => {
            const message = "The Void whispers";
            const replacements = { "void": "empty" };
            const distorted = applyDistortion(message, 1.0, replacements);
            assert.strictEqual(distorted, "The empty whispers", `Expected \"The empty whispers\", got \"${distorted}\"`)
        });

        it('should handle words with trailing punctuation for replacement matching', () => {
            const message = "The ruins, are vast.";
            const replacements = { "ruins": "wasteland" };
            const distorted = applyDistortion(message, 1.0, replacements);
            assert.strictEqual(distorted, "The wasteland are vast.", `Expected \"The wasteland are vast.\", got \"${distorted}\"`)
        });
    });

    describe('simulateWhisper', () => {
        it('should log the initial message and each hop', () => {
            const message = "Test message."; // 2 words
            const hops = 2;
            const truncationFactor = 0.5;
            const replacements = {};

            simulateWhisper(message, hops, truncationFactor, replacements);

            assert.strictEqual(consoleOutput.length, 6); // 3 headers + 3 messages
            assert.ok(consoleOutput[0].includes('Initial Message'));
            assert.strictEqual(consoleOutput[1], 'Test message.');
            assert.ok(consoleOutput[2].includes('Hop 1'));
            assert.strictEqual(consoleOutput[3], 'Test message.', 'Hop 1 should be truncated to 1 word'); // "Test message." (2 words) * 0.5 = 1 word (min 1)
            assert.ok(consoleOutput[4].includes('Hop 2'));
            assert.strictEqual(consoleOutput[5], 'Test', 'Hop 2 should be truncated to 1 word'); // "Test" (1 word) * 0.5 = 0.5 -> 1 word (min 1)
        });

        it('should correctly apply multiple hops with truncation and replacements', () => {
            const message = "The ancient scrolls speak of a hidden bunker beneath the old city ruins, filled with pre-collapse tech and sustenance for a thousand years."; // 25 words
            const hops = 2;
            const truncationFactor = 0.8;
            const replacements = { "scrolls": "papers", "bunker": "shelter", "tech": "gadgets", "sustenance": "food" };

            simulateWhisper(message, hops, truncationFactor, replacements);

            // Original: 25 words
            // Hop 1: 25 * 0.8 = 20 words. Replacements applied.
            // Hop 2: 20 * 0.8 = 16 words. Replacements applied.

            assert.strictEqual(consoleOutput.length, 6); // 3 headers + 3 messages

            assert.ok(consoleOutput[0].includes('Initial Message'));
            assert.strictEqual(consoleOutput[1], message);

            assert.ok(consoleOutput[2].includes('Hop 1'));
            const hop1Expected = "The ancient papers speak of a hidden shelter beneath the old city ruins, filled with pre-collapse gadgets and food for a thousand years.";
            assert.strictEqual(consoleOutput[3], hop1Expected);
            assert.strictEqual(consoleOutput[3].split(/\s+/).length, 20);

            assert.ok(consoleOutput[4].includes('Hop 2'));
            const hop2Expected = "The ancient papers speak of a hidden shelter beneath the old city ruins, filled with pre-collapse gadgets and food for a thousand";
            assert.strictEqual(consoleOutput[5], hop2Expected);
            assert.strictEqual(consoleOutput[5].split(/\s+/).length, 16);
        });

        it('should handle zero hops gracefully', () => {
            const message = "No hops here.";
            const hops = 0;
            const truncationFactor = 0.5;
            const replacements = {};

            simulateWhisper(message, hops, truncationFactor, replacements);

            assert.strictEqual(consoleOutput.length, 2); // Only initial message header + message
            assert.ok(consoleOutput[0].includes('Initial Message'));
            assert.strictEqual(consoleOutput[1], message);
        });
    });
});
