import * as fs from 'fs';
import * as path from 'path';
import { Command } from 'commander';
import chalk from 'chalk';

interface BlockedSite {
  site: string;
  blockedUntil: number; // Unix timestamp in milliseconds
}

interface State {
  blockedSites: BlockedSite[];
  originalHostsContent: string | null;
  unblockTimeoutId: NodeJS.Timeout | null; // Stored as string for JSON serialization, then converted back
}

const program = new Command();

const HOSTS_PATH = process.platform === 'win32'
  ? path.join(process.env.SystemRoot || 'C:\\Windows', 'System32', 'drivers', 'etc', 'hosts')
  : '/etc/hosts';

const NPPB_DIR = path.join(process.env.HOME || process.env.USERPROFILE || '~', '.nppb');
const STATE_FILE_PATH = path.join(NPPB_DIR, 'state.json');

const DEFAULT_STATE: State = {
  blockedSites: [],
  originalHostsContent: null,
  unblockTimeoutId: null,
};

function ensureNppbDir() {
  if (!fs.existsSync(NPPB_DIR)) {
    fs.mkdirSync(NPPB_DIR, { recursive: true });
  }
}

function loadState(): State {
  ensureNppbDir();
  if (fs.existsSync(STATE_FILE_PATH)) {
    try {
      const rawData = fs.readFileSync(STATE_FILE_PATH, 'utf8');
      const state = JSON.parse(rawData);
      // Clear any old timeout IDs that might be loaded from a previous session
      if (state.unblockTimeoutId) {
        clearTimeout(state.unblockTimeoutId);
        state.unblockTimeoutId = null;
      }
      return { ...DEFAULT_STATE, ...state };
    } catch (error) {
      console.error(chalk.red(`Failed to load state: ${error}. Starting fresh.`));
      return DEFAULT_STATE;
    }
  }
  return DEFAULT_STATE;
}

function saveState(state: State) {
  ensureNppbDir();
  try {
    fs.writeFileSync(STATE_FILE_PATH, JSON.stringify(state, null, 2), 'utf8');
  } catch (error) {
    console.error(chalk.red(`Failed to save state: ${error}`));
  }
}

function readHostsFile(): string {
  try {
    return fs.readFileSync(HOSTS_PATH, 'utf8');
  } catch (error) {
    console.error(chalk.red(`Error reading hosts file (${HOSTS_PATH}): ${error}\n` +
      `Please ensure you have sufficient permissions (e.g., run with 'sudo' or as Administrator).`));
    process.exit(1);
  }
}

function writeHostsFile(content: string) {
  try {
    fs.writeFileSync(HOSTS_PATH, content, 'utf8');
  } catch (error) {
    console.error(chalk.red(`Error writing to hosts file (${HOSTS_PATH}): ${error}\n` +
      `Please ensure you have sufficient permissions (e.g., run with 'sudo' or as Administrator).`));
    process.exit(1);
  }
}

function parseDuration(durationStr: string): number {
  const regex = /(\d+)([smh])/g;
  let totalMilliseconds = 0;
  let match;

  while ((match = regex.exec(durationStr)) !== null) {
    const value = parseInt(match[1], 10);
    const unit = match[2];

    switch (unit) {
      case 's':
        totalMilliseconds += value * 1000;
        break;
      case 'm':
        totalMilliseconds += value * 60 * 1000;
        break;
      case 'h':
        totalMilliseconds += value * 60 * 60 * 1000;
        break;
    }
  }

  if (totalMilliseconds === 0) {
    throw new Error('Invalid duration format. Use e.g., 30m, 1h, 2h30m.');
  }
  return totalMilliseconds;
}

async function blockPortals(durationStr: string, sites: string[]) {
  let state = loadState();

  if (state.blockedSites.length > 0) {
    console.log(chalk.yellow('\n⚠️ Some portals are already blocked. Unblock them first or wait for them to expire.'));
    showStatus();
    return;
  }

  let durationMs: number;
  try {
    durationMs = parseDuration(durationStr);
  } catch (error: any) {
    console.error(chalk.red(`\nError: ${error.message}`));
    process.exit(1);
  }

  const hostsContent = readHostsFile();
  state.originalHostsContent = hostsContent;

  const blockedUntil = Date.now() + durationMs;
  state.blockedSites = sites.map(site => ({ site, blockedUntil }));

  let newHostsContent = hostsContent;
  newHostsContent += '\n# --- NPPB Blocked Portals ---';
  state.blockedSites.forEach(blockedSite => {
    newHostsContent += `\n127.0.0.1\t${blockedSite.site}`;
  });
  newHostsContent += '\n# --- End NPPB Blocked Portals ---';

  writeHostsFile(newHostsContent);
  saveState(state);

  console.log(chalk.green(`\n✨ Poof! The following portals have been sealed for ${durationStr}:`));
  state.blockedSites.forEach(s => console.log(chalk.cyan(`- ${s.site}`)));
  console.log(chalk.green(`They will automatically reopen at ${new Date(blockedUntil).toLocaleTimeString()} on ${new Date(blockedUntil).toLocaleDateString()}.`));
  console.log(chalk.yellow('Remember, you can always use `sudo nppb unblock` to restore access sooner.'));

  // Set a timeout to unblock automatically
  const timeoutId = setTimeout(() => {
    console.log(chalk.green('\n🎉 Time's up! Your focus period has ended. Unblocking portals...'));
    unblockPortals();
  }, durationMs);
  // Note: This timeout will only persist if the process stays alive. For true persistence across reboots, a cron job or systemd timer would be needed.
  // For this utility, we rely on manual unblock or the process staying alive.
  state.unblockTimeoutId = timeoutId;
  saveState(state); // Save state with timeout ID (though it won't survive process exit)
}

async function unblockPortals() {
  let state = loadState();

  if (state.originalHostsContent === null) {
    console.log(chalk.yellow('\n😌 No portals are currently blocked by NPPB. All clear!'));
    return;
  }

  writeHostsFile(state.originalHostsContent);

  if (state.unblockTimeoutId) {
    clearTimeout(state.unblockTimeoutId);
  }

  state = DEFAULT_STATE; // Reset state
  saveState(state);

  console.log(chalk.green('\n🔓 All digital portals have been restored! Go forth and explore (responsibly)!'));
}

function showStatus() {
  const state = loadState();

  if (state.blockedSites.length === 0) {
    console.log(chalk.yellow('\n😌 No portals are currently blocked by NPPB. All clear!'));
    return;
  }

  console.log(chalk.magenta('\n🌌 Current Portal Lockdown Status:'));
  const now = Date.now();

  state.blockedSites.forEach(blockedSite => {
    const timeLeftMs = blockedSite.blockedUntil - now;
    if (timeLeftMs <= 0) {
      console.log(chalk.green(`- ${blockedSite.site}: Expired. Will unblock on next command.`));
      // Automatically unblock if expired
      unblockPortals();
      return;
    }

    const hours = Math.floor(timeLeftMs / (1000 * 60 * 60));
    const minutes = Math.floor((timeLeftMs % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeLeftMs % (1000 * 60)) / 1000);

    let timeLeftStr = '';
    if (hours > 0) timeLeftStr += `${hours}h `;
    if (minutes > 0) timeLeftStr += `${minutes}m `;
    timeLeftStr += `${seconds}s`;

    console.log(chalk.cyan(`- ${blockedSite.site}: Locked for ${timeLeftStr.trim()} (until ${new Date(blockedSite.blockedUntil).toLocaleTimeString()}).`));
  });
  console.log(chalk.yellow('\nTip: Use `sudo nppb unblock` to manually lift the blockade.'));
}

program
  .name('nppb')
  .description('Nightly Procrastination Portal Blocker - Banish distractions!')
  .version('1.0.0');

program
  .command('block <duration> <sites...>')
  .description('Temporarily block access to specified websites.')
  .action(blockPortals);

program
  .command('unblock')
  .description('Unblock all currently blocked websites and restore your hosts file.')
  .action(unblockPortals);

program
  .command('status')
  .description('Show current blocking status.')
  .action(showStatus);

// Check for expired blocks on every run
const initialState = loadState();
if (initialState.blockedSites.length > 0) {
  const now = Date.now();
  const expiredSites = initialState.blockedSites.filter(s => s.blockedUntil <= now);
  if (expiredSites.length > 0) {
    console.log(chalk.yellow('\n⏳ Detected expired portal blocks. Automatically unblocking...'));
    unblockPortals();
  }
}

program.parse(process.argv);
