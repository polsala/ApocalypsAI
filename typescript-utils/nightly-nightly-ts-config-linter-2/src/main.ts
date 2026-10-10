import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

// Define a type for a linting rule
interface LintRule {
  name: string;
  description: string;
  check: (config: any, filePath: string) => LintError[];
}

// Define a type for a linting error
interface LintError {
  rule: string;
  message: string;
  filePath: string;
  line?: number;
  column?: number;
}

// --- Linting Rules ---

const requiredFieldsRule: LintRule = {
  name: 'required-fields',
  description: 'Ensures specified fields are present in the configuration.',
  check: (config: any, filePath: string): LintError[] => {
    const errors: LintError[] = [];
    const requiredFields = ['version', 'name']; // Example required fields

    requiredFields.forEach(field => {
      if (!(field in config)) {
        errors.push({
          rule: this.name,
          message: `Required field '${field}' is missing.`,
          filePath: filePath
        });
      }
    });
    return errors;
  }
};

const noEmptyStringsRule: LintRule = {
  name: 'no-empty-strings',
  description: 'Checks for empty string values in configuration.',
  check: (config: any, filePath: string): LintError[] => {
    const errors: LintError[] = [];
    const checkObject = (obj: any, currentPath: string) => {
      for (const key in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, key)) {
          const value = obj[key];
          const newPath = currentPath ? `${currentPath}.${key}` : key;
          if (typeof value === 'string' && value.trim() === '') {
            errors.push({
              rule: this.name,
              message: `Field '${newPath}' has an empty string value.`,
              filePath: filePath
            });
          } else if (typeof value === 'object' && value !== null) {
            checkObject(value, newPath);
          }
        }
      }
    };
    checkObject(config, '');
    return errors;
  }
};

// Add more rules here as needed
const allRules: LintRule[] = [
  requiredFieldsRule,
  noEmptyStringsRule
];

// --- File Parsing ---

function parseConfigFile(filePath: string): any {
  const ext = path.extname(filePath).toLowerCase();
  const fileContent = fs.readFileSync(filePath, 'utf-8');

  switch (ext) {
    case '.json':
      return JSON.parse(fileContent);
    case '.yaml':
    case '.yml':
      return yaml.load(fileContent);
    default:
      throw new Error(`Unsupported file extension: ${ext}`);
  }
}

// --- Main Linter Logic ---

function lintConfig(filePath: string): LintError[] {
  let configData;
  try {
    configData = parseConfigFile(filePath);
  } catch (error: any) {
    return [{
      rule: 'parsing',
      message: `Failed to parse file: ${error.message}`,
      filePath: filePath
    }];
  }

  const errors: LintError[] = [];
  allRules.forEach(rule => {
    try {
      const ruleErrors = rule.check(configData, filePath);
      errors.push(...ruleErrors);
    } catch (ruleError: any) {
      errors.push({
        rule: rule.name,
        message: `Error during rule execution: ${ruleError.message}`,
        filePath: filePath
      });
    }
  });

  return errors;
}

// --- CLI Entry Point ---

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: nightly-ts-config-linter <path_to_config_file>');
    process.exit(1);
  }

  const filePath = path.resolve(args[0]);

  if (!fs.existsSync(filePath)) {
    console.error(`Error: File not found at ${filePath}`);
    process.exit(1);
  }

  const lintErrors = lintConfig(filePath);

  if (lintErrors.length > 0) {
    console.error(`Linting failed for ${filePath}:`);
    lintErrors.forEach(error => {
      console.error(`  - [${error.rule}] ${error.message}`);
    });
    process.exit(1);
  } else {
    console.log(`Linting successful for ${filePath}. No issues found.`);
    process.exit(0);
  }
}

if (require.main === module) {
  main();
}

export { lintConfig, LintRule, LintError };
