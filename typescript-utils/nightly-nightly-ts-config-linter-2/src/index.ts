import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

interface LintResult {
  filePath: string;
  errors: string[];
}

function lintJson(filePath: string): LintResult {
  const errors: string[] = [];
  try {
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    JSON.parse(fileContent);
    // Add more specific JSON linting rules here if needed
    if (fileContent.includes('//')) {
      errors.push('JSON files should not contain comments (//).');
    }
  } catch (e: any) {
    errors.push(`JSON parsing error: ${e.message}`);
  }
  return { filePath, errors };
}

function lintYaml(filePath: string): LintResult {
  const errors: string[] = [];
  try {
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    yaml.load(fileContent);
    // Add more specific YAML linting rules here if needed
    if (fileContent.includes('  #')) { // Basic check for commented lines
      errors.push('YAML files should use `#` for comments, not `  #`.');
    }
  } catch (e: any) {
    errors.push(`YAML parsing error: ${e.message}`);
  }
  return { filePath, errors };
}

function lintConfig(filePath: string): LintResult {
  const absolutePath = path.resolve(filePath);
  const ext = path.extname(absolutePath).toLowerCase();

  if (ext === '.json') {
    return lintJson(absolutePath);
  } else if (ext === '.yaml' || ext === '.yml') {
    return lintYaml(absolutePath);
  } else {
    return { filePath: absolutePath, errors: [`Unsupported file extension: ${ext}`] };
  }
}

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: nightly-ts-config-linter <path_to_config_file>');
    process.exit(1);
  }

  const filePath = args[0];
  const result = lintConfig(filePath);

  if (result.errors.length > 0) {
    console.error(`Linting failed for: ${result.filePath}`);
    result.errors.forEach(error => console.error(`- ${error}`));
    process.exit(1);
  } else {
    console.log(`Linting successful for: ${result.filePath}`);
    process.exit(0);
  }
}

if (require.main === module) {
  main();
}

export { lintConfig, LintResult };
