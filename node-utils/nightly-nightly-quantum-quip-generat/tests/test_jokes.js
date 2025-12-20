// Tests for Jokes Database
const jokes = require('../src/jokes.js');

function runJokeTests() {
  console.log('Running Jokes Database Tests...\n');
  
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

  // Test 1: Jokes array structure
  test('Jokes array is valid', () => {
    assert(Array.isArray(jokes), 'Jokes should be an array');
    assert(jokes.length > 0, 'Should have at least one joke');
  });

  // Test 2: Each joke has required properties
  test('Each joke has required properties', () => {
    jokes.forEach((joke, index) => {
      assert(typeof joke === 'object', `Joke ${index}: should be an object`);
      assert(joke.text, `Joke ${index}: should have text property`);
      assert(joke.category, `Joke ${index}: should have category property`);
      assert(joke.explanation, `Joke ${index}: should have explanation property`);
    });
  });

  // Test 3: Joke text validation
  test('Joke text validation', () => {
    jokes.forEach((joke, index) => {
      assert(typeof joke.text === 'string', `Joke ${index}: text should be string`);
      assert(joke.text.length > 10, `Joke ${index}: text should be longer than 10 characters`);
      assert(joke.text.includes('\n'), `Joke ${index}: text should contain newline for punchline`);
    });
  });

  // Test 4: Category validation
  test('Category validation', () => {
    const validCategories = ['superposition', 'entanglement', 'qubits', 'algorithms', 'hardware', 'general'];
    
    jokes.forEach((joke, index) => {
      assert(typeof joke.category === 'string', `Joke ${index}: category should be string`);
      assert(joke.category.length > 0, `Joke ${index}: category should not be empty`);
      assert(validCategories.includes(joke.category.toLowerCase()), `Joke ${index}: category '${joke.category}' should be valid`);
    });
  });

  // Test 5: Explanation validation
  test('Explanation validation', () => {
    jokes.forEach((joke, index) => {
      assert(typeof joke.explanation === 'string', `Joke ${index}: explanation should be string`);
      assert(joke.explanation.length > 20, `Joke ${index}: explanation should be longer than 20 characters`);
      assert(!joke.explanation.startsWith('Explanation:'), `Joke ${index}: explanation should not start with 'Explanation:'`);
    });
  });

  // Test 6: No duplicate jokes
  test('No duplicate jokes', () => {
    const jokeTexts = jokes.map(j => j.text);
    const uniqueJokes = new Set(jokeTexts);
    assert(uniqueJokes.size === jokeTexts.length, 'Should not have duplicate jokes');
  });

  // Test 7: Family-friendly content
  test('Family-friendly content', () => {
    const badWords = ['badword1', 'badword2', 'badword3']; // Add any words you want to filter
    
    jokes.forEach((joke, index) => {
      const text = joke.text.toLowerCase();
      const explanation = joke.explanation.toLowerCase();
      
      badWords.forEach(word => {
        assert(!text.includes(word), `Joke ${index}: text should not contain '${word}'`);
        assert(!explanation.includes(word), `Joke ${index}: explanation should not contain '${word}'`);
      });
    });
  });

  // Test 8: Categories distribution
  test('Categories distribution', () => {
    const categoryCount = {};
    jokes.forEach(joke => {
      categoryCount[joke.category] = (categoryCount[joke.category] || 0) + 1;
    });
    
    // Each category should have at least 2 jokes
    Object.keys(categoryCount).forEach(category => {
      assert(categoryCount[category] >= 2, `Category '${category}' should have at least 2 jokes`);
    });
  });

  // Test 9: Joke format consistency
  test('Joke format consistency', () => {
    jokes.forEach((joke, index) => {
      // Jokes should start with a question or statement
      const firstLine = joke.text.split('\n')[0];
      assert(firstLine.length > 5, `Joke ${index}: first line should be substantial`);
      
      // Should have a punchline (second line)
      const lines = joke.text.split('\n');
      assert(lines.length >= 2, `Joke ${index}: should have at least 2 lines`);
      assert(lines[1].length > 0, `Joke ${index}: punchline should not be empty`);
    });
  });

  // Test 10: Explanation quality
  test('Explanation quality', () => {
    jokes.forEach((joke, index) => {
      const explanation = joke.explanation;
      
      // Explanation should be educational
      assert(explanation.length >= 50, `Joke ${index}: explanation should be detailed`);
      
      // Should mention quantum concepts
      const quantumTerms = ['quantum', 'qubit', 'superposition', 'entanglement', 'particle', 'wave', 'state'];
      const hasQuantumTerm = quantumTerms.some(term => explanation.toLowerCase().includes(term));
      assert(hasQuantumTerm, `Joke ${index}: explanation should mention quantum concepts`);
    });
  });

  // Summary
  console.log(`\nTest Results: ${passed} passed, ${failed} failed`);
  
  if (failed === 0) {
    console.log('All joke tests passed! 🎉');
    return true;
  } else {
    console.log('Some joke tests failed! ❌');
    return false;
  }
}

// Run tests if called directly
if (require.main === module) {
  const success = runJokeTests();
  process.exit(success ? 0 : 1);
}

module.exports = { runJokeTests };
