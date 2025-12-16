import axios from 'axios';
import { execSync } from 'child_process';

interface BeaconResponse {
  timestamp: number;
}

async function getTimeFromBeacon(beaconUrl: string): Promise<number> {
  try {
    const response = await axios.get<BeaconResponse>(beaconUrl);
    if (typeof response.data.timestamp !== 'number') {
      throw new Error('Invalid timestamp format from beacon.');
    }
    return response.data.timestamp;
  } catch (error: any) {
    console.error(`Error fetching time from beacon at ${beaconUrl}: ${error.message}`);
    throw error;
  }
}

function adjustLocalTime(offsetMs: number): void {
  if (process.platform === 'win32') {
    // Windows adjustment (requires admin privileges)
    // This is a simplified example; a robust solution would involve more complex WMI calls.
    console.warn('Windows time adjustment is complex and requires admin privileges. Attempting a basic sync command.');
    try {
      // Attempt to sync with a public NTP server
      execSync(`w32tm /resync /force`, { stdio: 'inherit' });
      console.log('Attempted to resynchronize Windows time.');
    } catch (e: any) {
      console.error(`Failed to adjust time on Windows: ${e.message}`);
    }
  } else {
    // Unix-like systems (Linux, macOS) adjustment (requires root privileges)
    console.log(`Attempting to adjust local time by ${offsetMs}ms (requires root privileges)...`);
    try {
      // Constructing the date command to set time
      // Note: This is a simplified approach. A more robust solution might use 'ntpd' or 'chrony'.
      const currentLocalTime = Date.now();
      const newLocalTime = currentLocalTime + offsetMs;
      const dateCommand = `date -s @${Math.floor(newLocalTime / 1000)}.${(newLocalTime % 1000).toString().padStart(3, '0')}`;
      execSync(`sudo ${dateCommand}`, { stdio: 'inherit' });
      console.log('Local time adjusted successfully.');
    } catch (e: any) {
      console.error(`Failed to adjust time on Unix-like system: ${e.message}`);
      console.error('Please ensure you have root privileges or run with `sudo`.');
    }
  }
}

async function main() {
  const args = process.argv.slice(2);
  let beaconUrl: string | undefined;
  let adjustTime = false;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--beacon-url' && args[i + 1]) {
      beaconUrl = args[i + 1];
      i++;
    } else if (args[i] === '--adjust') {
      adjustTime = true;
    }
  }

  if (!beaconUrl) {
    console.error('Error: --beacon-url is required.');
    process.exit(1);
  }

  try {
    const beaconTimestamp = await getTimeFromBeacon(beaconUrl);
    const localTimestamp = Date.now();
    const offsetMs = beaconTimestamp - localTimestamp;

    console.log(`Temporal Sync Beacon Status:`);
    console.log(`  Beacon URL: ${beaconUrl}`);
    console.log(`  Beacon Timestamp: ${new Date(beaconTimestamp).toISOString()}`);
    console.log(`  Local Timestamp: ${new Date(localTimestamp).toISOString()}`);
    console.log(`  Temporal Offset: ${offsetMs}ms`);

    if (adjustTime) {
      if (Math.abs(offsetMs) > 1000) { // Only adjust if offset is significant
        adjustLocalTime(offsetMs);
      } else {
        console.log('Local time is already within acceptable synchronization range. No adjustment needed.');
      }
    }

  } catch (error) {
    console.error('Temporal synchronization failed.');
    process.exit(1);
  }
}

main();
