#!/usr/bin/env node

import { DataDicer, DataItem } from './index';
import * as fs from 'fs';
import * as path from 'path';

function parseArgs(args: string[]) {
  const options: {
    file?: string;
    filter?: string;
    sample?: number;
    pick?: string[];
    omit?: string[];
    sort?: string;
    sortDesc?: boolean;
    seed?: number;
    help?: boolean;
  } = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '-f':
      case '--file':
        options.file = args[++i];
        break;
      case '--filter':
        options.filter = args[++i];
        break;
      case '-s':
      case '--sample':
        options.sample = parseInt(args[++i], 10);
        break;
      case '--seed':
        options.seed = parseInt(args[++i], 10);
        break;
      case '-p':
      case '--pick':
        options.pick = args[++i].split(',');
        break;
      case '-o':
      case '--omit':
        options.omit = args[++i].split(',');
        break;
      case '--sort':
        options.sort = args[++i];
        break;
      case '--sort-desc':
        options.sortDesc = true;
        break;
      case '-h':
      case '--help':
        options.help = true;
        break;
      default:
        if (arg.startsWith('-')) {
          console.error(`Error: Unknown option: ${arg}\n`);
          options.help = true; // Show help on unknown option
        }
        break;
    }
  }
  return options;
}

function showHelpAndExit() {
  console.log(`
Usage: nightly-data-dicer [options]

A type-safe TypeScript utility to slice and dice structured data.

Options:
  -f, --file <path>       Input JSON file path. If not provided, reads from stdin.
  --filter <key=value>    Filter data where item[key] equals value. Supports basic string/number equality.
  -s, --sample <count>    Randomly sample N items.
  --seed <number>         Seed for deterministic sampling.
  -p, --pick <keys>       Comma-separated list of keys to pick (e.g., "name,age").
  -o, --omit <keys>       Comma-separated list of keys to omit (e.g., "id,password").
  --sort <key>            Sort data by a specific key.
  --sort-desc             Sort in descending order (requires --sort).
  -h, --help              Display this help message.
  `);
  process.exit(0);
}

async function run() {
  const options = parseArgs(process.argv.slice(2));

  if (options.help) {
    showHelpAndExit();
  }

  let rawData: string;
  try {
    if (options.file) {
      rawData = fs.readFileSync(options.file, 'utf8');
    } else {
      // Read from stdin only if not a TTY or if data is explicitly piped
      if (process.stdin.isTTY) {
        console.error("Error: No input data. Use --file <path> or pipe JSON to stdin.\n");
        showHelpAndExit();
        return; // Should not be reached due to process.exit
      }
      rawData = await new Promise<string>((resolve, reject) => {
        let data = '';
        process.stdin.on('data', chunk => data += chunk);
        process.stdin.on('end', () => resolve(data));
        process.stdin.on('error', (err) => reject(err));
      });
    }
  } catch (error: any) {
    console.error(`Error reading input data: ${error.message}\n`);
    process.exit(1);
  }

  let inputData: DataItem[];
  try {
    inputData = JSON.parse(rawData);
    if (!Array.isArray(inputData)) {
      throw new Error("Input JSON must be an array of objects.");
    }
  } catch (error: any) {
    console.error(`Error parsing input JSON: ${error.message}\n`);
    process.exit(1);
  }

  let dicer = new DataDicer(inputData);

  if (options.filter) {
    const parts = options.filter.split('=');
    if (parts.length < 2) {
      console.error("Error: Invalid filter format. Use --filter 'key=value'.\n");
      showHelpAndExit();
    }
    const key = parts[0];
    const value = parts.slice(1).join('='); // Handle values with '=' signs
    dicer = dicer.filter(item => String(item[key]) === value);
  }

  if (options.sort) {
    dicer = dicer.sort(options.sort, !options.sortDesc);
  }

  if (options.pick) {
    dicer = dicer.pick(options.pick);
  }

  if (options.omit) {
    dicer = dicer.omit(options.omit);
  }

  if (options.sample !== undefined) {
    dicer = dicer.sample(options.sample, options.seed);
  }

  const result = dicer.execute();
  console.log(JSON.stringify(result, null, 2));
}

if (require.main === module) {
  run();
}
