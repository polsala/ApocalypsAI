import { parseDiceNotation, rollDice, DiceNotation } from '../src/index';
import assert from 'assert';

function mockRng(values: number[]): () => number {
  let i = 0;
  return () => {
    const val = values[i % values.length];
    i++;
    return val;
  };
}

// --- parseDiceNotation tests ---
(() => {
  const notation = parseDiceNotation('2d6+3');
  assert.deepStrictEqual(notation, { count: 2, sides: 6, modifier: 3 } as DiceNotation);
  const notation2 = parseDiceNotation('d20');
  assert.deepStrictEqual(notation2, { count: 1, sides: 20, modifier: 0 } as DiceNotation);
})();

// --- rollDice deterministic test ---
(() => {
  const notation: DiceNotation = { count: 3, sides: 6, modifier: 2 };
  // rng values 0.0 -> roll 1, 0.5 -> roll 4, 0.99 -> roll 6
  const rng = mockRng([0.0, 0.5, 0.99]);
  const result = rollDice(notation, rng);
  // rolls: 1 + 4 + 6 = 11, plus modifier 2 = 13
  assert.strictEqual(result, 13);
})();
