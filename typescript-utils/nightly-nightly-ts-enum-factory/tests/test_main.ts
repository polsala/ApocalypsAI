import { execSync } from 'child_process';

// Mock rationale: Using synchronous CLI execution for deterministic testing
// Test 1: Basic conversion
test('basic conversion', () => {
  const output = execSync('ts-enum-factory --input "Apple Banana Cherry"').toString();
  expect(output).toContain("export enum Generated {\n  Apple = 'Apple',\n  Banana = 'Banana',\n  Cherry = 'Cherry'\n}");
});

// Test 2: With suffix and emoji
test('suffix and emoji', () => {
  const output = execSync("ts-enum-factory --input 'Red Green' --suffix -color --emoji 🎨").toString();
  expect(output).toContain("🎨RedColor = 'Red',");
  expect(output).toContain("🎨GreenColor = 'Green'");
});

// Test 3: Snake case
test('snake case', () => {
  const output = execSync("ts-enum-factory --input 'sun light shadow' --snake-case").toString();
  expect(output).toContain("sun = 'sun',");
  expect(output).toContain("light = 'light',");
  expect(output).toContain("shadow = 'shadow'");
});
