import { strict as assert } from 'assert'
import { nameColor } from '../src/index'

// Mock rationale: deterministic mapping based on RGB values

assert.equal(nameColor('#ff0000'), 'Scorching Ember')
assert.equal(nameColor('#00ff00'), 'Toxic Mire')
assert.equal(nameColor('#0000ff'), 'Frozen Glacier')
assert.equal(nameColor('#808080'), 'Dusty Ember')

console.log('All tests passed')
