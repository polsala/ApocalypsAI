import { classifyRelic, sortClassifiedRelics } from '../src/classifier';
import { Relic, Rarity, ClassificationResult, KeywordRule } from '../src/types';

describe('classifyRelic', () => {
  it('should classify a common relic correctly', () => {
    const relic: Relic = { name: 'Rusty Spoon', description: 'A very old and broken spoon.' };
    const result = classifyRelic(relic);
    expect(result.relic).toEqual(relic);
    expect(result.rarity).toBe('Common');
    expect(result.utilityScore).toBe(0); // -2 from broken/rusty, capped at 0
    expect(result.reason).toEqual(expect.arrayContaining([
      expect.stringContaining('Indicates low quality or damage: broken, rusty')
    ]));
  });

  it('should classify an uncommon relic correctly', () => {
    const relic: Relic = { name: 'Gleaming Data-Chip', description: 'An intact data storage unit.' };
    const result = classifyRelic(relic);
    expect(result.relic).toEqual(relic);
    expect(result.rarity).toBe('Uncommon');
    expect(result.utilityScore).toBe(4); // 1 from gleaming, 3 from data-chip
    expect(result.reason).toEqual(expect.arrayContaining([
      expect.stringContaining('Suggests good condition or aesthetic value: gleaming'),
      expect.stringContaining('Electronic components, potentially useful: data-chip')
    ]));
  });

  it('should classify a rare relic correctly', () => {
    const relic: Relic = { name: 'Ancient Power-Cell', description: 'A pre-fall energy core, still pulsating faintly.' };
    const result = classifyRelic(relic);
    expect(result.relic).toEqual(relic);
    expect(result.rarity).toBe('Rare');
    expect(result.utilityScore).toBe(9); // 5 from power-cell, 4 from ancient/pre-fall
    expect(result.reason).toEqual(expect.arrayContaining([
      expect.stringContaining('Power sources are always valuable: power-cell'),
      expect.stringContaining('Historical significance, might hold secrets: ancient, pre-fall')
    ]));
  });

  it('should classify a legendary relic correctly', () => {
    const relic: Relic = { name: 'Glowing Schematic', description: 'A blueprint for a temporal flux capacitor.' };
    const result = classifyRelic(relic);
    expect(result.relic).toEqual(relic);
    expect(result.rarity).toBe('Legendary');
    expect(result.utilityScore).toBe(10); // 7 from glowing, 8 from schematic, capped at 10
    expect(result.reason).toEqual(expect.arrayContaining([
      expect.stringContaining('Unusual properties, high potential: glowing'),
      expect.stringContaining('Knowledge is power, especially lost knowledge: schematic')
    ]));
  });

  it('should classify a mythic relic correctly', () => {
    const relic: Relic = { name: 'Void-Shard', description: 'A fragment of pure temporal-flux energy.' };
    const result = classifyRelic(relic);
    expect(result.relic).toEqual(relic);
    expect(result.rarity).toBe('Mythic');
    expect(result.utilityScore).toBe(10); // 10 from void-shard/temporal-flux, capped at 10
    expect(result.reason).toEqual(expect.arrayContaining([
      expect.stringContaining('Items of immense, possibly dangerous, power: void-shard, temporal-flux')
    ]));
  });

  it('should handle relics with no matching keywords', () => {
    const relic: Relic = { name: 'Plain Rock', description: 'Just a rock.' };
    const result = classifyRelic(relic);
    expect(result.rarity).toBe('Common');
    expect(result.utilityScore).toBe(0);
    expect(result.reason).toEqual(['No specific rules matched, classified as Common.']);
  });

  it('should apply custom rules', () => {
    const customRules: KeywordRule[] = [
      { keywords: ['super-rare'], rarityBoost: 'Mythic', utilityBoost: 10, description: 'Custom super-rare item.' },
      { keywords: ['useless'], rarityBoost: 'Common', utilityBoost: -5, description: 'Custom useless item.' },
    ];
    const relic1: Relic = { name: 'Super-Rare Widget' };
    const result1 = classifyRelic(relic1, customRules);
    expect(result1.rarity).toBe('Mythic');
    expect(result1.utilityScore).toBe(10);
    expect(result1.reason).toEqual(expect.arrayContaining([
      expect.stringContaining('Custom super-rare item: super-rare')
    ]));

    const relic2: Relic = { name: 'Useless Gadget' };
    const result2 = classifyRelic(relic2, customRules);
    expect(result2.rarity).toBe('Common');
    expect(result2.utilityScore).toBe(0); // -5 capped at 0
    expect(result2.reason).toEqual(expect.arrayContaining([
      expect.stringContaining('Custom useless item: useless')
    ]));
  });
});

describe('sortClassifiedRelics', () => {
  it('should sort relics by rarity then utility score', () => {
    const results: ClassificationResult[] = [
      { relic: { name: 'Common Item' }, rarity: 'Common', utilityScore: 5, reason: [] },
      { relic: { name: 'Rare Item A' }, rarity: 'Rare', utilityScore: 3, reason: [] },
      { relic: { name: 'Uncommon Item' }, rarity: 'Uncommon', utilityScore: 7, reason: [] },
      { relic: { name: 'Rare Item B' }, rarity: 'Rare', utilityScore: 8, reason: [] },
      { relic: { name: 'Mythic Item' }, rarity: 'Mythic', utilityScore: 10, reason: [] },
      { relic: { name: 'Legendary Item' }, rarity: 'Legendary', utilityScore: 9, reason: [] },
    ];

    const sorted = sortClassifiedRelics(results);

    expect(sorted.map(r => r.relic.name)).toEqual([
      'Mythic Item',
      'Legendary Item',
      'Rare Item B', // Higher utility score
      'Rare Item A',
      'Uncommon Item',
      'Common Item',
    ]);
  });
});
