import * as fs from 'fs';
import * as path from 'path';
import { v4 as uuidv4 } from 'uuid';
import { RealityRipple, RippleType } from './types';

const DATA_DIR = path.join(__dirname, '..', '.data');
const DATA_FILE_PATH = path.join(DATA_DIR, 'ripples.json');

export class RippleManager {
  private async ensureDataDirectory(): Promise<void> {
    if (!fs.existsSync(DATA_DIR)) {
      await fs.promises.mkdir(DATA_DIR, { recursive: true });
    }
  }

  public async loadRipples(): Promise<RealityRipple[]> {
    try {
      if (!fs.existsSync(DATA_FILE_PATH)) {
        return [];
      }
      const data = await fs.promises.readFile(DATA_FILE_PATH, 'utf8');
      return JSON.parse(data) as RealityRipple[];
    } catch (error) {
      console.error(`Error loading ripples: ${error instanceof Error ? error.message : String(error)}`);
      return [];
    }
  }

  public async saveRipples(ripples: RealityRipple[]): Promise<void> {
    try {
      await this.ensureDataDirectory();
      const data = JSON.stringify(ripples, null, 2);
      await fs.promises.writeFile(DATA_FILE_PATH, data, 'utf8');
    } catch (error) {
      console.error(`Error saving ripples: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  public async addRipple(type: RippleType, description: string): Promise<RealityRipple> {
    const ripples = await this.loadRipples();
    const newRipple: RealityRipple = {
      id: uuidv4(),
      type,
      description,
      timestamp: new Date().toISOString(),
    };
    ripples.push(newRipple);
    await this.saveRipples(ripples);
    return newRipple;
  }

  public async listRipples(): Promise<RealityRipple[]> {
    return this.loadRipples();
  }

  public async filterRipples(type: RippleType): Promise<RealityRipple[]> {
    const ripples = await this.loadRipples();
    return ripples.filter(ripple => ripple.type === type);
  }
}
