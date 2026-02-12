import * as fs from 'fs';
import * as path from 'path';
import { MoraleData, MoraleEntry } from './types';

const DATA_FILE = path.join(process.cwd(), 'morale.json');

export function loadMoraleData(): MoraleData {
  if (fs.existsSync(DATA_FILE)) {
    const rawData = fs.readFileSync(DATA_FILE, 'utf8');
    try {
      return JSON.parse(rawData) as MoraleData;
    } catch (e) {
      console.error("Error parsing morale.json, starting fresh.", e);
      return { entries: [] };
    }
  }
  return { entries: [] };
}

export function saveMoraleData(data: MoraleData): void {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf8');
}

export function addEntry(entry: MoraleEntry): void {
  const data = loadMoraleData();
  data.entries.push(entry);
  saveMoraleData(data);
}

export function clearEntries(): void {
  saveMoraleData({ entries: [] });
}
