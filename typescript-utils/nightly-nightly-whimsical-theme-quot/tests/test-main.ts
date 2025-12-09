import { execSync } from 'child_process';

const testCases = [
  { args: ['--theme', 'apocalypse', '--mood', 'uplifting'], expected: /The end is nigh/ },
  { args: ['--theme', 'tech', '--mood', 'cryptic'], expected: /Quantum computing/ },
  { args: ['--theme', 'survival', '--mood', 'default'], expected: /Invalid theme/ }
];

for (const [index, test] of testCases.entries()) {
  try {
    const output = execSync(`ts-node src/main.ts ${test.args.join(' ')}`,{encoding: 'utf-8'});
    if (!output.match(test.expected)) {
      throw new Error(`Test ${index} failed: Expected ${test.expected}`);
    }
  } catch (e) {
    console.error(`\nTest ${index} failed:`, e);
    process.exit(1);
  }
}

console.log('\nAll tests passed! ✅');

// Mock rationale: Uses deterministic command execution with regex pattern matching
// to verify output structure without relying on specific random selections
