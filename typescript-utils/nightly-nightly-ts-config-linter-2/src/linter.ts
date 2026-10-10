import { ConfigError, ConfigRule } from './types';

/**
 * Safely retrieves a nested value from an object using a dot-notation path.
 * @param obj The object to traverse.
 * @param path The dot-notation path (e.g., 'user.address.city').
 * @returns The value at the specified path, or undefined if the path is invalid.
 */
function getNestedValue(obj: any, path: string): any {
  const keys = path.split('.');
  let current = obj;
  for (const key of keys) {
    if (current === null || typeof current !== 'object') {
      return undefined;
    }
    current = current[key];
  }
  return current;
}

/**
 * Lints a configuration object against a set of rules.
 * @param config The configuration object to lint.
 * @param rules An array of ConfigRule objects.
 * @returns An array of ConfigError objects for any violations found.
 */
export function lintConfig(config: any, rules: ConfigRule[]): ConfigError[] {
  const errors: ConfigError[] = [];

  for (const rule of rules) {
    const value = getNestedValue(config, rule.path);

    // If the path doesn't exist, we might want to flag it or ignore it depending on the rule's intent.
    // For now, we assume rules are for existing properties.
    if (value === undefined) {
      // Optionally, add an error if the path itself is expected to exist
      // errors.push({ path: rule.path, message: `Path does not exist` });
      continue;
    }

    if (!rule.validator(value)) {
      errors.push({
        path: rule.path,
        message: rule.description
      });
    }
  }

  return errors;
}
