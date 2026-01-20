import { generateAffirmation } from '../src/void-whisperer';

// Mock rationale: We mock randomness by overriding Math.random to return fixed indices.
jest.spyOn(global.Math, 'random').mockReturnValue(0.5);

describe('Void Whisperer', () => {
  it('should generate a deterministic affirmation', () => {
    const result = generateAffirmation();
    expect(result).toBe("In the ruins, silence blooms anew.");
  });
});
