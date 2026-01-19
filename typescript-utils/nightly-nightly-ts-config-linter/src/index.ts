import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import Ajv from 'ajv';

interface ConfigLintOptions {
  schemaPath?: string;
}

interface LintResult {
  filePath: string;
  errors: string[];
}

const ajv = new Ajv();

function parseConfig(filePath: string): any {
  const ext = path.extname(filePath).toLowerCase();
  const fileContent = fs.readFileSync(filePath, 'utf8');

  if (ext === '.json') {
    return JSON.parse(fileContent);
  } else if (ext === '.yaml' || ext === '.yml') {
    return yaml.load(fileContent);
  } else {
    throw new Error(`Unsupported file extension: ${ext}`);
  }
}

function loadSchema(schemaPath: string): any {
  if (!fs.existsSync(schemaPath)) {
    throw new Error(`Schema file not found: ${schemaPath}`);
  }
  const schemaContent = fs.readFileSync(schemaPath, 'utf8');
  try {
    return JSON.parse(schemaContent);
  } catch (e) {
    throw new Error(`Invalid JSON schema: ${e.message}`);
  }
}

export function lintConfig(filePath: string, options: ConfigLintOptions = {}): LintResult {
  const errors: string[] = [];
  let configData;

  try {
    configData = parseConfig(filePath);
  } catch (e: any) {
    errors.push(`Failed to parse config file: ${e.message}`);
    return { filePath, errors };
  }

  if (options.schemaPath) {
    try {
      const schema = loadSchema(options.schemaPath);
      const validate = ajv.compile(schema);
      const valid = validate(configData);
      if (!valid) {
        validate.errors?.forEach(err => {
          errors.push(`Schema validation error at ${err.instancePath}: ${err.message}`);
        });
      }
    } catch (e: any) {
      errors.push(`Schema processing error: ${e.message}`);
    }
  }

  // Add more generic checks here if needed, e.g., checking for empty files, specific keys etc.
  if (Object.keys(configData).length === 0 && !options.schemaPath) {
      errors.push('Configuration file is empty and no schema was provided for validation.');
  }

  return { filePath, errors };
}

// CLI execution logic
if (require.main === module) {
  const args = process.argv.slice(2);
  let filePath = '';
  let schemaPath = '';

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--schema' && args[i+1]) {
      schemaPath = args[i+1];
      i++;
    } else {
      filePath = args[i];
    }
  }

  if (!filePath) {
    console.error('Usage: nightly-ts-config-linter <file_path> [--schema <schema_path>]');
    process.exit(1);
  }

  try {
    const result = lintConfig(path.resolve(filePath), { schemaPath: schemaPath ? path.resolve(schemaPath) : undefined });
    if (result.errors.length > 0) {
      console.error(`Linting failed for ${result.filePath}:`);
      result.errors.forEach(err => console.error(`  - ${err}`));
      process.exit(1);
    } else {
      console.log(`Linting successful for ${result.filePath}. No errors found.`);
      process.exit(0);
    }
  } catch (e: any) {
    console.error(`An unexpected error occurred: ${e.message}`);
    process.exit(1);
  }
}
