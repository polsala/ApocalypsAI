import fs from 'fs';
import path from 'path';
import Ajv from 'ajv';

// Mock rationale: Ajv is a popular JSON schema validator library.
// We are using it here to perform the core validation logic.
const ajv = new Ajv({ allErrors: true });

interface ConfigArgs {
  config: string;
  schema: string;
}

function parseArgs(args: string[]): ConfigArgs {
  const configArgIndex = args.indexOf('--config');
  const schemaArgIndex = args.indexOf('--schema');

  if (configArgIndex === -1 || schemaArgIndex === -1 || configArgIndex + 1 >= args.length || schemaArgIndex + 1 >= args.length) {
    throw new Error('Usage: nightly-ts-config-linter --config <path-to-config-file> --schema <path-to-schema-file>');
  }

  return {
    config: path.resolve(args[configArgIndex + 1]),
    schema: path.resolve(args[schemaArgIndex + 1]),
  };
}

function loadFile(filePath: string): any {
  try {
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(fileContent);
  } catch (error: any) {
    throw new Error(`Failed to load or parse file ${filePath}: ${error.message}`);
  }
}

function lintConfig(config: any, schema: any): string[] {
  const validate = ajv.compile(schema);
  const valid = validate(config);

  if (!valid) {
    const errors = validate.errors?.map(err => {
      let message = '';
      if (err.instancePath) {
        message += `${err.instancePath.substring(1).replace(/\//g, '.')}: `;
      }
      message += err.message;
      return message;
    }) || ['Unknown validation error'];
    return errors;
  }
  return [];
}

function main() {
  try {
    const args = parseArgs(process.argv.slice(2));

    const configData = loadFile(args.config);
    const schemaData = loadFile(args.schema);

    const validationErrors = lintConfig(configData, schemaData);

    if (validationErrors.length > 0) {
      console.error('Configuration validation failed:');
      validationErrors.forEach(error => console.error(`  - ${error}`));
      process.exit(1);
    } else {
      console.log('Configuration is valid.');
      process.exit(0);
    }
  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main();
