import { promises as fs } from 'node:fs';
import { v4 as uuidv4 } from 'uuid';
import { ScavengedItem, ItemCondition, ManifestData } from './types';

const MANIFEST_FILE = 'manifest.json';

export class ScavengerManifest {
  private data: ManifestData = { items: [] };

  constructor() {
    this.loadManifest();
  }

  private async loadManifest(): Promise<void> {
    try {
      const fileContent = await fs.readFile(MANIFEST_FILE, 'utf-8');
      this.data = JSON.parse(fileContent) as ManifestData;
    } catch (error: any) {
      if (error.code === 'ENOENT') {
        // Manifest file does not exist, initialize with empty data
        this.data = { items: [] };
        await this.saveManifest(); // Create the file
      } else {
        console.error(`Error loading manifest: ${error.message}`);
        this.data = { items: [] }; // Fallback to empty data on other errors
      }
    }
  }

  private async saveManifest(): Promise<void> {
    try {
      await fs.writeFile(MANIFEST_FILE, JSON.stringify(this.data, null, 2), 'utf-8');
    } catch (error: any) {
      console.error(`Error saving manifest: ${error.message}`);
    }
  }

  public async addItem(name: string, category: string, condition: ItemCondition, quantity: number, notes?: string): Promise<ScavengedItem> {
    const newItem: ScavengedItem = {
      id: uuidv4(),
      name,
      category,
      condition,
      quantity,
      notes,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    this.data.items.push(newItem);
    await this.saveManifest();
    return newItem;
  }

  public async listItems(): Promise<ScavengedItem[]> {
    await this.loadManifest(); // Ensure latest data is loaded
    return this.data.items;
  }

  public async updateItem(id: string, updates: Partial<Omit<ScavengedItem, 'id' | 'createdAt'>>): Promise<ScavengedItem | null> {
    const itemIndex = this.data.items.findIndex(item => item.id === id);
    if (itemIndex === -1) {
      return null;
    }

    this.data.items[itemIndex] = {
      ...this.data.items[itemIndex],
      ...updates,
      updatedAt: new Date().toISOString(),
    };
    await this.saveManifest();
    return this.data.items[itemIndex];
  }

  public async removeItem(id: string): Promise<boolean> {
    const initialLength = this.data.items.length;
    this.data.items = this.data.items.filter(item => item.id !== id);
    if (this.data.items.length < initialLength) {
      await this.saveManifest();
      return true;
    }
    return false;
  }

  public async searchItems(query: string, field?: keyof ScavengedItem): Promise<ScavengedItem[]> {
    await this.loadManifest();
    const lowerQuery = query.toLowerCase();

    return this.data.items.filter(item => {
      if (field) {
        const value = item[field];
        return typeof value === 'string' && value.toLowerCase().includes(lowerQuery);
      } else {
        // Search across name, category, condition, and notes by default
        return (
          item.name.toLowerCase().includes(lowerQuery) ||
          item.category.toLowerCase().includes(lowerQuery) ||
          item.condition.toLowerCase().includes(lowerQuery) ||
          (item.notes && item.notes.toLowerCase().includes(lowerQuery))
        );
      }
    });
  }
}
