import { createValidator } from '../src/index';

// Mock rationale: Pure unit tests that do not require external resources or I/O.

describe('Voidbound Validator', () => {
  it('should accept matching flat structure', () => {
    const schema = { name: 'string', age: 'number' };
    const data = { name: 'Alice', age: 30 };
    const validator = createValidator(schema);
    const result = validator(data);
    expect(result.valid).toBe(true);
  });

  it('should reject wrong primitive types', () => {
    const schema = { active: 'boolean' };
    const data = { active: 'yes' };
    const validator = createValidator(schema);
    const result = validator(data);
    expect(result.valid).toBe(false);
    expect(result.errors).toContain("Expected boolean at path 'active', got string");
  });

  it('should handle nested objects correctly', () => {
    const schema = { user: { id: 'number', profile: { email: 'string' } } };
    const data = { user: { id: 123, profile: { email: 'test@example.com' } } };
    const validator = createValidator(schema);
    const result = validator(data);
    expect(result.valid).toBe(true);
  });

  it('should report missing keys', () => {
    const schema = { requiredField: 'string' };
    const data = {};
    const validator = createValidator(schema);
    const result = validator(data);
    expect(result.valid).toBe(false);
    expect(result.errors).toContain("Expected string at path 'requiredField', got undefined");
  });

  it('should detect incorrect nested structures', () => {
    const schema = { settings: { theme: 'string' } };
    const data = { settings: { theme: 123 } };
    const validator = createValidator(schema);
    const result = validator(data);
    expect(result.valid).toBe(false);
    expect(result.errors).toContain("Expected string at path 'settings.theme', got number");
  });
});
