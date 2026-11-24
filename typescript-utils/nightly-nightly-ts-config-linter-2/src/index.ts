import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

interface LintError {
  filePath: string;
  message: string;
  line?: number;
  column?: number;
}

interface LinterConfig {
  requiredFields?: string[];
  expectedTypes?: { [key: string]: 'string' | 'number' | 'boolean' | 'object' | 'array' };
}

const defaultLinterConfig: LinterConfig = {
  requiredFields: [],
  expectedTypes: {}
};

function lintJson(filePath: string, content: string, config: LinterConfig): LintError[] {
  const errors: LintError[] = [];
  try {
    const jsonData = JSON.parse(content);

    // Check required fields
    if (config.requiredFields) {
      for (const field of config.requiredFields) {
        if (!(field in jsonData)) {
          errors.push({
            filePath,
            message: `Missing required field: \'${field}\'`
          });
        }
      }
    }

    // Check expected types
    if (config.expectedTypes) {
      for (const field in config.expectedTypes) {
        if (field in jsonData) {
          const expectedType = config.expectedTypes[field];
          const actualType = typeof jsonData[field];
          if (actualType !== expectedType) {
            errors.push({
              filePath,
              message: `Type mismatch for field \'${field}\': expected \'${expectedType}\' but got \'${actualType}\'`
            });
          }
        }
      }
    }

  } catch (e: any) {
    errors.push({
      filePath,
      message: `Invalid JSON syntax: ${e.message}`
    });
  }
  return errors;
}

function lintYaml(filePath: string, content: string, config: LinterConfig): LintError[] {
  const errors: LintError[] = [];
  try {
    const yamlData = yaml.load(content);

    // Check required fields
    if (config.requiredFields) {
      for (const field of config.requiredFields) {
        if (!(field in yamlData as object)) {
          errors.push({
            filePath,
            message: `Missing required field: \'${field}\'`
          });
        }
      }
    }

    // Check expected types
    if (config.expectedTypes) {
      for (const field in config.expectedTypes) {
        if (field in (yamlData as object)) {
          const expectedType = config.expectedTypes[field];
          const actualType = typeof (yamlData as any)[field];
          if (actualType !== expectedType) {
            errors.push({
              filePath,
              message: `Type mismatch for field \'${field}\': expected \'${expectedType}\' but got \'${actualType}\'`
            });
          }
        }
      }
    }

  } catch (e: any) {
    errors.push({
      filePath,
      message: `Invalid YAML syntax: ${e.message}`
    });
  }
  return errors;
}

function lintConfig(filePath: string, config: LinterConfig = defaultLinterConfig): void {
  if (!fs.existsSync(filePath)) {
    console.error(`Error: File not found at \'${filePath}\'`);
    process.exit(1);
  }

  const content = fs.readFileSync(filePath, 'utf-8');
  const ext = path.extname(filePath).toLowerCase();
  let errors: LintError[] = [];

  if (ext === '.json') {
    errors = lintJson(filePath, content, config);
  } else if (ext === '.yaml' || ext === '.yml') {
    errors = lintYaml(filePath, content, config);
  } else {
    console.warn(`Warning: Unsupported file extension \'${ext}\'. Only JSON and YAML are supported.`);
    return;
  }

  if (errors.length > 0) {
    console.error(`Linting failed for \'${filePath}\':`);
    errors.forEach(err => {
      console.error(`  - ${err.message}`);
    });
    process.exit(1);
  } else {
    console.log(`Linting successful for \'${filePath}\'`);
  }
}

// Command line argument parsing
const args = process.argv.slice(2);

if (args.length === 0) {
  console.error('Usage: nightly-ts-config-linter <path_to_config_file>');
  process.exit(1);
}

const filePath = args[0];

// Example of how to use custom config (can be extended to read from a file)
const customConfig: LinterConfig = {
  requiredFields: ['name', 'version'],
  expectedTypes: {
    name: 'string',
    version: 'string',
    private: 'boolean'
  }
};

lintConfig(filePath, customConfig);
