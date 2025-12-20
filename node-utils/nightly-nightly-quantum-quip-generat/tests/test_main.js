// Tests for Quantum Quip Generator
const { QuantumQuipGenerator } = require('../src/main.js');
const chalk = require('chalk');

// Mock chalk to avoid color codes in tests
const mockChalk = {
  cyan: (str) => str,
  yellow: (str) => str,
  blue: (str) => str,
  white: (str) => str,
  gray: (str) => str,
  red: (str) => str,
  green: (str) => str
};

// Replace chalk with mock
Object.keys(chalk).forEach(key => {
  chalk[key] = mockChalk[key] || ((str) => str);
});

// Mock inquirer to avoid interactive prompts in tests
const mockInquirer = {
  prompt: () => Promise.resolve({})
};

// Mock Command for CLI testing
const mockCommand = {
  name: () => mockCommand,
  description: () => mockCommand,
  version: () => mockCommand,
  command: () => ({
    description: () => mockCommand,
    option: () => mockCommand,
    action: () => mockCommand
  }),
  argument: () => mockCommand,
  option: () => mockCommand,
  action: () => mockCommand,
  parse: () => {}
};

// Replace require for inquirer and commander
const Module = require('module');
const originalRequire = Module.prototype.require;
Module.prototype.require = function(id) {
  if (id === 'inquirer') return mockInquirer;
  if (id === 'commander') return { Command: function() { return mockCommand; } };
  return originalRequire.apply(this, arguments);
};

// Test suite
function runTests() {
  console.log('Running Quantum Quip Generator Tests...\n');
  
  const generator = new QuantumQuipGenerator();
  let passed = 0;
  let failed = 0;

  function test(name, testFn) {
    try {
      testFn();
      console.log(`✓ ${name}`);
      passed++;
    } catch (error) {
      console.log(`✗ ${name}: ${error.message}`);
      failed++;
    }
  }

  function assert(condition, message) {
    if (!condition) {
      throw new Error(message);
    }
  }

  // Test 1: Generator instantiation
  test('Generator instantiates correctly', () => {
    assert(generator instanceof QuantumQuipGenerator, 'Generator should be instance of QuantumQuipGenerator');
    assert(Array.isArray(generator.categories), 'Categories should be an array');
    assert(generator.categories.length > 0, 'Should have at least one category');
  });

  // Test 2: Generate random joke
  test('Generate random joke', () => {
    const joke = generator.generateJoke();
    assert(typeof joke === 'object', 'Should return an object');
    assert(typeof joke.text === 'string', 'Joke text should be a string');
    assert(joke.text.length > 0, 'Joke text should not be empty');
    assert(typeof joke.category === 'string', 'Category should be a string');
    assert(joke.category.length > 0, 'Category should not be empty');
  });

  // Test 3: Generate joke with explanation
  test('Generate joke with explanation', () => {
    const joke = generator.generateJoke({ explain: true });
    assert(typeof joke === 'object', 'Should return an object');
    assert(typeof joke.text === 'string', 'Joke text should be a string');
    assert(joke.text.length > 0, 'Joke text should not be empty');
    assert(joke.explanation, 'Should include explanation when requested');
    assert(typeof joke.explanation === 'string', 'Explanation should be a string');
  });

  // Test 4: Generate joke by category
  test('Generate joke by category', () => {
    const category = generator.categories[0];
    const joke = generator.generateJoke({ category: category });
    assert(joke.category.toLowerCase() === category.toLowerCase(), 'Should return joke from specified category');
  });

  // Test 5: Invalid category handling
  test('Handle invalid category', () => {
    try {
      generator.generateJoke({ category: 'nonexistent' });
      assert(false, 'Should throw error for invalid category');
    } catch (error) {
      assert(error.message.includes('not found'), 'Should throw appropriate error message');
    }
  });

  // Test 6: Format output as text
  test('Format output as text', () => {
    const joke = generator.generateJoke({ explain: true });
    const output = generator.formatOutput(joke, 'text');
    assert(typeof output === 'string', 'Output should be a string');
    assert(output.includes(joke.text), 'Output should contain joke text');
    assert(output.includes(joke.explanation), 'Output should contain explanation when present');
  });

  // Test 7: Format output as JSON
  test('Format output as JSON', () => {
    const joke = generator.generateJoke({ explain: true });
    const output = generator.formatOutput(joke, 'json');
    assert(typeof output === 'string', 'Output should be a string');
    const parsed = JSON.parse(output);
    assert(parsed.text === joke.text, 'JSON should contain correct joke text');
    assert(parsed.category === joke.category, 'JSON should contain correct category');
    assert(parsed.explanation === joke.explanation, 'JSON should contain correct explanation');
  });

  // Test 8: Format output as markdown
  test('Format output as markdown', () => {
    const joke = generator.generateJoke({ explain: true });
    const output = generator.formatOutput(joke, 'markdown');
    assert(typeof output === 'string', 'Output should be a string');
    assert(output.includes('#'), 'Markdown should contain headers');
    assert(output.includes(joke.text), 'Markdown should contain joke text');
    assert(output.includes('**Explanation:**'), 'Markdown should contain explanation header');
  });

  // Test 9: Format category name
  test('Format category name', () => {
    const formatted = generator.formatCategory('superposition');
    assert(formatted === 'Superposition', 'Should capitalize first letter');
    
    const formatted2 = generator.formatCategory('qubits');
    assert(formatted2 === 'Qubits', 'Should capitalize first letter');
  });

  // Test 10: Multiple joke generation consistency
  test('Multiple joke generation', () => {
    const jokes = [];
    for (let i = 0; i < 10; i++) {
      const joke = generator.generateJoke();
      jokes.push(joke);
      assert(typeof joke.text === 'string', 'Each joke should have text');
      assert(joke.text.length > 0, 'Each joke should not be empty');
    }
    
    // Check that we get different jokes (probabilistic test)
    const uniqueJokes = new Set(jokes.map(j => j.text));
    assert(uniqueJokes.size >= 3, 'Should generate varied jokes over multiple calls');
  });

  // Test 11: All categories are covered
  test('All categories have jokes', () => {
    const allJokes = require('../src/jokes.js');
    const jokeCategories = new Set(allJokes.map(j => j.category.toLowerCase()));
    const generatorCategories = new Set(generator.categories.map(c => c.toLowerCase()));
    
    assert(jokeCategories.size === generatorCategories.size, 'Generator should recognize all joke categories');
    
    // Check that each category has at least one joke
    generator.categories.forEach(category => {
      const categoryJokes = allJokes.filter(j => j.category.toLowerCase() === category.toLowerCase());
      assert(categoryJokes.length > 0, `Category '${category}' should have at least one joke`);
    });
  });

  // Test 12: Joke structure validation
  test('Joke structure validation', () => {
    const allJokes = require('../src/jokes.js');
    
    allJokes.forEach((joke, index) => {
      assert(typeof joke.text === 'string', `Joke ${index}: text should be string`);
      assert(joke.text.length > 0, `Joke ${index}: text should not be empty`);
      assert(typeof joke.category === 'string', `Joke ${index}: category should be string`);
      assert(joke.category.length > 0, `Joke ${index}: category should not be empty`);
      assert(typeof joke.explanation === 'string', `Joke ${index}: explanation should be string`);
      assert(joke.explanation.length > 0, `Joke ${index}: explanation should not be empty`);
    });
  });

  // Summary
  console.log(`\nTest Results: ${passed} passed, ${failed} failed`);
  
  if (failed === 0) {
    console.log(chalk.green('\nAll tests passed! 🎉'));
    process.exit(0);
  } else {
    console.log(chalk.red('\nSome tests failed! ❌'));
    process.exit(1);
  }
}

// Run tests if called directly
if (require.main === module) {
  runTests();
}

module.exports = { runTests };
