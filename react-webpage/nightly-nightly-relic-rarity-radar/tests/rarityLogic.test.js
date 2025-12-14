import { assignRarity } from '../src/utils/rarityLogic';

describe('assignRarity', () => {
  // # Mock rationale: The assignRarity function is pure and deterministic, relying only on its input string. No external dependencies or side effects to mock.

  test('should assign Common Scavenge for simple, short items', () => {
    expect(assignRarity('rock').level).toBe('Common Scavenge');
    expect(assignRarity('old boot').level).toBe('Common Scavenge');
    expect(assignRarity('rusty nail').level).toBe('Common Scavenge');
  });

  test('should assign Uncommon Find for slightly longer or more descriptive items', () => {
    expect(assignRarity('broken radio').level).toBe('Uncommon Find');
    expect(assignRarity('tattered map').level).toBe('Uncommon Find');
    expect(assignRarity('water bottle 2L').level).toBe('Uncommon Find');
  });

  test('should assign Rare Relic for items with specific keywords or complexity', () => {
    expect(assignRarity('ancient coin').level).toBe('Rare Relic');
    expect(assignRarity('glowing mushroom').level).toBe('Rare Relic');
    expect(assignRarity('circuit board fragment').level).toBe('Rare Relic');
    expect(assignRarity('data chip 0xAF').level).toBe('Rare Relic');
  });

  test('should assign Legendary Artifact for items with multiple strong keywords or significant length', () => {
    expect(assignRarity('legendary glowing ancient sword').level).toBe('Legendary Artifact');
    expect(assignRarity('temporal data core shard').level).toBe('Legendary Artifact');
    expect(assignRarity('whispering circuit fragment of power').level).toBe('Legendary Artifact');
  });

  test('should assign Mythic Echo for items containing void, temporal, or anomaly keywords', () => {
    expect(assignRarity('void crystal').level).toBe('Mythic Echo');
    expect(assignRarity('temporal anomaly detector').level).toBe('Mythic Echo');
    expect(assignRarity('whispers of the void').level).toBe('Mythic Echo');
    expect(assignRarity('ancient temporal void echo shard').level).toBe('Mythic Echo');
  });

  test('should handle case insensitivity', () => {
    expect(assignRarity('Void Crystal').level).toBe('Mythic Echo');
    expect(assignRarity('gLoWiNg ShArD').level).toBe('Rare Relic');
  });

  test('should prioritize stronger keywords', () => {
    // 'void' gives +5, 'glowing' gives +3. 'void' should dominate.
    expect(assignRarity('glowing void shard').level).toBe('Mythic Echo');
  });

  test('should correctly calculate score for edge cases', () => {
    // 'a' -> length 1, score 0 -> Common
    expect(assignRarity('a').level).toBe('Common Scavenge');
    // 'ab' -> length 2, score 0 -> Common
    expect(assignRarity('ab').level).toBe('Common Scavenge');
    // 'abcde' -> length 5, score 1 -> Common
    expect(assignRarity('abcde').level).toBe('Common Scavenge');
    // 'abcdefghij' -> length 10, score 2 -> Uncommon
    expect(assignRarity('abcdefghij').level).toBe('Uncommon Find');
    // 'glowing' -> length 7 (1), keyword (3) = 4 -> Rare
    expect(assignRarity('glowing').level).toBe('Rare Relic');
    // 'void' -> length 4 (0), keyword (5) = 5 -> Mythic
    expect(assignRarity('void').level).toBe('Mythic Echo');
  });
});
