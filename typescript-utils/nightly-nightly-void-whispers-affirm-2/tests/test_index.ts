import { whisperFromTheVoid } from '../src/index';
import * as assert from 'assert';

// Mock rationale: To ensure deterministic test results by overriding Math.random
const mockAffirmation = "You refactor reality into elegant simplicity.";
const mockRandom = () => 0.3;

Math.random = mockRandom;

describe('Void Whispers Affirmations', () => {
  it('should return a fixed mocked affirmation', () => {
    const result = whisperFromTheVoid();
    const expected = `The void murmurs: ${mockAffirmation}`;
    assert.strictEqual(result, expected);
  });
});
