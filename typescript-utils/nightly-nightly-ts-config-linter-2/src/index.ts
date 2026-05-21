import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

interface LinterResult {
  filePath: string;
  errors: string[];
}

function lintJson(filePath: string): LinterResult {
  const errors: string[] = [];
  try {
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    JSON.parse(fileContent);
  } catch (e: any) {
    errors.push(`JSON parsing error: ${e.message}`);
  }
  return { filePath, errors };
}

function lintYaml(filePath: string): LinterResult {
  const errors: string[] = [];
  try {
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    yaml.load(fileContent);
  } catch (e: any) {
    errors.push(`YAML parsing error: ${e.message}`);
  }
  return { filePath, errors };
}

function lintFile(filePath: string): LinterResult {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === '.json') {
    return lintJson(filePath);
  } else if (ext === '.yaml' || ext === '.yml') {
    return lintYaml(filePath);
  } else {
    return { filePath, errors: [`Unsupported file extension: ${ext}`] };
  }
}

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: nightly-ts-config-linter <path_to_config_file>');
    process.exit(1);
  }

  const filePath = args[0];
  const result = lintFile(filePath);

  if (result.errors.length > 0) {
    console.error(`Linting errors found in ${result.filePath}:`);
    result.errors.forEach(error => console.error(`- ${error}`));
    process.exit(1);
  } else {
    console.log(`Configuration file ${result.filePath} linted successfully.`);
    process.exit(0);
  }
}

main();
