import axios from 'axios';
import { EventEmitter } from 'events';

interface BeaconResponse {
  timestamp: number;
}

export class TemporalSyncBeacon extends EventEmitter {
  private beaconUrl: string;
  private intervalSeconds: number;
  private timerId: NodeJS.Timeout | null = null;
  private isRunning: boolean = false;

  constructor(beaconUrl: string, intervalSeconds: number = 300) {
    super();
    if (!beaconUrl) {
      throw new Error('Beacon URL is required.');
    }
    this.beaconUrl = beaconUrl;
    this.intervalSeconds = intervalSeconds;
  }

  /**
   * Starts the temporal synchronization process.
   */
  public async start(): Promise<void> {
    if (this.isRunning) {
      console.warn('TemporalSyncBeacon is already running.');
      return;
    }
    this.isRunning = true;
    await this.syncTime(); // Perform an initial sync immediately
    this.timerId = setInterval(() => {
      this.syncTime().catch(err => {
        console.error('Error during interval sync:', err);
        this.emit('error', new Error('Interval sync failed'));
      });
    }, this.intervalSeconds * 1000);
    console.log(`TemporalSyncBeacon started. Syncing every ${this.intervalSeconds} seconds from ${this.beaconUrl}`);
  }

  /**
   * Stops the temporal synchronization process.
   */
  public stop(): void {
    if (this.timerId) {
      clearInterval(this.timerId);
      this.timerId = null;
      this.isRunning = false;
      console.log('TemporalSyncBeacon stopped.');
    }
  }

  /**
   * Synchronizes the local time with the temporal beacon.
   */
  private async syncTime(): Promise<void> {
    try {
      const response = await axios.get<BeaconResponse>(this.beaconUrl);
      if (typeof response.data.timestamp !== 'number') {
        throw new Error('Invalid timestamp format received from beacon.');
      }
      const beaconTime = new Date(response.data.timestamp);
      const currentTime = new Date();

      // For simplicity, we'll just emit the beacon's time.
      // In a more complex scenario, you might adjust the system clock or store an offset.
      this.emit('synced', beaconTime);

    } catch (error: any) {
      const errorMessage = error.response ? `${error.response.status} - ${error.response.data}` : error.message;
      console.error(`Failed to sync time from ${this.beaconUrl}: ${errorMessage}`);
      this.emit('error', new Error(`Failed to sync time: ${errorMessage}`));
      throw error; // Re-throw to be caught by setInterval error handler
    }
  }
}

// CLI execution logic
if (require.main === module) {
  const args = process.argv.slice(2);
  const beaconUrlIndex = args.indexOf('--beacon-url');
  const intervalIndex = args.indexOf('--interval');

  if (beaconUrlIndex === -1) {
    console.error('Error: --beacon-url is a required argument.');
    console.log('Usage: ts-node src/main.ts --beacon-url <beacon_server_url> [--interval <seconds>]');
    process.exit(1);
  }

  const beaconUrl = args[beaconUrlIndex + 1];
  const interval = intervalIndex !== -1 ? parseInt(args[intervalIndex + 1], 10) : 300;

  if (isNaN(interval) || interval <= 0) {
    console.error('Error: --interval must be a positive number.');
    process.exit(1);
  }

  const beacon = new TemporalSyncBeacon(beaconUrl, interval);

  beacon.on('synced', (newTime: Date) => {
    console.log(`[${newTime.toISOString()}] Time synchronized.`);
  });

  beacon.on('error', (err: Error) => {
    console.error(`[${new Date().toISOString()}] Synchronization Error: ${err.message}`);
  });

  beacon.start().catch(err => {
    console.error(`Failed to start TemporalSyncBeacon: ${err.message}`);
    process.exit(1);
  });

  // Keep the process alive
  process.stdin.resume();
}
