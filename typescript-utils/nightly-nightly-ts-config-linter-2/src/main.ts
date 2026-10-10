import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

// Define a type for our linting rules
interface LintRule {
  name: string;
  description: string;
  check: (config: any, filePath: string) => LintError[] | null;
}

interface LintError {
  ruleName: string;
  message: string;
  filePath: string;
  line?: number;
  column?: number;
}

// --- Whimsical Linting Rules ---

const rules: LintRule[] = [
  {
    name: "no-empty-values",
    description: "Ensures no configuration values are empty strings.",
    check: (config: any, filePath: string): LintError[] | null => {
      const errors: LintError[] = [];
      const checkObject = (obj: any, currentPath: string = ''): void => {
        for (const key in obj) {
          if (Object.prototype.hasOwnProperty.call(obj, key)) {
            const newPath = currentPath ? `${currentPath}.${key}` : key;
            if (typeof obj[key] === 'string' && obj[key].trim() === '') {
              errors.push({
                ruleName: "no-empty-values",
                message: `Configuration key '${newPath}' has an empty string value.`,
                filePath: filePath,
              });
            } else if (typeof obj[key] === 'object' && obj[key] !== null) {
              checkObject(obj[key], newPath);
            }
          }
        }
      };
      checkObject(config);
      return errors.length > 0 ? errors : null;
    }
  },
  {
    name: "require-api-key",
    description: "Checks if an 'apiKey' field is present (case-insensitive).",
    check: (config: any, filePath: string): LintError[] | null => {
      const apiKeyKeys = Object.keys(config).filter(key => key.toLowerCase() === 'apikey');
      if (apiKeyKeys.length === 0) {
        return [
          {
            ruleName: "require-api-key",
            message: "Configuration is missing an 'apiKey' field. This is crucial for many services!",
            filePath: filePath,
          }
        ];
      }
      return null;
    }
  },
  {
    name: "no-sensitive-data-in-comments",
    description: "Warns if comments contain potentially sensitive information.",
    check: (config: any, filePath: string): LintError[] | null => {
      // This rule is a bit more complex for structured data like JSON/YAML
      // For simplicity, we'll assume comments are part of the raw file content
      // In a real-world scenario, you'd parse comments separately if supported by the parser.
      // For this example, we'll simulate by checking for common sensitive keywords in a hypothetical comment field.
      const errors: LintError[] = [];
      if (config.comments && typeof config.comments === 'string') {
        const sensitiveKeywords = ['password', 'secret', 'token', 'credentials'];
        const lowerCaseComment = config.comments.toLowerCase();
        sensitiveKeywords.forEach(keyword => {
          if (lowerCaseComment.includes(keyword)) {
            errors.push({
              ruleName: "no-sensitive-data-in-comments",
              message: `Comment might contain sensitive information: '${keyword}'. Please review.`,
              filePath: filePath,
            });
          }
        });
      }
      return errors.length > 0 ? errors : null;
    }
  }
];

// --- Helper Functions ---

function parseConfig(filePath: string): any {
  const fileExtension = path.extname(filePath).toLowerCase();
  const fileContent = fs.readFileSync(filePath, 'utf-8');

  try {
    if (fileExtension === '.json') {
      return JSON.parse(fileContent);
    } else if (fileExtension === '.yaml' || fileExtension === '.yml') {
      return yaml.load(fileContent);
    } else {
      throw new Error(`Unsupported file extension: ${fileExtension}`);
    }
  } catch (error: any) {
    throw new Error(`Failed to parse ${filePath}: ${error.message}`);
  }
}

function runLinter(filePath: string): LintError[] {
  const allErrors: LintError[] = [];
  try {
    const config = parseConfig(filePath);
    for (const rule of rules) {
      const ruleErrors = rule.check(config, filePath);
      if (ruleErrors) {
        allErrors.push(...ruleErrors);
      }
    }
  } catch (error: any) {
    allErrors.push({
      ruleName: "parsing-error",
      message: error.message,
      filePath: filePath,
    });
  }
  return allErrors;
}

// --- Main Execution ---

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: nightly-ts-config-linter <path_to_config_file>");
    process.exit(1);
  }

  const filePath = path.resolve(args[0]);
  const lintErrors = runLinter(filePath);

  if (lintErrors.length > 0) {
    console.error(`\n✨ Found ${lintErrors.length} linting issue(s) in ${filePath}:\n`);
    lintErrors.forEach(error => {
      console.error(`- [${error.ruleName}] ${error.message} (File: ${error.filePath}${error.line ? `, Line: ${error.line}` : ''}${error.column ? `, Column: ${error.column}` : ''})`);
    });
    process.exit(1);
  } else {
    console.log(`\n✅ Configuration file ${filePath} looks surprisingly tidy! No issues found.`);
    process.exit(0);
  }
}

main();
