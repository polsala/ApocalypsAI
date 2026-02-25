import { computeTotalWeight, SupplyItem } from '../src/index';
import assert from 'assert';

function runTests() {
  const items: SupplyItem[] = [
    { name: 'Canned beans', weight: 400, unit: 'g', quantity: 3 }, // 1200 g
    { name: 'Water bottle', weight: 1, unit: 'kg', quantity: 2 }, // 2000 g
    { name: 'Rope', weight: 2, unit: 'lb', quantity: 1 }, // 907.18474 g
  ];

  const totalKg = computeTotalWeight(items, 'kg');
  // Expected total grams = 1200 + 2000 + 907.18474 = 4107.18474 g → 4.107185 kg
  const expectedKg = 4.107185;
  const diff = Math.abs(totalKg - expectedKg);
  assert(diff < 0.0001, `Kg conversion off: expected ${expectedKg}, got ${totalKg}`);

  const totalOz = computeTotalWeight(items, 'oz');
  // 4107.18474 g / 28.349523125 = 144.822 oz (approx)
  const expectedOz = 144.822;
  assert(Math.abs(totalOz - expectedOz) < 0.01, `Oz conversion off: expected ~${expectedOz}, got ${totalOz}`);

  console.log('All tests passed.');
}

runTests();
