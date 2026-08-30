import { NutrientNoodleNegotiator } from './negotiator';
import { DEFAULT_PASTES } from './data';
import { ConsumptionRecord } from './types';
import * as fs from 'fs';
import * as path from 'path';

const RECORD_FILE = path.join(process.cwd(), '.nutrient_noodle_record.json');

/**
 * Loads the consumption record from a JSON file.
 * If the file doesn't exist or is invalid, returns a fresh record.
 * @returns The loaded or a new ConsumptionRecord.
 */
function loadRecord(): ConsumptionRecord {
  try {
    if (fs.existsSync(RECORD_FILE)) {
      const data = fs.readFileSync(RECORD_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error("Error loading consumption record, starting fresh:", error);
  }
  return { lastConsumedId: null, history: [] };
}

/**
 * Saves the consumption record to a JSON file.
 * @param record The ConsumptionRecord to save.
 */
function saveRecord(record: ConsumptionRecord): void {
  try {
    fs.writeFileSync(RECORD_FILE, JSON.stringify(record, null, 2), 'utf8');
  } catch (error) {
    console.error("Error saving consumption record:", error);
  }
}

/**
 * Main function to run the CLI utility.
 * Parses arguments, gets a suggestion, and updates the record.
 */
function main() {
  const args = process.argv.slice(2);
  const moodIndex = args.indexOf('--mood');
  let moodTag: string | undefined;

  if (moodIndex !== -1 && args[moodIndex + 1]) {
    moodTag = args[moodIndex + 1].toLowerCase();
  }

  const currentRecord = loadRecord();
  const negotiator = new NutrientNoodleNegotiator(DEFAULT_PASTES, currentRecord);
  const { suggestion, record: updatedRecord } = negotiator.suggestNext(moodTag);

  console.log(`\n🍜 Your next nutrient paste suggestion: ${suggestion.name}`);
  if (moodTag) {
    console.log(`(Influenced by your '${moodTag}' mood)`);
  }
  console.log(`Tags: ${suggestion.tags.join(', ')}\n`);

  saveRecord(updatedRecord);
}

main();
