import { readFileSync, writeFileSync, existsSync } from 'fs';
import { v4 as uuidv4 } from 'uuid';
import { Snack } from './types';

const DATA_FILE = 'snack_stash.json';

export class SnackManager {
  private snacks: Snack[];
  private dataFilePath: string;

  constructor(dataFilePath: string = DATA_FILE) {
    this.dataFilePath = dataFilePath;
    this.snacks = this.loadData();
  }

  private loadData(): Snack[] {
    if (existsSync(this.dataFilePath)) {
      try {
        const data = readFileSync(this.dataFilePath, 'utf8');
        return JSON.parse(data) as Snack[];
      } catch (error) {
        console.error(`Error reading snack data from ${this.dataFilePath}:`, error);
        return [];
      }
    }
    return [];
  }

  private saveData(): void {
    try {
      writeFileSync(this.dataFilePath, JSON.stringify(this.snacks, null, 2), 'utf8');
    } catch (error) {
      console.error(`Error writing snack data to ${this.dataFilePath}:`, error);
    }
  }

  addSnack(name: string, quantity: number, expirationDateStr: string): Snack {
    if (quantity <= 0) {
      throw new Error('Quantity must be greater than 0.');
    }
    if (isNaN(new Date(expirationDateStr).getTime())) {
      throw new Error('Invalid expiration date format. Use YYYY-MM-DD.');
    }

    const newSnack: Snack = {
      id: uuidv4(),
      name,
      quantity,
      expirationDate: expirationDateStr,
    };
    this.snacks.push(newSnack);
    this.saveData();
    return newSnack;
  }

  listSnacks(): Snack[] {
    // Sort by expiration date, earliest first
    return [...this.snacks].sort((a, b) => {
      const dateA = new Date(a.expirationDate).getTime();
      const dateB = new Date(b.expirationDate).getTime();
      return dateA - dateB;
    });
  }

  eatSnack(id: string, quantityToEat: number): Snack | null {
    if (quantityToEat <= 0) {
      throw new Error('Quantity to eat must be greater than 0.');
    }

    const snackIndex = this.snacks.findIndex(s => s.id === id);
    if (snackIndex === -1) {
      return null; // Snack not found
    }

    const snack = this.snacks[snackIndex];
    if (snack.quantity < quantityToEat) {
      throw new Error(`Cannot eat ${quantityToEat} of ${snack.name}. Only ${snack.quantity} available.`);
    }

    snack.quantity -= quantityToEat;
    if (snack.quantity === 0) {
      this.snacks.splice(snackIndex, 1); // Remove if fully consumed
    }
    this.saveData();
    return snack;
  }

  suggestSnacks(): Snack[] {
    // Filter out expired snacks and sort by expiration date, earliest first
    const now = new Date();
    now.setHours(0, 0, 0, 0); // Compare only date part

    return [...this.snacks]
      .filter(snack => new Date(snack.expirationDate).getTime() >= now.getTime())
      .sort((a, b) => {
        const dateA = new Date(a.expirationDate).getTime();
        const dateB = new Date(b.expirationDate).getTime();
        return dateA - dateB;
      });
  }

  // For testing purposes, to clear the stash
  _clearStash(): void {
    this.snacks = [];
    this.saveData();
  }
}
