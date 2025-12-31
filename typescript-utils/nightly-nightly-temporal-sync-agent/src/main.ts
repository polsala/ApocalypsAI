import { createClient } from 'ntp-client';

interface NtpConfig {
  server: string;
  updateIntervalMs: number;
}

const defaultConfig: NtpConfig = {
  server: 'pool.ntp.org',
  updateIntervalMs: 60 * 60 * 1000, // 1 hour
};

async function syncTime(config: NtpConfig): Promise<void> {
  console.log(`Attempting to sync time with NTP server: ${config.server}`);
  try {
    const client = createClient(config.server);

    client.on('error', (err) => {
      console.error(`NTP client error: ${err.message}`);
    });

    client.on('message', (msg) => {
      if (msg.txTimestamp) {
        const ntpTime = new Date(msg.txTimestamp * 1000);
        console.log(`NTP server time: ${ntpTime.toISOString()}`);
        // In a real-world scenario, you would use OS-level commands to set the system time.
        // For this simulation, we'll just log it.
        console.log('System time synchronization simulated successfully.');
      }
    });

    client.query();
  } catch (error) {
    console.error(`Failed to create NTP client or query: ${(error as Error).message}`);
  }
}

function startSyncAgent(): void {
  const ntpServer = process.env.NTP_SERVER || defaultConfig.server;
  const updateInterval = parseInt(process.env.UPDATE_INTERVAL_MS || String(defaultConfig.updateIntervalMs), 10);

  if (isNaN(updateInterval) || updateInterval <= 0) {
    console.error('Invalid UPDATE_INTERVAL_MS. Using default.');
    setTimeout(() => startSyncAgent(), defaultConfig.updateIntervalMs);
    return;
  }

  const config: NtpConfig = {
    server: ntpServer,
    updateIntervalMs: updateInterval,
  };

  console.log(`Temporal Sync Agent started. Updating every ${config.updateIntervalMs / 1000 / 60} minutes.`);
  syncTime(config);

  setInterval(() => {
    syncTime(config);
  }, config.updateIntervalMs);
}

// Mock rationale: The 'ntp-client' library is an external dependency that would require network access. 
// For deterministic offline testing, we will mock its behavior.
// In a real execution environment, this would be replaced by the actual library.

// Mocking the ntp-client library for testing purposes
if (process.env.NODE_ENV === 'test') {
  jest.mock('ntp-client', () => ({
    createClient: jest.fn(() => ({
      on: jest.fn((event: string, handler: (...args: any[]) => void) => {
        if (event === 'message') {
          // Simulate a successful time response
          handler({
            txTimestamp: Date.now() / 1000, // Current time in seconds
            refTimestamp: 0,
            origTimestamp: 0,
            recvTimestamp: 0,
            leap: 0,
            precision: 0,
            stratum: 0,
            poll: 0,
            rtt: 0,
            dispersion: 0,
            rootDelay: 0,
            rootDispersion: 0,
            kissCode: 0,
            ntpData: Buffer.from([]),
          });
        } else if (event === 'error') {
          // Simulate an error if needed for specific test cases
          // handler(new Error('Mocked NTP error'));
        }
      }),
      query: jest.fn(),
    })),
  }));
}

startSyncAgent();
