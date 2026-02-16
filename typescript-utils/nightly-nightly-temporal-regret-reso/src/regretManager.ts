import { readFileSync, writeFileSync, existsSync } from 'fs';
import { v4 as uuidv4 } from 'uuid';
import { Regret, RegretData } from './types';

export class RegretManager {
  private filePath: string;
  private data: RegretData;

  constructor(filePath: string) {
    this.filePath = filePath;
    this.data = this._loadData();
  }

  /**
   * Adds a new temporal echo (regret) to the active list.
   * @param description The description of the regret.
   * @returns The newly created Regret object.
   */
  addRegret(description: string): Regret {
    const newRegret: Regret = {
      id: uuidv4(),
      description,
      timestamp: new Date().toISOString(),
    };
    this.data.active.push(newRegret);
    this._saveData();
    return newRegret;
  }

  /**
   * Retrieves all active (unresolved) temporal echoes.
   * @returns An array of active Regret objects.
   */
  listActiveRegrets(): Regret[] {
    return [...this.data.active];
  }

  /**
   * Retrieves all resolved temporal echoes.
   * @returns An array of resolved Regret objects.
   */
  listResolvedRegrets(): Regret[] {
    return [...this.data.resolved];
  }

  /**
   * Resolves a temporal echo by its ID, moving it from active to resolved.
   * @param id The ID of the regret to resolve.
   * @returns The resolved Regret object, or undefined if not found.
   */
  resolveRegret(id: string): Regret | undefined {
    const index = this.data.active.findIndex(r => r.id === id);
    if (index === -1) {
      return undefined;
    }

    const [resolvedRegret] = this.data.active.splice(index, 1);
    resolvedRegret.resolvedAt = new Date().toISOString();
    this.data.resolved.push(resolvedRegret);
    this._saveData();
    return resolvedRegret;
  }

  /**
   * Clears all data (for testing or fresh start).
   * # Mock rationale: This method is primarily for testing setup/teardown
   * # and allows tests to start with a clean slate without affecting real data.
   */
  _clearData(): void {
    this.data = { active: [], resolved: [] };
    this._saveData();
  }

  private _loadData(): RegretData {
    if (existsSync(this.filePath)) {
      try {
        const fileContent = readFileSync(this.filePath, 'utf8');
        return JSON.parse(fileContent) as RegretData;
      } catch (error) {
        console.error(`Error reading or parsing data file: ${this.filePath}`, error);
        return { active: [], resolved: [] };
      }
    }
    return { active: [], resolved: [] };
  }

  private _saveData(): void {
    try {
      writeFileSync(this.filePath, JSON.stringify(this.data, null, 2), 'utf8');
    } catch (error) {
      console.error(`Error writing data file: ${this.filePath}`, error);
    }
  }
}
