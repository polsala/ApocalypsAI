#!/usr/bin/env node
import { readFileSync } from 'fs';
import { ChronalFragmentHarmonizer } from './harmonizer';
import { DataFragment } from './types';

function displayHelp() {
  console.log(`
Usage: harmonize-fragments <input-file.json>

A TypeScript CLI tool to sort and categorize temporal data fragments based on distortion and timestamp, generating a harmonization report.

Arguments:
  <input-file.json>  Path to a JSON file containing an array of DataFragment objects.

Example:
  harmonize-fragments ./fragments.json
  `);
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    displayHelp();
    process.exit(0);
  }

  const inputFilePath = args[0];

  try {
    const fileContent = readFileSync(inputFilePath, 'utf8');
    const fragments: DataFragment[] = JSON.parse(fileContent);

    const harmonizer = new ChronalFragmentHarmonizer(fragments);
    const report = harmonizer.generateReport();
    console.log(harmonizer.formatReport(report));

  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main();
