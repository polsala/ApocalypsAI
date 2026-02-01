import * as fs from 'node:fs';
import * => path from 'node:path';
import { v4 as uuidv4 } from 'uuid';
import { TemporalEcho, ReframedEcho, EchoData, EchoStatus } from './types';

const DATA_DIR = path.join(__dirname, '..', 'data');
const ECHOES_FILE = path.join(DATA_DIR, 'echoes.json');

// Ensure data directory exists on initialization
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

export class EchoManager {
  private echoes: EchoData[] = [];

  constructor() {
    this.loadEchoes();
  }

  private loadEchoes(): void {
    try {
      if (fs.existsSync(ECHOES_FILE)) {
        const data = fs.readFileSync(ECHOES_FILE, 'utf8');
        this.echoes = JSON.parse(data) as EchoData[];
      } else {
        this.echoes = [];
      }
    } catch (error) {
      console.error('Failed to load echoes:', error);
      this.echoes = [];
    }
  }

  private saveEchoes(): void {
    try {
      fs.writeFileSync(ECHOES_FILE, JSON.stringify(this.echoes, null, 2), 'utf8');
    } catch (error) {
      console.error('Failed to save echoes:', error);
    }
  }

  public logEcho(description: string, impact: string): TemporalEcho {
    const newEcho: TemporalEcho = {
      id: uuidv4(),
      timestamp: new Date().toISOString(),
      description,
      impact,
      status: 'raw'
    };
    this.echoes.push(newEcho);
    this.saveEchoes();
    return newEcho;
  }

  public reframeEcho(id: string, lesson: string, action: string): ReframedEcho | null {
    const index = this.echoes.findIndex(echo => echo.id === id && echo.status === 'raw');
    if (index === -1) {
      return null; // Echo not found or already reframed
    }

    const originalEcho = this.echoes[index] as TemporalEcho;
    const reframedEcho: ReframedEcho = {
      ...originalEcho,
      status: 'reframed',
      reframedTimestamp: new Date().toISOString(),
      lesson,
      action
    };

    this.echoes[index] = reframedEcho;
    this.saveEchoes();
    return reframedEcho;
  }

  public listEchoes(statusFilter?: EchoStatus): EchoData[] {
    if (statusFilter) {
      return this.echoes.filter(echo => echo.status === statusFilter);
    }
    return [...this.echoes]; // Return a copy to prevent external modification
  }

  // For testing purposes, to reset internal state without file interaction
  public _resetEchoes(initialEchoes: EchoData[] = []): void {
    this.echoes = initialEchoes;
    this.saveEchoes(); // Ensure the mocked save is called for consistency in tests
  }
}
