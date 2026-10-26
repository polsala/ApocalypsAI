import { NutrientNoodleNegotiator } from '../src/negotiator';
import { NutrientPaste, ConsumptionRecord } from '../src/types';

const MOCK_PASTES: NutrientPaste[] = [
  { id: 'A', name: 'Paste A', tags: ['sweet'] },
  { id: 'B', name: 'Paste B', tags: ['savory'] },
  { id: 'C', name: 'Paste C', tags: ['sweet', 'umami'] },
  { id: 'D', name: 'Paste D', tags: ['bland'] },
];

describe('NutrientNoodleNegotiator', () => {
  it('should start with the first paste if no history', () => {
    const record: ConsumptionRecord = { lastConsumedId: null, history: [] };
    const negotiator = new NutrientNoodleNegotiator(MOCK_PASTES, record);
    const { suggestion, record: updatedRecord } = negotiator.suggestNext();
    expect(suggestion.id).toBe('A');
    expect(updatedRecord.lastConsumedId).toBe('A');
    expect(updatedRecord.history).toEqual(['A']);
  });

  it('should rotate to the next paste', () => {
    const record: ConsumptionRecord = { lastConsumedId: 'A', history: ['A'] };
    const negotiator = new NutrientNoodleNegotiator(MOCK_PASTES, record);
    const { suggestion, record: updatedRecord } = negotiator.suggestNext();
    expect(suggestion.id).toBe('B');
    expect(updatedRecord.lastConsumedId).toBe('B');
    expect(updatedRecord.history).toEqual(['B', 'A']);
  });

  it('should wrap around when rotating past the last paste', () => {
    const record: ConsumptionRecord = { lastConsumedId: 'D', history: ['D'] };
    const negotiator = new NutrientNoodleNegotiator(MOCK_PASTES, record);
    const { suggestion, record: updatedRecord } = negotiator.suggestNext();
    expect(suggestion.id).toBe('A');
    expect(updatedRecord.lastConsumedId).toBe('A');
    expect(updatedRecord.history).toEqual(['A', 'D']);
  });

  it('should suggest a mood-matching paste if available and not in recent history', () => {
    const record: ConsumptionRecord = { lastConsumedId: 'A', history: ['A', 'D'] }; // A and D are recent
    const negotiator = new NutrientNoodleNegotiator(MOCK_PASTES, record, 2); // History size 2
    const { suggestion, record: updatedRecord } = negotiator.suggestNext('savory');
    expect(suggestion.id).toBe('B'); // B is savory and not in history ['A', 'D']
    expect(updatedRecord.lastConsumedId).toBe('B');
    expect(updatedRecord.history).toEqual(['B', 'A']);
  });

  it('should fall back to rotational if mood-matching paste is in recent history', () => {
    const record: ConsumptionRecord = { lastConsumedId: 'B', history: ['B', 'A'] }; // B is savory and recent
    const negotiator = new NutrientNoodleNegotiator(MOCK_PASTES, record, 2);
    const { suggestion, record: updatedRecord } = negotiator.suggestNext('savory');
    expect(suggestion.id).toBe('C'); // B is recent, so it should rotate to C (next after B)
    expect(updatedRecord.lastConsumedId).toBe('C');
    expect(updatedRecord.history).toEqual(['C', 'B']);
  });

  it('should fall back to rotational if no mood-matching paste exists', () => {
    const record: ConsumptionRecord = { lastConsumedId: 'A', history: ['A'] };
    const negotiator = new NutrientNoodleNegotiator(MOCK_PASTES, record);
    const { suggestion, record: updatedRecord } = negotiator.suggestNext('nonexistent-mood');
    expect(suggestion.id).toBe('B'); // No match, so rotate
    expect(updatedRecord.lastConsumedId).toBe('B');
    expect(updatedRecord.history).toEqual(['B', 'A']);
  });

  it('should maintain history size correctly', () => {
    const record: ConsumptionRecord = { lastConsumedId: 'A', history: ['A', 'D', 'C'] };
    const negotiator = new NutrientNoodleNegotiator(MOCK_PASTES, record, 2); // History size 2
    const { suggestion, record: updatedRecord } = negotiator.suggestNext(); // Should rotate to B
    expect(suggestion.id).toBe('B');
    expect(updatedRecord.history).toEqual(['B', 'A']); // Only B and A should be kept
  });

  it('should handle empty pastes list gracefully', () => {
    expect(() => new NutrientNoodleNegotiator([], { lastConsumedId: null, history: [] }))
      .toThrow("No nutrient pastes available.");
  });
});
