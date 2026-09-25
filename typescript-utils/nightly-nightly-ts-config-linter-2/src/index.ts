import * as fs from 'fs/promises';
import * as path from 'path';
import yaml from 'js-yaml';

interface LintError {
  message: string;
  location?: string;
}

interface RuleConfig {
  [ruleName: string]: 'error' | 'warn' | 'off';
}

interface LinterConfig {
  rules?: RuleConfig;
  ignore?: string[];
}

const DEFAULT_RULES: RuleConfig = {
  'require-port': 'error',
  'valid-database-host': 'warn',
};

async function loadConfig(filePath: string): Promise<LinterConfig> {
  try {
    const fileContent = await fs.readFile(filePath, 'utf-8');
    if (filePath.endsWith('.json')) {
      return JSON.parse(fileContent);
    } else if (filePath.endsWith('.yaml') || filePath.endsWith('.yml')) {
      return yaml.load(fileContent) as LinterConfig;
    }
  } catch (error) {
    console.warn(`Could not load or parse config file ${filePath}:`, error);
  }
  return {};
}

function applyRules(config: any, rules: RuleConfig, filePath: string): LintError[] {
  const errors: LintError[] = [];

  // Rule: require-port
  if (rules['require-port'] !== 'off') {
    if (typeof config.port === 'undefined') {
      const error: LintError = { message: 'Configuration must include a "port" property.' };
      if (rules['require-port'] === 'error') {
        errors.push(error);
      } else {
        console.warn(`[WARN] ${error.message} in ${filePath}`);
      }
    }
  }

  // Rule: valid-database-host
  if (rules['valid-database-host'] !== 'off') {
    if (config.database && config.database.host) {
      if (config.database.host === 'localhost' || config.database.host === '127.0.0.1') {
        // This is a valid local host, no error/warning needed.
      } else {
        const error: LintError = { message: `Database host "${config.database.host}" is not a local address.`, location: 'database.host' };
        if (rules['valid-database-host'] === 'error') {
          errors.push(error);
        } else {
          console.warn(`[WARN] ${error.message} in ${filePath}`);
        }
      }
    }
  }

  // Add more rules here...

  return errors;
}

export async function lintConfig(configContent: string, filePath: string): Promise<LintError[]> {
  let config: any;
  try {
    if (filePath.endsWith('.json')) {
      config = JSON.parse(configContent);
    } else if (filePath.endsWith('.yaml') || filePath.endsWith('.yml')) {
      config = yaml.load(configContent);
    } else {
      throw new Error(`Unsupported file type: ${filePath}`);
    }
  } catch (error: any) {
    return [{ message: `Failed to parse configuration: ${error.message}` }];
  }

  const linterConfigPath = path.join(process.cwd(), '.ts-config-linterrc.json');
  let userConfig: LinterConfig = {};
  try {
    const linterConfigFile = await fs.readFile(linterConfigPath, 'utf-8');
    userConfig = JSON.parse(linterConfigFile);
  } catch (error) {
    // Ignore if no user config file is found
  }

  const effectiveRules = { ...DEFAULT_RULES, ...userConfig.rules };

  // TODO: Implement ignore logic based on userConfig.ignore

  return applyRules(config, effectiveRules, filePath);
}

export async function lintFile(filePath: string): Promise<LintError[]> {
  try {
    const fileContent = await fs.readFile(filePath, 'utf-8');
    return lintConfig(fileContent, filePath);
  } catch (error: any) {
    return [{ message: `Failed to read file: ${error.message}` }];
  }
}

// Example of how to use it as a CLI tool
async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: nightly-ts-config-linter --file <path-to-config>');
    process.exit(1);
  }

  let filePath = '';
  if (args[0] === '--file' && args[1]) {
    filePath = args[1];
  } else {
    console.error('Usage: nightly-ts-config-linter --file <path-to-config>');
    process.exit(1);
  }

  const errors = await lintFile(filePath);

  if (errors.length > 0) {
    console.error(`Linting errors found in ${filePath}:`);
    errors.forEach(err => {
      console.error(`- ${err.message}${err.location ? ` (at ${err.location})` : ''}`);
    });
    process.exit(1);
  } else {
    console.log(`Configuration file ${filePath} is valid.`);
  }
}

if (require.main === module) {
  main();
}
