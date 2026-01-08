const assert = require('assert');
const { defineDialects } = require('../src/dialects');

describe('defineDialects', () => {
  it('should create dialect objects with default values if not provided', () => {
    const dialectConfig = {
      simple: {}
    };
    const dialects = defineDialects(dialectConfig);
    assert.deepStrictEqual(dialects.simple, {
      prefix: '',
      suffix: '',
      transform: (msg) => msg
    }, 'Should have default empty prefix/suffix and identity transform');
  });

  it('should correctly apply provided prefix, suffix, and transform', () => {
    const mockTransform = (msg) => `TRANSFORMED(${msg})`;
    const dialectConfig = {
      complex: {
        prefix: '[PRE] ',
        suffix: ' [SUF]',
        transform: mockTransform
      }
    };
    const dialects = defineDialects(dialectConfig);
    const result = dialects.complex.transform("Hello");
    assert.strictEqual(result, "TRANSFORMED(Hello)", 'Transform function not applied correctly');
    assert.strictEqual(dialects.complex.prefix, '[PRE] ', 'Prefix not applied correctly');
    assert.strictEqual(dialects.complex.suffix, ' [SUF]', 'Suffix not applied correctly');
  });

  it('should handle multiple dialects', () => {
    const dialectConfig = {
      one: { prefix: '1' },
      two: { suffix: '2' }
    };
    const dialects = defineDialects(dialectConfig);
    assert.ok(dialects.one, 'Dialect "one" should exist');
    assert.ok(dialects.two, 'Dialect "two" should exist');
    assert.strictEqual(dialects.one.prefix, '1', 'Dialect "one" prefix incorrect');
    assert.strictEqual(dialects.two.suffix, '2', 'Dialect "two" suffix incorrect');
  });

  it('should return an empty object if no dialects are provided', () => {
    const dialects = defineDialects({});
    assert.deepStrictEqual(dialects, {}, 'Should return an empty object for empty config');
  });
});
