export type ConfigType = 'string' | 'number' | 'boolean';

interface FieldDefinition {
  type: ConfigType;
  required?: boolean;
  default?: string | number | boolean;
}

interface SchemaDefinition {
  [key: string]: FieldDefinition;
}

interface ParsedConfig {
  [key: string]: string | number | boolean;
}

export function createConfigSchema(schemaDef: SchemaDefinition) {
  return {
    parse(envVars: Record<string, string | undefined>): ParsedConfig {
      const result: ParsedConfig = {};
      const errors: string[] = [];

      for (const [key, def] of Object.entries(schemaDef)) {
        const value = envVars[key];

        if (value === undefined || value === '') {
          if (def.required && def.default === undefined) {
            errors.push(`Missing required field: ${key}`);
            continue;
          }
          if (def.default !== undefined) {
            result[key] = def.default;
            continue;
          }
          result[key] = '';
          continue;
        }

        switch (def.type) {
          case 'number':
            const numValue = Number(value);
            if (isNaN(numValue)) {
              errors.push(`Invalid number for key: ${key}`);
            } else {
              result[key] = numValue;
            }
            break;
          case 'boolean':
            if (value.toLowerCase() === 'true') {
              result[key] = true;
            } else if (value.toLowerCase() === 'false') {
              result[key] = false;
            } else {
              errors.push(`Invalid boolean for key: ${key}`);
            }
            break;
          default:
            result[key] = value;
        }
      }

      if (errors.length > 0) {
        throw new Error(errors.join('; '));
      }

      return result;
    }
  };
}
