import EventEmitter from 'events';
import fetch from 'node-fetch'; // Assuming a Node.js environment for fetch

interface BeaconResponse {
  timestamp: number;
}

interface TemporalSyncBeaconEvents {
  on(event: 'synced', listener: (offsetMs: number) => void): this;
  on(event: 'error', listener: (error: Error) => void): this;
}

export class TemporalSyncBeacon extends EventEmitter implements TemporalSyncBeaconEvents {
  private beaconUrl: string;
  private syncInterval: number;
  private timerId: NodeJS.Timeout | null = null;
  private currentOffsetMs: number = 0;

  constructor(beaconUrl: string, syncInterval: number = 60000) { // Default to 1 minute
    super();
    this.beaconUrl = beaconUrl;
    this.syncInterval = syncInterval;
  }

  /**
   * Starts the temporal synchronization process.
   */
  public async start(): Promise<void> {
    if (this.timerId) {
      console.warn('Synchronization is already running.');
      return;
    }
    await this.synchronize(); // Perform an initial sync immediately
    this.timerId = setInterval(() => {
      this.synchronize().catch(err => {
        this.emit('error', new Error(`Failed during interval sync: ${err.message}`));
      });
    }, this.syncInterval);
  }

  /**
   * Stops the temporal synchronization process.
   */
  public stop(): void {
    if (this.timerId) {
      clearInterval(this.timerId);
      this.timerId = null;
      console.log('Temporal synchronization stopped.');
    } else {
      console.warn('Synchronization is not running.');
    }
  }

  /**
   * Gets the current estimated time offset in milliseconds.
   * @returns The offset in milliseconds.
   */
  public getOffset(): number {
    return this.currentOffsetMs;
  }

  private async synchronize(): Promise<void> {
    try {
      const response = await fetch(this.beaconUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: BeaconResponse = await response.json();

      const beaconTimestamp = data.timestamp;
      const localTimestamp = Date.now();
      const offset = beaconTimestamp - localTimestamp;

      this.currentOffsetMs = offset;
      this.emit('synced', offset);

    } catch (error: any) {
      this.emit('error', error);
      // Optionally, you might want to reset offset or handle persistent errors differently
      this.currentOffsetMs = 0; // Reset offset on error to avoid propagating bad data
    }
  }
}

// Example CLI execution (if run directly)
if (require.main === module) {
  const args = process.argv.slice(2);
  let beaconUrl = 'http://localhost:3000/mock-beacon'; // Default mock beacon
  let interval = 60000;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--beacon-url' && args[i+1]) {
      beaconUrl = args[i+1];
      i++;
    } else if (args[i] === '--interval' && args[i+1]) {
      interval = parseInt(args[i+1], 10);
      if (isNaN(interval)) {
        console.error('Invalid interval value. Please provide a number.');
        process.exit(1);
      }
      i++;
    }
  }

  // Mock server for CLI example if no URL is provided
  if (beaconUrl === 'http://localhost:3000/mock-beacon') {
    const http = require('http');
    const mockServer = http.createServer((req, res) => {
      if (req.url === '/mock-beacon') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ timestamp: Date.now() }));
      } else {
        res.writeHead(404);
        res.end();
      }
    });
    mockServer.listen(3000, () => {
      console.log('Mock temporal beacon running on http://localhost:3000/mock-beacon');
    });
    // Ensure mock server is cleaned up on exit
    process.on('exit', () => mockServer.close());
  }

  const beacon = new TemporalSyncBeacon(beaconUrl, interval);

  beacon.on('synced', (offsetMs: number) => {
    console.log(`[${new Date().toISOString()}] Time synchronized. Offset: ${offsetMs}ms`);
  });

  beacon.on('error', (err: Error) => {
    console.error(`[${new Date().toISOString()}] Synchronization error: ${err.message}`);
  });

  console.log(`Starting temporal synchronization with beacon: ${beaconUrl} every ${interval}ms`);
  beacon.start().catch(console.error);

  // Keep the process alive for the interval timer
  process.stdin.resume();
}
