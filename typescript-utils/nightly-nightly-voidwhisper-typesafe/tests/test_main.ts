import { createConfigSchema } from '../src/main';

// Mock rationale: Testing different combinations of inputs without actual process.env manipulation

function runTests() {
  let passed = 0;
  let failed = 0;

  function test(name: string, fn: () => void) {
    try {
      fn();
      console.log(`✅ ${name}`);
      passed++;
    } catch (err) {
      console.error(`❌ ${name}: ${(err as Error).message}`);
      failed++;
    }
  }

  test('should accept valid number', () => {
    const schema = createConfigSchema({ PORT: { type: 'number', required: true } });
    const result = schema.parse({ PORT: '3000' });
    if (result.PORT !== 3000) throw new Error('Expected 3000');
  });

  test('should fail invalid number', () => {
    const schema = createConfigSchema({ PORT: { type: 'number', required: true } });
    try {
      schema.parse({ PORT: 'not_a_number' });
      throw new Error('Should have thrown');
    } catch (e) {
      if ((e as Error).message.includes('Invalid number')) return;
      throw e;
    }
  });

  test('should use default when missing optional field', () => {
    const schema = createConfigSchema({ NODE_ENV: { type: 'string', required: false, default: 'production' } });
    const result = schema.parse({});
    if (result.NODE_ENV !== 'production') throw new Error('Expected production');
  });

  test('should throw on missing required field', () => {
    const schema = createConfigSchema({ API_KEY: { type: 'string', required: true } });
    try {
      schema.parse({});
      throw new Error('Should have thrown');
    } catch (e) {
      if (!(e instanceof Error && e.message.includes('Missing required field'))) throw e;
    }
  });

  test('should correctly parse boolean values', () => {
    const schema = createConfigSchema({ DEBUG: { type: 'boolean', required: true } });
    const result1 = schema.parse({ DEBUG: 'true' });
    const result2 = schema.parse({ DEBUG: 'false' });
    if (result1.DEBUG !== true) throw new Error('Expected true');
    if (result2.DEBUG !== false) throw new Error('Expected false');
  });

  test('should fail invalid boolean value', () => {
    const schema = createConfigSchema({ DEBUG: { type: 'boolean', required: true } });
    try {
      schema.parse({ DEBUG: 'yes' });
      throw new Error('Should have thrown');
    } catch (e) {
      if (!(e instanceof Error && e.message.includes('Invalid boolean'))) throw e;
    }
  });

  console.log(`\nTests completed: ${passed} passed, ${failed} failed`);
  if (failed > 0) process.exit(1);
}

runTests();
