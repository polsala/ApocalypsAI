const { encode, decode } = require('../src/index.js');

describe('Cosmic Chatter Translator', () => {
    // Mock rationale: Math.random is used for adding flair, which makes tests non-deterministic.
    // We mock Math.random to ensure consistent test results.
    let originalMathRandom;

    beforeEach(() => {
        originalMathRandom = Math.random;
    });

    afterEach(() => {
        Math.random = originalMathRandom;
    });

    it('should encode a simple message with predictable output', () => {
        // Mock Math.random to return a fixed sequence for predictable encoding
        const mockRandomValues = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];
        let mockRandomIndex = 0;
        Math.random = jest.fn(() => mockRandomValues[mockRandomIndex++ % mockRandomValues.length]);

        const message = "hello";
        // Expected output based on the mock random values and the encoding logic
        // 'h' -> 'hazz', 'e' -> 'elp', 'l' -> 'lop', 'l' -> 'lop', 'o' -> 'o'
        // Prefixes: 0.1, 0.2, 0.3, 0.4, 0.5 -> 'Zorp '
        // Suffixes: 0.6, 0.7, 0.8, 0.9, 1.0 -> '!'
        const expected = "Zorp hazzelp loplop o!";
        expect(encode(message)).toBe(expected);
    });

    it('should decode a predictable encoded message', () => {
        // This test uses a message that was predictably encoded in a previous test or manually crafted.
        // The decoder is heuristic, so we test a known good case.
        const encodedMessage = "Zorp hazzelp loplop o!";
        const expected = "Hello";
        expect(decode(encodedMessage)).toBe(expected);
    });

    it('should handle messages with spaces and punctuation', () => {
        // Mock Math.random for predictable flair
        const mockRandomValues = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];
        let mockRandomIndex = 0;
        Math.random = jest.fn(() => mockRandomValues[mockRandomIndex++ % mockRandomValues.length]);

        const message = "Greetings from the void!";
        // Expected output based on mock random values and encoding logic
        // 'g' -> 'glorp', 'r' -> 'raz', 'e' -> 'elp', 'e' -> 'elp', 't' -> 'taz', 'i' -> 'ip', 'n' -> 'norp', 'g' -> 'glorp', 's' -> 'snorp'
        // 'f' -> 'flib', 'r' -> 'raz', 'o' -> 'o', 'm' -> 'morp'
        // 't' -> 'taz', 'h' -> 'hazz', 'e' -> 'elp'
        // 'v' -> 'vord', 'o' -> 'o', 'i' -> 'ip', 'd' -> 'daz'
        // Prefixes: 0.1, 0.2, 0.3, 0.4, 0.5 -> 'Zorp '
        // Suffixes: 0.6, 0.7, 0.8, 0.9, 1.0 -> '!'
        const expected = "Zorp glorprazelp elptazipnorp glorpsnorp flibraz o morp tazhazz elp vord o ip daz!";
        expect(encode(message)).toBe(expected);
    });

    it('should decode a message with spaces and punctuation', () => {
        const encodedMessage = "Zorp glorprazelp elptazipnorp glorpsnorp flibraz o morp tazhazz elp vord o ip daz!";
        const expected = "Greetings from the void"; // Decoder might not perfectly recover punctuation if it was part of the mapping
        expect(decode(encodedMessage)).toBe(expected);
    });

    it('should handle empty strings', () => {
        // Mock Math.random for predictable flair
        const mockRandomValues = [0.1, 0.2];
        let mockRandomIndex = 0;
        Math.random = jest.fn(() => mockRandomValues[mockRandomIndex++ % mockRandomValues.length]);

        const message = "";
        const expected = "Zorp !"; // Default flair for empty string
        expect(encode(message)).toBe(expected);
        expect(decode("Zorp !")).toBe("");
    });

    it('should preserve case in decoding when possible (heuristic)', () => {
        // The decoder aims to capitalize the first letter, but doesn't preserve internal case.
        const encodedMessage = "Zorp Hazzelp Loplop O!";
        const expected = "Hazzelp loplop o"; // Decoder is case-insensitive for input, but outputs lower case with first letter capitalized.
        expect(decode(encodedMessage)).toBe(expected);
    });

    it('should handle numbers and special characters gracefully', () => {
        // Mock Math.random for predictable flair
        const mockRandomValues = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];
        let mockRandomIndex = 0;
        Math.random = jest.fn(() => mockRandomValues[mockRandomIndex++ % mockRandomValues.length]);

        const message = "Agent 007, report!";
        // 'a' -> 'orp', 'g' -> 'glorp', 'e' -> 'elp', 'n' -> 'norp', 't' -> 'taz'
        // 'r' -> 'raz', 'e' -> 'elp', 'p' -> 'paz', 'o' -> 'o', 'r' -> 'raz', 't' -> 'taz' 
        // Prefixes: 0.1, 0.2, 0.3, 0.4, 0.5 -> 'Zorp '
        // Suffixes: 0.6, 0.7, 0.8, 0.9, 1.0 -> '!'
        const expected = "Zorp orpglorpelpnorptaz 007, razelpaz o raz taz!";
        expect(encode(message)).toBe(expected);
    });

    it('should decode a message with numbers and special characters', () => {
        const encodedMessage = "Zorp orpglorpelpnorptaz 007, razelpaz o raz taz!";
        const expected = "Agent 007, report"; // Decoder will strip trailing punctuation from the mapping
        expect(decode(encodedMessage)).toBe(expected);
    });
});
