type PrimitiveType = 'string' | 'number' | 'boolean' | 'null';
type SchemaNode = PrimitiveType | Array<Schema> | { [key: string]: SchemaNode };
type Schema = { [key: string]: SchemaNode };

interface ValidationResult {
  valid: boolean;
  errors?: string[];
}

function getType(value: unknown): string {
  if (value === null) return 'null';
  if (Array.isArray(value)) return 'array';
  return typeof value;
}

export function createValidator(schema: Schema) {
  return function validate(data: any, basePath = ''): ValidationResult {
    const errors: string[] = [];

    for (const key in schema) {
      const expectedType = schema[key];
      const currentValue = data?.[key];
      const currentPath = basePath ? `${basePath}.${key}` : key;

      if (expectedType === 'array') {
        if (!Array.isArray(currentValue)) {
          errors.push(`Expected array at path '${currentPath}', got ${getType(currentValue)}`);
          continue;
        }

        // Handle array item validation later if needed
      } else if (typeof expectedType === 'object' && !Array.isArray(expectedType)) {
        if (getType(currentValue) !== 'object' || currentValue === null) {
          errors.push(`Expected object at path '${currentPath}', got ${getType(currentValue)}`);
          continue;
        }
        const nestedResult = validate(expectedType as any, currentValue, currentPath);
        if (!nestedResult.valid && nestedResult.errors) {
          errors.push(...nestedResult.errors);
        }
      } else {
        if (getType(currentValue) !== expectedType) {
          errors.push(
            `Expected ${expectedType} at path '${currentPath}', got ${getType(currentValue)}`
          );
        }
      }
    }

    return {
      valid: errors.length === 0,
      errors: errors.length > 0 ? errors : undefined
    };
  };
}
