import { DigitalItem, Scarcity, Utility } from './types';
import { v4 as uuidv4 } from 'uuid';
import * as fs from 'fs';
import * as path from 'path';

export class HoardManager {
  private hoard: DigitalItem[] = [];
  private dataFilePath: string;

  constructor(dataDir: string) {
    // Ensure the data directory exists
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
    }
    this.dataFilePath = path.join(dataDir, 'hoard.json');
    this.loadHoard();
  }

  private loadHoard(): void {
    if (fs.existsSync(this.dataFilePath)) {
      try {
        const data = fs.readFileSync(this.dataFilePath, 'utf8');
        this.hoard = JSON.parse(data);
      } catch (error) {
        console.error('Failed to load hoard data:', error);
        this.hoard = []; // Start fresh if data is corrupted
      }
    } else {
      this.hoard = [];
    }
  }

  private saveHoard(): void {
    try {
      fs.writeFileSync(this.dataFilePath, JSON.stringify(this.hoard, null, 2), 'utf8');
    } catch (error) {
      console.error('Failed to save hoard data:', error);
    }
  }

  addItem(name: string, type: DigitalItem['type'], pathOrContent: string, scarcity: Scarcity, utility: Utility): DigitalItem {
    const newItem: DigitalItem = {
      id: uuidv4(),
      name,
      type,
      pathOrContent,
      scarcity,
      utility,
      addedAt: new Date().toISOString(),
    };
    this.hoard.push(newItem);
    this.saveHoard();
    return newItem;
  }

  listItems(): DigitalItem[] {
    return [...this.hoard]; // Return a copy to prevent external modification
  }

  getItem(id: string): DigitalItem | undefined {
    return this.hoard.find(item => item.id === id);
  }

  deleteItem(id: string): boolean {
    const initialLength = this.hoard.length;
    this.hoard = this.hoard.filter(item => item.id !== id);
    if (this.hoard.length < initialLength) {
      this.saveHoard();
      return true;
    }
    return false;
  }

  generateCurationReport(): string[] {
    const report: string[] = ['--- Digital Hoard Curation Report ---'];

    const scarcityOrder: Scarcity[] = ['legendary', 'rare', 'uncommon', 'common'];
    const utilityOrder: Utility[] = ['essential', 'useful', 'archive', 'ephemeral'];

    // Sort items for consistent reporting
    const sortedHoard = [...this.hoard].sort((a, b) => {
      const scarcityDiff = scarcityOrder.indexOf(a.scarcity) - scarcityOrder.indexOf(b.scarcity);
      if (scarcityDiff !== 0) return scarcityDiff;
      const utilityDiff = utilityOrder.indexOf(a.utility) - utilityOrder.indexOf(b.utility);
      if (utilityDiff !== 0) return utilityDiff;
      return a.name.localeCompare(b.name);
    });

    report.push('\nLegendary & Essential Items (PRIORITY BACKUP!):');
    sortedHoard.filter(item => item.scarcity === 'legendary' && item.utility === 'essential')
      .forEach(item => report.push(`  - [${item.id.substring(0, 8)}] ${item.name} (${item.type})`));

    report.push('\nRare & Useful Items (Consider Backup):');
    sortedHoard.filter(item => item.scarcity === 'rare' && item.utility === 'useful')
      .forEach(item => report.push(`  - [${item.id.substring(0, 8)}] ${item.name} (${item.type})`));

    report.push('\nEphemeral Items (Review for Deletion):');
    sortedHoard.filter(item => item.utility === 'ephemeral')
      .forEach(item => report.push(`  - [${item.id.substring(0, 8)}] ${item.name} (${item.type})`));

    report.push('\nArchive Items (Verify Redundancy):');
    sortedHoard.filter(item => item.utility === 'archive')
      .forEach(item => report.push(`  - [${item.id.substring(0, 8)}] ${item.name} (${item.type})`));

    if (this.hoard.length === 0) {
      report.push('\nYour hoard is empty. Time to scavenge!');
    }

    report.push('\n--- End Report ---');
    return report;
  }
}
