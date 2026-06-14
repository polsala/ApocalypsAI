import { RELIC_SCHEMAS, SchemaDefinition } from './schemas';

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

/**
 * Recursively validates a data object against a schema definition.
 * @param data The data object to validate.
 * @param schema The schema definition to validate against.
 * @param path The current path in the data object (for error reporting).
 * @returns An array of error messages.
 */
function recursiveValidate(data: any, schema: SchemaDefinition, path: string): string[] {
  const errors: string[] = [];

  if (typeof data !== 'object' || data === null) {
    errors.push(`Expected object at path '${path}', but got ${typeof data}`);
    return errors;
  }

  // Check for missing required properties in data
  for (const key in schema) {
    if (schema.hasOwnProperty(key)) {
      const expectedType = schema[key];
      const dataValue = data[key];
      const currentPath = path ? `${path}.${key}` : key;

      if (!(key in data)) {
        // For simplicity, all properties in SchemaDefinition are considered required.
        // Optional properties would require a more complex SchemaDefinition (e.g., { type: 'string', optional: true }).
        errors.push(`Missing required property: ${currentPath}`);
        continue;
      }

      if (typeof expectedType === 'object') {
        // Nested object validation
        errors.push(...recursiveValidate(dataValue, expectedType, currentPath));
      } else {
        // Basic type validation
        const actualType = Array.isArray(dataValue) ? 'array' : typeof dataValue;
        if (actualType !== expectedType) {
          errors.push(`Property '${currentPath}' has incorrect type: expected ${expectedType}, got ${actualType}`);
        }
      }
    }
  }

  // Optionally, check for extra properties in data not defined in schema
  // For this utility, we'll allow extra properties for flexibility.

  return errors;
}

/**
 * Validates a given data object against a named relic schema.
 * @param schemaName The name of the schema to use for validation.
 * @param data The data object to validate.
 * @returns A ValidationResult object indicating validity and any errors.
 */
export function validateData(schemaName: string, data: any): ValidationResult {
  const schemaDefinition = RELIC_SCHEMAS[schemaName];

  if (!schemaDefinition) {
    return {
      isValid: false,
      errors: [`Unknown schema: ${schemaName}`]
    };
  }

  const errors = recursiveValidate(data, schemaDefinition, '');

  return {
    isValid: errors.length === 0,
    errors: errors
  };
}
