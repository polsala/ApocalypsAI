const assert = require('assert');
const sinon = require('sinon');
const fs = require('fs');
const { getRelicInfo, loadRelics, findBestMatch } = require('../src/index');

// Mock rationale: We need to control the relic database for deterministic tests.
// By mocking fs.readFileSync, we ensure tests don't depend on the actual file system
// and always use a predefined set of relics.

describe('Nightly Relic Identifier', () => {
  let readFileSyncStub;
  let consoleErrorStub;

  const mockRelics = [
    {
      "keywords": ["shiny", "metal", "disc", "hole"],
      "name": "Ancient Data Storage Disc (CD/DVD)",
      "purpose": "Used to store digital information.",
      "repurpose": "Makeshift blade.",
      "survival_rating": "Moderate"
    },
    {
      "keywords": ["plastic", "box", "buttons", "screen"],
      "name": "Personal Communication Device (Smartphone)",
      "purpose": "Enabled communication.",
      "repurpose": "Paperweight.",
      "survival_rating": "Low"
    }
  ];

  beforeEach(() => {
    readFileSyncStub = sinon.stub(fs, 'readFileSync').returns(JSON.stringify(mockRelics));
    consoleErrorStub = sinon.stub(console, 'error'); // Stub console.error to prevent output during tests
  });

  afterEach(() => {
    readFileSyncStub.restore();
    consoleErrorStub.restore();
  });

  it('should identify a CD/DVD correctly', () => {
    const info = getRelicInfo('A shiny metal disc with a hole in the middle.');
    assert.deepStrictEqual(info, {
      name: 'Ancient Data Storage Disc (CD/DVD)',
      purpose: 'Used to store digital information.',
      repurpose: 'Makeshift blade.',
      survival_rating: 'Moderate'
    });
  });

  it('should identify a Smartphone correctly', () => {
    const info = getRelicInfo('Found a small plastic box with many buttons and a cracked screen.');
    assert.deepStrictEqual(info, {
      name: 'Personal Communication Device (Smartphone)',
      purpose: 'Enabled communication.',
      repurpose: 'Paperweight.',
      survival_rating: 'Low'
    });
  });

  it('should return unknown for an unidentified relic', () => {
    const info = getRelicInfo('A strange glowing rock.');
    assert.deepStrictEqual(info, {
      name: 'Unknown Anomaly',
      purpose: 'Lost to the mists of time, or perhaps never had one.',
      repurpose: 'Use as a paperweight, a conversation starter, or a very slow-acting poison (handle with care).',
      survival_rating: 'Unpredictable'
    });
  });

  it('should handle empty description gracefully', () => {
    const info = getRelicInfo('');
    assert.deepStrictEqual(info, {
      name: 'Unknown Anomaly',
      purpose: 'Lost to the mists of time, or perhaps never had one.',
      repurpose: 'Use as a paperweight, a conversation starter, or a very slow-acting poison (handle with care).',
      survival_rating: 'Unpredictable'
    });
  });

  it('loadRelics should return empty array on file read error', () => {
    readFileSyncStub.restore(); // Restore original to re-stub with error
    readFileSyncStub = sinon.stub(fs, 'readFileSync').throws(new Error('File not found'));
    const relics = loadRelics();
    assert.deepStrictEqual(relics, []);
    assert.strictEqual(consoleErrorStub.callCount, 1); // console.error should be called once
    assert.ok(consoleErrorStub.getCall(0).args[0].includes('Error loading relics database:'));
  });

  it('loadRelics should return empty array on invalid JSON', () => {
    readFileSyncStub.restore();
    readFileSyncStub = sinon.stub(fs, 'readFileSync').returns('invalid json');
    const relics = loadRelics();
    assert.deepStrictEqual(relics, []);
    assert.strictEqual(consoleErrorStub.callCount, 1); // console.error should be called once
    assert.ok(consoleErrorStub.getCall(0).args[0].includes('Error loading relics database:'));
  });
});

// A simple describe/it/assert implementation for basic testing without a full framework
function describe(name, fn) {
  console.log(`\n${name}`);
  fn();
}

function it(name, fn) {
  try {
    fn();
    console.log(`  ✓ ${name}`);
  } catch (error) {
    console.error(`  ✗ ${name}`);
    console.error(error);
    process.exit(1);
  }
}
