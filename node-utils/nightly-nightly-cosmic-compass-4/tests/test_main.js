const assert = require('assert');
const { generateCosmicTip } = require('../src/main');

// Mock chalk to prevent actual console coloring during tests
const mockChalk = {
    yellow: (text) => text,
    cyan: (text) => text,
    green: (text) => text,
    blue: (text) => text,
    red: (text) => text,
    gray: (text) => text,
    bold: { magenta: (text) => text },
    italic: (text) => text
};

// Replace chalk with our mock for the duration of the tests
const originalChalk = require('chalk');
require('chalk') = mockChalk;

describe('Cosmic Compass', () => {
    it('should generate a navigation tip with expected elements', () => {
        const tip = generateCosmicTip();

        // Mock rationale: These assertions check for the presence of key phrases and simulated celestial elements.
        // The actual content will vary due to random selection, but the structure and expected components should be present.
        assert(tip.includes('Look to the'), 'Tip should include star guidance.');
        assert(tip.includes('Polaris') || tip.includes('Seven Sisters') || tip.includes('Orion'), 'Tip should mention a known star.');
        assert(tip.includes('North') || tip.includes('East') || tip.includes('South'), 'Tip should mention a star direction.');
        assert(tip.includes('Full Moon'), 'Tip should mention the moon phase.');
        assert(tip.includes('West'), 'Tip should mention the sun position.');
        assert(tip.includes('whisper secrets') || tip.includes('shadows lengthen') || tip.includes('dying light'), 'Tip should include lore.');
    });

    it('should return a non-empty string', () => {
        const tip = generateCosmicTip();
        assert(tip.length > 0, 'Generated tip should not be empty.');
    });

    // Restore original chalk after tests
    after(() => {
        require('chalk') = originalChalk;
    });
});

// Mock describe and it functions if running in a non-test environment
if (typeof describe === 'undefined') {
    global.describe = (name, fn) => fn();
    global.it = (name, fn) => fn();
    global.beforeEach = () => {};
    global.after = () => {};
}
