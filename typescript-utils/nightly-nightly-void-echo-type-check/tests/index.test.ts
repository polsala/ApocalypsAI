import { VoidEchoTypeChecker } from '../src/index';
import { VoidEchoSchemaDefinition } from '../src/types';

describe('VoidEchoTypeChecker', () => {
  let checker: VoidEchoTypeChecker;

  beforeEach(() => {
    checker = new VoidEchoTypeChecker();
  });

  describe('registerSchema', () => {
    it('should register a new schema', () => {
      const schema: VoidEchoSchemaDefinition = { type: 'string', pattern: 'test' };
      checker.registerSchema('my-schema', schema);
      // # Mock rationale: Internal state of the checker is being tested. No external dependencies.
      expect((checker as any).schemas.get('my-schema')).toEqual(schema);
    });

    it('should warn and overwrite if schema name already exists', () => {
      const schema1: VoidEchoSchemaDefinition = { type: 'string', pattern: 'test1' };
      const schema2: VoidEchoSchemaDefinition = { type: 'string', pattern: 'test2' };
      checker.registerSchema('my-schema', schema1);
      const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {}); // # Mock rationale: Suppress console warning for test output, verify call.
      checker.registerSchema('my-schema', schema2);
      expect(consoleWarnSpy).toHaveBeenCalledWith('Schema "my-schema" already registered. Overwriting.');
      expect((checker as any).schemas.get('my-schema')).toEqual(schema2);
      consoleWarnSpy.mockRestore();
    });
  });

  describe('validate - string schemas', () => {
    beforeEach(() => {
      checker.registerSchema('status-message', { type: 'string', pattern: '^Status: (OK|ERROR) - .+$' });
    });

    it('should return isValid true for a matching string message', () => {
      const result = checker.validate('status-message', 'Status: OK - System operational.');
      expect(result.isValid).toBe(true);
      expect(result.errors).toBeUndefined();
    });

    it('should return isValid false for a non-matching string message', () => {
      const result = checker.validate('status-message', 'System operational.');
      expect(result.isValid).toBe(false);
      expect(result.errors).toEqual(['Message does not match pattern "^Status: (OK|ERROR) - .+".']);
    });

    it('should return isValid false if message is not a string', () => {
      const result = checker.validate('status-message', { status: 'OK' });
      expect(result.isValid).toBe(false);
      expect(result.errors).toEqual(['Expected a string message for this schema.']);
    });
  });

  describe('validate - JSON schemas', () => {
    beforeEach(() => {
      checker.registerSchema('event-log', {
        type: 'json',
        properties: {
          id: { type: 'string', required: true },
          timestamp: { type: 'number', required: true },
          severity: { type: 'string', required: true, enum: ['LOW', 'MEDIUM', 'HIGH'] },
          details: { type: 'object', required: false } // Simplified object type check
        }
      });
    });

    it('should return isValid true for a matching JSON message', () => {
      const message = {
        id: 'evt-123',
        timestamp: 1678886400000,
        severity: 'MEDIUM',
        details: { user: 'admin' }
      };
      const result = checker.validate('event-log', message);
      expect(result.isValid).toBe(true);
      expect(result.errors).toBeUndefined();
    });

    it('should return isValid false for missing required properties', () => {
      const message = {
        id: 'evt-123',
        severity: 'LOW'
      };
      const result = checker.validate('event-log', message);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Missing required property: "timestamp".');
    });

    it('should return isValid false for incorrect property types', () => {
      const message = {
        id: 'evt-123',
        timestamp: 'not-a-number', // Incorrect type
        severity: 'HIGH'
      };
      const result = checker.validate('event-log', message);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Property "timestamp" has incorrect type. Expected "number", got "string".');
    });

    it('should return isValid false for enum mismatch', () => {
      const message = {
        id: 'evt-123',
        timestamp: 1678886400000,
        severity: 'CRITICAL' // Not in enum
      };
      const result = checker.validate('event-log', message);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Property "severity" value "CRITICAL" is not one of the allowed enum values: LOW, MEDIUM, HIGH.');
    });

    it('should return isValid false for unexpected properties', () => {
      const message = {
        id: 'evt-123',
        timestamp: 1678886400000,
        severity: 'LOW',
        extraField: 'unexpected'
      };
      const result = checker.validate('event-log', message);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Unexpected property: "extraField".');
    });

    it('should return isValid false if message is not an object', () => {
      const result = checker.validate('event-log', 'not-an-object');
      expect(result.isValid).toBe(false);
      expect(result.errors).toEqual(['Expected a JSON object message for this schema.']);
    });

    it('should handle optional properties correctly', () => {
      const message = {
        id: 'evt-123',
        timestamp: 1678886400000,
        severity: 'LOW'
      };
      const result = checker.validate('event-log', message);
      expect(result.isValid).toBe(true);
      expect(result.errors).toBeUndefined();
    });

    it('should handle array type correctly', () => {
      checker.registerSchema('array-test', {
        type: 'json',
        properties: {
          items: { type: 'array', required: true }
        }
      });
      const validArrayMessage = { items: [1, 2, 3] };
      const invalidArrayMessage = { items: 'not-an-array' };
      expect(checker.validate('array-test', validArrayMessage).isValid).toBe(true);
      expect(checker.validate('array-test', invalidArrayMessage).isValid).toBe(false);
      expect(checker.validate('array-test', invalidArrayMessage).errors).toContain('Property "items" has incorrect type. Expected "array", got "string".');
    });

    it('should handle object type correctly', () => {
      checker.registerSchema('object-test', {
        type: 'json',
        properties: {
          data: { type: 'object', required: true }
        }
      });
      const validObjectMessage = { data: { key: 'value' } };
      const invalidObjectMessage = { data: 'not-an-object' };
      expect(checker.validate('object-test', validObjectMessage).isValid).toBe(true);
      expect(checker.validate('object-test', invalidObjectMessage).isValid).toBe(false);
      expect(checker.validate('object-test', invalidObjectMessage).errors).toContain('Property "data" has incorrect type. Expected "object", got "string".');
    });
  });

  it('should return isValid false if schema is not found', () => {
    const result = checker.validate('non-existent-schema', 'any message');
    expect(result.isValid).toBe(false);
    expect(result.errors).toEqual(['Schema "non-existent-schema" not found.']);
  });
});
