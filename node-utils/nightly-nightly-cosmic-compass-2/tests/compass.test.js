const assert = require('assert');
const { getCosmicAlignment, alignments } = require('../src/compass');

// Mock rationale: We need deterministic results for testing.
// By providing specific Date objects, we ensure the seed calculation
// in getCosmicAlignment is consistent across test runs, making tests reliable and offline.
describe('Cosmic Compass', () => {
  it('should return a cosmic alignment for a given date', () => {
    const testDate = new Date('2023-01-15T12:00:00Z'); // Fixed date for deterministic test
    const result = getCosmicAlignment(testDate);

    assert.strictEqual(typeof result, 'object');
    assert.strictEqual(result.date, '2023-01-15');
    assert.strictEqual(typeof result.location, 'string');
    assert.strictEqual(typeof result.alignment, 'string');
    assert.strictEqual(typeof result.influence, 'string');

    // Check if the alignment is one of the predefined ones
    const alignmentNames = alignments.map(a => a.name);
    assert.ok(alignmentNames.includes(result.alignment));
  });

  it('should return a consistent alignment for the same date', () => {
    const date1 = new Date('2024-03-20T00:00:00Z');
    const date2 = new Date('2024-03-20T23:59:59Z'); // Same day, different time
    const result1 = getCosmicAlignment(date1, 'Earth');
    const result2 = getCosmicAlignment(date2, 'Earth');

    assert.deepStrictEqual(result1, result2);
  });

  it('should return different alignments for different dates', () => {
    const date1 = new Date('2024-03-20T12:00:00Z');
    const date2 = new Date('2024-03-21T12:00:00Z');
    const result1 = getCosmicAlignment(date1);
    const result2 = getCosmicAlignment(date2);

    assert.notDeepStrictEqual(result1.alignment, result2.alignment);
  });

  it('should incorporate the specified location', () => {
    const testDate = new Date('2023-01-15T12:00:00Z');
    const testLocation = 'Mars Colony Alpha';
    const result = getCosmicAlignment(testDate, testLocation);

    assert.strictEqual(result.location, testLocation);
  });

  it('should default to "the known universe" if no location is provided', () => {
    const testDate = new Date('2023-01-15T12:00:00Z');
    const result = getCosmicAlignment(testDate);

    assert.strictEqual(result.location, 'the known universe');
  });

  it('should handle dates at the boundary of alignment array (index 0)', () => {
    // Date: 2023-01-10 -> seed 20230110. 20230110 % 10 (alignments.length) = 0.
    const dateForIndex0 = new Date('2023-01-10T12:00:00Z');
    const resultIndex0 = getCosmicAlignment(dateForIndex0);
    assert.strictEqual(resultIndex0.alignment, alignments[0].name);
  });

  it('should handle dates at the boundary of alignment array (last index)', () => {
    // Date: 2023-01-09 -> seed 20230109. 20230109 % 10 (alignments.length) = 9.
    const dateForLastIndex = new Date('2023-01-09T12:00:00Z');
    const resultLastIndex = getCosmicAlignment(dateForLastIndex);
    assert.strictEqual(resultLastIndex.alignment, alignments[alignments.length - 1].name);
  });
});
