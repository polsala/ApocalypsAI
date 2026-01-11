import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

// Define a generic type for configuration files
interface ConfigFile {
  [key: string]: any;
}

// Define a type for linting rules
interface LintRule {
  name: string;
  description: string;
  check: (config: ConfigFile, filePath: string) => LintError[];
}

interface LintError {
  ruleName: string;
  message: string;
  filePath: string;
  severity: 'error' | 'warning';
}

// --- Linting Rules ---

const rules: LintRule[] = [
  {
    name: 'no-empty-config',
    description: 'Configuration file should not be empty.',
    check: (config: ConfigFile, filePath: string): LintError[] => {
      if (Object.keys(config).length === 0) {
        return [
          {
            ruleName: 'no-empty-config',
            message: 'Configuration file is empty.',
            filePath,
            severity: 'error',
          },
        ];
      }
      return [];
    },
  },
  {
    name: 'no-trailing-commas',
    description: 'Avoid trailing commas in JSON-like structures (applies to YAML too).',
    check: (config: ConfigFile, filePath: string): LintError[] => {
      // This is a simplified check. A full implementation would require AST parsing.
      // For now, we'll check for common YAML trailing comma patterns.
      const fileContent = fs.readFileSync(filePath, 'utf-8');
      const lines = fileContent.split('\n');
      const errors: LintError[] = [];
      lines.forEach((line, index) => {
        if (line.trim().endsWith(',') && !line.trim().endsWith('}')) { // Basic check, not perfect
          errors.push({
            ruleName: 'no-trailing-commas',
            message: `Potential trailing comma found on line ${index + 1}.`, 
            filePath,
            severity: 'warning',
          });
        }
      });
      return errors;
    },
  },
  // Add more rules here...
  // Example: Check for specific keys in package.json
  // { 
  //   name: 'require-version',
  //   description: 'package.json must have a version field.',
  //   check: (config: ConfigFile, filePath: string): LintError[] => {
  //     if (!config.version) {
  //       return [{ ruleName: 'require-version', message: 'Missing "version" field.', filePath, severity: 'error' }];
  //     }
  //     return [];
  //   }
  // }
];

// --- File Parsing ---

function parseConfigFile(filePath: string): ConfigFile | null {
  const ext = path.extname(filePath).toLowerCase();
  try {
    const fileContent = fs.readFileSync(filePath, 'utf-8');
    if (ext === '.json') {
      return JSON.parse(fileContent);
    } else if (ext === '.yaml' || ext === '.yml') {
      return yaml.load(fileContent) as ConfigFile;
    }
    console.error(`Unsupported file extension: ${ext}`);
    return null;
  } catch (error: any) {
    console.error(`Error parsing file ${filePath}: ${error.message}`);
    return null;
  }
}

// --- Linting Logic ---

function lintFile(filePath: string): LintError[] {
  const config = parseConfigFile(filePath);
  if (!config) {
    return [
      {
        ruleName: 'file-parsing-error',
        message: 'Failed to parse configuration file.',
        filePath,
        severity: 'error',
      },
    ];
  }

  let allErrors: LintError[] = [];
  for (const rule of rules) {
    try {
      const ruleErrors = rule.check(config, filePath);
      allErrors = allErrors.concat(ruleErrors);
    } catch (error: any) {
      console.error(`Error running rule ${rule.name} on ${filePath}: ${error.message}`);
      allErrors.push({
        ruleName: `rule-execution-error:${rule.name}`,
        message: `Error executing rule: ${error.message}`,
        filePath,
        severity: 'error',
      });
    }
  }
  return allErrors;
}

// --- CLI Entry Point ---

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: nightly-ts-config-linter <path_to_config_file>');
    process.exit(1);
  }

  const filePath = args[0];
  const absolutePath = path.resolve(filePath);

  if (!fs.existsSync(absolutePath)) {
    console.error(`Error: File not found at ${absolutePath}`);
    process.exit(1);
  }

  const errors = lintFile(absolutePath);

  if (errors.length > 0) {
    console.log(`Linting results for: ${absolutePath}`);
    errors.forEach(err => {
      console.log(`  [${err.severity.toUpperCase()}] ${err.ruleName}: ${err.message}`);
    });
    process.exit(1); // Exit with error code if there are errors
  } else {
    console.log(`✅ No linting issues found in ${absolutePath}`);
    process.exit(0);
  }
}

main();
