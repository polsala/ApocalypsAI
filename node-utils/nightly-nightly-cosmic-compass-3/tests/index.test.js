const { runCompass, getRandomCosmicGuidance, cosmicAlignments } = require('../src/index');

describe('Nightly Cosmic Compass', () => {
    let consoleSpy;
    let mockRandom;

    beforeEach(() => {
        consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
        // Mock rationale: Math.random is mocked to ensure deterministic test results.
        // Without mocking, the output would be random, making assertions impossible.
        mockRandom = jest.spyOn(Math, 'random').mockReturnValue(0.1); // Always pick the first item (index 0)
    });

    afterEach(() => {
        consoleSpy.mockRestore();
        mockRandom.mockRestore();
    });

    test('should guide a single item with deterministic output', () => {
        runCompass(['My First Task']);
        expect(consoleSpy).toHaveBeenCalledTimes(1);
        const expectedGuidance = cosmicAlignments[0]; // Stellar Core
        expect(consoleSpy).toHaveBeenCalledWith(
            `${expectedGuidance.emoji} My First Task: Aligned with the ${expectedGuidance.name}. ${expectedGuidance.whisper}`
        );
    });

    test('should guide multiple items with deterministic output', () => {
        runCompass(['Task A', 'Task B']);
        expect(consoleSpy).toHaveBeenCalledTimes(2);
        const expectedGuidance = cosmicAlignments[0]; // Stellar Core
        expect(consoleSpy).toHaveBeenCalledWith(
            `${expectedGuidance.emoji} Task A: Aligned with the ${expectedGuidance.name}. ${expectedGuidance.whisper}`
        );
        expect(consoleSpy).toHaveBeenCalledWith(
            `${expectedGuidance.emoji} Task B: Aligned with the ${expectedGuidance.name}. ${expectedGuidance.whisper}`
        );
    });

    test('should handle no items gracefully', () => {
        runCompass([]);
        expect(consoleSpy).toHaveBeenCalledTimes(1);
        expect(consoleSpy).toHaveBeenCalledWith("The cosmic compass needs items to guide. Provide tasks or ideas!");
    });

    test('getRandomCosmicGuidance should return a valid guidance object', () => {
        const guidance = getRandomCosmicGuidance();
        expect(cosmicAlignments).toContain(guidance);
        expect(guidance).toHaveProperty('name');
        expect(guidance).toHaveProperty('emoji');
        expect(guidance).toHaveProperty('whisper');
    });

    test('getRandomCosmicGuidance should return different guidance when random is varied (mocked)', () => {
        mockRandom.mockReturnValueOnce(0.1); // Stellar Core
        mockRandom.mockReturnValueOnce(0.9); // Celestial Bloom (last item)

        const guidance1 = getRandomCosmicGuidance();
        const guidance2 = getRandomCosmicGuidance();

        expect(guidance1.name).toBe('Stellar Core');
        expect(guidance2.name).toBe('Celestial Bloom');
    });
});
