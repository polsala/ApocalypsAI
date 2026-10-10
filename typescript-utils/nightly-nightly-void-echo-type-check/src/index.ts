import { VoidEchoSchemaDefinition, ValidationResult } from './types';

export class VoidEchoTypeChecker {
  private schemas: Map<string, VoidEchoSchemaDefinition> = new Map();

  /**
   * Registers a new schema for validating void echo messages.
   * If a schema with the same name already exists, it will be overwritten.
   * @param name The unique name for the schema.
   * @param schema The schema definition (string pattern or JSON properties).
   */
  registerSchema(name: string, schema: VoidEchoSchemaDefinition): void {
    if (this.schemas.has(name)) {
      console.warn(`Schema "${name}" already registered. Overwriting.`);
    }
    this.schemas.set(name, schema);
  }

  /**
   * Validates a given message against a registered schema.
   * @param schemaName The name of the schema to validate against.
   * @param message The message to validate. Can be a string or a JSON object.
   * @returns A ValidationResult indicating if the message is valid and any errors found.
   */
  validate(schemaName: string, message: string | object): ValidationResult {
    const schema = this.schemas.get(schemaName);
    if (!schema) {
      return { isValid: false, errors: [`Schema "${schemaName}" not found.`] };
    }

    if (schema.type === 'string') {
      if (typeof message !== 'string') {
        return { isValid: false, errors: ['Expected a string message for this schema.'] };
      }
      const regex = new RegExp(schema.pattern);
      if (!regex.test(message)) {
        return { isValid: false, errors: [`Message does not match pattern "${schema.pattern}".`] };
      }
    } else if (schema.type === 'json') {
      if (typeof message !== 'object' || message === null || Array.isArray(message)) {
        return { isValid: false, errors: ['Expected a JSON object message for this schema.'] };
      }
      const errors: string[] = [];
      const msgObj = message as Record<string, any>;

      for (const propName in schema.properties) {
        const propDef = schema.properties[propName];
        const value = msgObj[propName];

        if (propDef.required && value === undefined) {
          errors.push(`Missing required property: "${propName}".`);
          continue;
        }
        if (value === undefined) continue; // Not required and not present

        // Basic type checking
        let typeMatch = false;
        switch (propDef.type) {
          case 'string': typeMatch = typeof value === 'string'; break;
          case 'number': typeMatch = typeof value === 'number'; break;
          case 'boolean': typeMatch = typeof value === 'boolean'; break;
          case 'array': typeMatch = Array.isArray(value); break;
          case 'object': typeMatch = typeof value === 'object' && value !== null && !Array.isArray(value); break;
          default: typeMatch = false; // Should not happen with defined types
        }
        if (!typeMatch) {
          errors.push(`Property "${propName}" has incorrect type. Expected "${propDef.type}", got "${typeof value}".`);
        }

        // Enum checking
        if (propDef.enum && !propDef.enum.includes(value)) {
          errors.push(`Property "${propName}" value "${value}" is not one of the allowed enum values: ${propDef.enum.join(', ')}.`);
        }
      }

      // Check for extra properties not defined in schema
      for (const propName in msgObj) {
        if (!(propName in schema.properties)) {
          errors.push(`Unexpected property: "${propName}".`);
        }
      }

      if (errors.length > 0) {
        return { isValid: false, errors };
      }
    }

    return { isValid: true };
  }
}

/**
 * A singleton instance of the VoidEchoTypeChecker for convenience.
 * You can also create new instances if you need isolated schema registries.
 */
export const voidEchoTypeChecker = new VoidEchoTypeChecker();
