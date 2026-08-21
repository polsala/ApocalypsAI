import { leetify } from '../src/main';
import * as assert from 'assert';

function runTests() {
  // Level 1 replaces basic characters
  assert.strictEqual(leetify('test', 1), '7357');

  // Level 2 adds b->8 and g->9
  assert.strictEqual(leetify('bag', 2), '849');

  // Level 3 adds Z->2
  assert.strictEqual(leetify('zoo', 3), '200');
}

runTests();
