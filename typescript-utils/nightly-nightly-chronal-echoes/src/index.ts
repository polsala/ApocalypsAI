import { promises as fs } from 'fs';
import path from 'path';

interface ChronalEcho {
  id: string;
  message: string;
  timestamp: Date;
}

export class ChronalEchoesManager {
  private filePath: string;
  private echoes: ChronalEcho[] = [];

  constructor(fileName: string = '.chronal-echoes.json') {
    this.filePath = path.resolve(process.cwd(), fileName);
  }

  public async init(): Promise<void> {
    await this.loadEchoes();
  }

  public async scheduleEcho(message: string, futureDate: Date): Promise<ChronalEcho> {
    if (futureDate.getTime() <= new Date().getTime()) {
      throw new Error("Future date must be in the future.");
    }
    const newEcho: ChronalEcho = {
      id: Date.now().toString() + Math.random().toString(36).substring(2, 9),
      message,
      timestamp: futureDate,
    };
    this.echoes.push(newEcho);
    await this.saveEchoes();
    return newEcho;
  }

  public async retrieveEchoes(currentTime: Date = new Date()): Promise<ChronalEcho[]> {
    const triggeredEchoes: ChronalEcho[] = [];
    const remainingEchoes: ChronalEcho[] = [];

    for (const echo of this.echoes) {
      if (echo.timestamp.getTime() <= currentTime.getTime()) {
        triggeredEchoes.push(echo);
      } else {
        remainingEchoes.push(echo);
      }
    }

    this.echoes = remainingEchoes;
    if (triggeredEchoes.length > 0) {
      await this.saveEchoes();
    }
    return triggeredEchoes;
  }

  public async clearAllEchoes(): Promise<void> {
    this.echoes = [];
    await this.saveEchoes();
  }

  private async saveEchoes(): Promise<void> {
    const serializableEchoes = this.echoes.map(echo => ({
      ...echo,
      timestamp: echo.timestamp.toISOString(), // Convert Date to ISO string for serialization
    }));
    await fs.writeFile(this.filePath, JSON.stringify(serializableEchoes, null, 2), 'utf8');
  }

  private async loadEchoes(): Promise<void> {
    try {
      const data = await fs.readFile(this.filePath, 'utf8');
      const serializableEchoes: Omit<ChronalEcho, 'timestamp'> & { timestamp: string }[] = JSON.parse(data);
      this.echoes = serializableEchoes.map(echo => ({
        ...echo,
        timestamp: new Date(echo.timestamp), // Convert ISO string back to Date
      }));
    } catch (error: any) {
      if (error.code === 'ENOENT') {
        this.echoes = []; // File not found, start with empty echoes
      } else {
        console.error(`Error loading chronal echoes: ${error.message}`);
        this.echoes = []; // Fallback to empty on other errors or invalid JSON
      }
    }
  }
}

// CLI entry point
if (require.main === module) {
  const manager = new ChronalEchoesManager();
  manager.init().then(async () => {
    const args = process.argv.slice(2);
    const command = args[0];

    switch (command) {
      case 'schedule':
        const message = args[1];
        const dateString = args[2];
        if (!message || !dateString) {
          console.error('Usage: chronal-echoes schedule "<message>" "<YYYY-MM-DDTHH:MM:SSZ>"');
          process.exit(1);
        }
        try {
          const futureDate = new Date(dateString);
          if (isNaN(futureDate.getTime())) {
            throw new Error('Invalid date format. Use ISO 8601 (e.g., "2025-01-01T10:00:00Z").');
          }
          const echo = await manager.scheduleEcho(message, futureDate);
          console.log(`Echo scheduled: "${echo.message}" for ${echo.timestamp.toISOString()}`);
        } catch (error: any) {
          console.error(`Failed to schedule echo: ${error.message}`);
          process.exit(1);
        }
        break;

      case 'retrieve':
        const retrieved = await manager.retrieveEchoes();
        if (retrieved.length > 0) {
          console.log('Chronal Echoes manifested:');
          retrieved.forEach(echo => {
            console.log(`- [${echo.timestamp.toISOString()}] ${echo.message} (ID: ${echo.id})`);
          });
        } else {
          console.log('No chronal echoes have manifested yet.');
        }
        break;

      case 'clear':
        await manager.clearAllEchoes();
        console.log('All chronal echoes cleared from the timeline.');
        break;

      default:
        console.log('Usage:');
        console.log('  chronal-echoes schedule "<message>" "<YYYY-MM-DDTHH:MM:SSZ>"');
        console.log('  chronal-echoes retrieve');
        console.log('  chronal-echoes clear');
        process.exit(1);
    }
  }).catch(error => {
    console.error(`An error occurred during initialization: ${error.message}`);
    process.exit(1);
  });
}
