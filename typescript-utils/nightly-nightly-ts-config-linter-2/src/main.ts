import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

// Define a type for a linting rule
interface LintRule {
  name: string;
  description: string;
  check: (config: any) => LintError[];
}

// Define a type for a linting error
interface LintError {
  rule: string;
  message: string;
  path?: string;
}

// --- Linting Rules ---

const requiredKeysRule: LintRule = {
  name: 'required-keys',
  description: 'Ensures essential keys are present in the configuration.',
  check: (config: any): LintError[] => {
    const errors: LintError[] = [];
    const required = ['version', 'settings']; // Example required keys
    required.forEach(key => {
      if (!(key in config)) {
        errors.push({
          rule: this.name,
          message: `Required key '${key}' is missing.`, 
          path: ''
        });
      }
    });
    return errors;
  }
};

const noEmptyObjectsRule: LintRule = {
  name: 'no-empty-objects',
  description: 'Disallows empty objects where they might indicate an oversight.',
  check: (config: any, currentPath: string = ''): LintError[] => {
    let errors: LintError[] = [];
    if (typeof config === 'object' && config !== null && !Array.isArray(config)) {
      if (Object.keys(config).length === 0) {
        errors.push({
          rule: this.name,
          message: `Object at path '${currentPath}' is empty.`, 
          path: currentPath
        });
      } else {
        for (const key in config) {
          if (Object.prototype.hasOwnProperty.call(config, key)) {
            errors = errors.concat(this.check(config[key], currentPath ? `${currentPath}.${key}` : key));
          }
        }
      }
    }
    return errors;
  }
};

const allRules: LintRule[] = [
  requiredKeysRule,
  noEmptyObjectsRule
];

// --- File Parsing ---

function parseConfig(filePath: string): any {
  const ext = path.extname(filePath).toLowerCase();
  const content = fs.readFileSync(filePath, 'utf-8');

  if (ext === '.json') {
    return JSON.parse(content);
  } else if (ext === '.yaml' || ext === '.yml') {
    return yaml.load(content);
  } else {
    throw new Error(`Unsupported file extension: ${ext}. Only JSON and YAML are supported.`);
  }
}

// --- Main Linter Logic ---

function lintConfig(filePath: string): LintError[] {
  let config: any;
  try {
    config = parseConfig(filePath);
  } catch (error: any) {
    return [{ rule: 'parsing-error', message: error.message }];
  }

  let allErrors: LintError[] = [];
  allRules.forEach(rule => {
    const ruleErrors = rule.check(config);
    allErrors = allErrors.concat(ruleErrors);
  });

  return allErrors;
}

// --- CLI Entry Point ---

function main() {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error('Usage: nightly-ts-config-linter <path_to_config_file>');
    process.exit(1);
  }

  const filePath = path.resolve(args[0]);

  if (!fs.existsSync(filePath)) {
    console.error(`Error: File not found at '${filePath}'`);
    process.exit(1);
  }

  const errors = lintConfig(filePath);

  if (errors.length > 0) {
    console.error(`Linting failed for '${filePath}':`);
    errors.forEach(err => {
      console.error(`  - [${err.rule}] ${err.message}${err.path ? ` (Path: ${err.path})` : ''}`);
    });
    process.exit(1);
  } else {
    console.log(`Linting successful for '${filePath}'. No issues found.`);
    process.exit(0);
  }
}

if (require.main === module) {
  main();
}

export { lintConfig, LintError, LintRule };
