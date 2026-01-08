import axios from 'axios';
import { program } from 'commander';

interface NodeTimeResponse {
  timestamp: number;
}

interface NodeStatus {
  url: string;
  timestamp: number | null;
  error: string | null;
}

async function getNodeTimestamp(url: string): Promise<NodeStatus> {
  try {
    const response = await axios.get<NodeTimeResponse>(url, { timeout: 5000 });
    if (typeof response.data.timestamp !== 'number') {
      return { url, timestamp: null, error: 'Invalid timestamp format received' };
    }
    return { url, timestamp: response.data.timestamp, error: null };
  } catch (error: any) {
    return { url, timestamp: null, error: error.message };
  }
}

async function checkTemporalSync(nodeUrls: string[], toleranceSeconds: number): Promise<void> {
  console.log(`Checking temporal sync for nodes: ${nodeUrls.join(', ')} with tolerance ${toleranceSeconds}s...`);

  const statuses: NodeStatus[] = await Promise.all(
    nodeUrls.map(url => getNodeTimestamp(url))
  );

  const validStatuses = statuses.filter(s => s.timestamp !== null) as { url: string; timestamp: number; error: null }[];
  const invalidStatuses = statuses.filter(s => s.timestamp === null);

  if (invalidStatuses.length > 0) {
    console.error('\n--- Errors Encountered ---');
    invalidStatuses.forEach(s => {
      console.error(`  ${s.url}: ${s.error}`);
    });
  }

  if (validStatuses.length < 2) {
    console.error('\nNot enough valid nodes to perform sync check.');
    return;
  }

  const firstTimestamp = validStatuses[0].timestamp;
  let maxDiff = 0;
  let syncStatus = 'SYNCED';

  for (let i = 1; i < validStatuses.length; i++) {
    const diff = Math.abs(validStatuses[i].timestamp - firstTimestamp);
    if (diff > maxDiff) {
      maxDiff = diff;
    }
    if (diff > toleranceSeconds * 1000) {
      syncStatus = 'DESYNCED';
    }
  }

  console.log('\n--- Sync Report ---');
  validStatuses.forEach(s => {
    const diffFromFirst = s.timestamp - firstTimestamp;
    console.log(`  ${s.url}: Timestamp ${s.timestamp} (Difference: ${diffFromFirst}ms)`);
  });

  console.log(`\nMaximum temporal drift detected: ${maxDiff}ms`);
  console.log(`Overall sync status: ${syncStatus}`);

  if (syncStatus === 'DESYNCED') {
    process.exitCode = 1; // Indicate failure
  }
}

program
  .version('1.0.0')
  .description('Checks temporal synchronization across multiple simulated nodes.')
  .requiredOption('-n, --nodes <urls...>', 'List of temporal node URLs to check')
  .option('-t, --tolerance <seconds>', 'Maximum acceptable time difference in seconds', '5')
  .action(async (options) => {
    const toleranceSeconds = parseInt(options.tolerance, 10);
    if (isNaN(toleranceSeconds) || toleranceSeconds < 0) {
      console.error('Error: Tolerance must be a non-negative number.');
      process.exit(1);
    }
    await checkTemporalSync(options.nodes, toleranceSeconds);
  });

program.parse(process.argv);
