import * as fs from 'fs';
import * as path from 'path';
import Ajv from 'ajv';

// Define types for command line arguments
interface Args {
  config: string;
  schema: string;
}

// Function to parse command line arguments
function parseArgs(argv: string[]): Args {
  const args: Partial<Args> = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--config' && i + 1 < argv.length) {
      args.config = argv[++i];
    } else if (argv[i] === '--schema' && i + 1 < argv.length) {
      args.schema = argv[++i];
    }
  }

  if (!args.config || !args.schema) {
    console.error('Error: --config and --schema arguments are required.');
    process.exit(1);
  }

  return args as Args;
}

// Function to read and parse JSON file
function readJsonFile(filePath: string): any {
  try {
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(fileContent);
  } catch (error: any) {
    console.error(`Error reading or parsing file ${filePath}: ${error.message}`);
    process.exit(1);
  }
}

// Main validation function
function validateConfig(config: any, schema: any): string[] {
  const ajv = new Ajv();
  const validate = ajv.compile(schema);
  const valid = validate(config);

  if (!valid) {
    const errors: string[] = [];
    if (validate.errors) {
      validate.errors.forEach(err => {
        errors.push(`- ${err.instancePath || 'root'} ${err.message}`);
      });
    }
    return errors;
  }
  return [];
}

// Entry point of the script
function main() {
  const args = parseArgs(process.argv.slice(2));

  const configPath = path.resolve(args.config);
  const schemaPath = path.resolve(args.schema);

  const configData = readJsonFile(configPath);
  const schemaData = readJsonFile(schemaPath);

  const validationErrors = validateConfig(configData, schemaData);

  if (validationErrors.length > 0) {
    console.error('Configuration validation failed:');
    validationErrors.forEach(error => console.error(error));
    process.exit(1);
  } else {
    console.log('Configuration is valid.');
    process.exit(0);
  }
}

// Execute main function
if (require.main === module) {
  main();
}

export { validateConfig, parseArgs, readJsonFile };
