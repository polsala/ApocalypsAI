import { generateAffirmation } from '../src/affirmationGenerator';
import { describe, it } from 'node:test';
import assert from 'node:assert';

// Mock rationale: We're testing deterministic output variations based on inputs
// without requiring external dependencies or network calls

describe('Affirmation Generator', () => {
  it('should generate an affirmation with default settings', () => {
    const result = generateAffirmation({});
    assert.strictEqual(typeof result, 'string');
    assert(result.length > 0);
    assert(result.includes('Survivor') || result.includes('Wanderer') || result.includes('Scavenger'));
  });

  it('should personalize affirmation with provided name', () => {
    const result = generateAffirmation({ name: 'Rebel' });
    assert(result.includes('Rebel'));
  });

  it('should generate mood-appropriate affirmations', () => {
    const hopeful = generateAffirmation({ mood: 'hopeful' });
    assert(hopeful.includes('hope') || hopeful.includes('light') || hopeful.includes('tomorrow'));
    
    const determined = generateAffirmation({ mood: 'determined' });
    assert(determined.includes('determination') || determined.includes('will') || determined.includes('resolve'));
  });

  it('should handle unknown moods gracefully', () => {
    const result = generateAffirmation({ mood: 'unknown' });
    assert.strictEqual(typeof result, 'string');
    assert(result.length > 0);
  });
});
