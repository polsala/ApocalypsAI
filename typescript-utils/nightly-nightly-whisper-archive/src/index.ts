import * as fs from 'fs';
import * as path from 'path';
import { v4 as uuidv4 } from 'uuid';
import { Whisper, WhisperArchive } from './types';

const ARCHIVE_FILE = path.join(process.env.HOME || process.env.USERPROFILE || '.', '.nightly-whisper-archive.json');

function loadArchive(): WhisperArchive {
  if (!fs.existsSync(ARCHIVE_FILE)) {
    return { whispers: [] };
  }
  const data = fs.readFileSync(ARCHIVE_FILE, 'utf8');
  try {
    return JSON.parse(data) as WhisperArchive;
  } catch (e) {
    console.error(`Error parsing archive file: ${e}. Initializing empty archive.`);
    return { whispers: [] };
  }
}

function saveArchive(archive: WhisperArchive): void {
  fs.writeFileSync(ARCHIVE_FILE, JSON.stringify(archive, null, 2), 'utf8');
}

function addWhisper(content: string, tags: string[]): Whisper {
  const archive = loadArchive();
  const newWhisper: Whisper = {
    id: uuidv4(),
    content,
    tags: tags.map(tag => tag.toLowerCase()),
    timestamp: new Date().toISOString(),
  };
  archive.whispers.push(newWhisper);
  saveArchive(archive);
  return newWhisper;
}

function listWhispers(filterTag?: string): Whisper[] {
  const archive = loadArchive();
  let filteredWhispers = archive.whispers;
  if (filterTag) {
    const lowerCaseFilterTag = filterTag.toLowerCase();
    filteredWhispers = filteredWhispers.filter(whisper =>
      whisper.tags.includes(lowerCaseFilterTag)
    );
  }
  return filteredWhispers.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
}

function searchWhispers(query: string): Whisper[] {
  const archive = loadArchive();
  const lowerCaseQuery = query.toLowerCase();
  return archive.whispers.filter(whisper =>
    whisper.content.toLowerCase().includes(lowerCaseQuery) ||
    whisper.tags.some(tag => tag.includes(lowerCaseQuery))
  ).sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
}

function getWhisperById(id: string): Whisper | undefined {
  const archive = loadArchive();
  return archive.whispers.find(whisper => whisper.id === id);
}

// CLI Logic
const args = process.argv.slice(2);
const command = args[0];

async function main() {
  if (!command) {
    console.log('Usage: nightly-whisper-archive <command> [options]');
    console.log('Commands: add "content" [--tags tag1,tag2] | list [--tags tag] | search "query" | show <id>');
    process.exit(1);
  }

  switch (command) {
    case 'add': {
      const contentArgIndex = args.findIndex(arg => arg.startsWith('"') || arg.startsWith("'"));
      if (contentArgIndex === -1) {
        console.error('Error: Content not provided. Usage: nightly-whisper-archive add "My thought" [--tags tag1,tag2]');
        process.exit(1);
      }
      let content = args[contentArgIndex];
      if (content.startsWith('"') && content.endsWith('"')) {
        content = content.slice(1, -1);
      } else if (content.startsWith("'") && content.endsWith("'")) {
        content = content.slice(1, -1);
      }

      const tagsArgIndex = args.indexOf('--tags');
      let tags: string[] = [];
      if (tagsArgIndex !== -1 && args[tagsArgIndex + 1]) {
        tags = args[tagsArgIndex + 1].split(',');
      }

      const newWhisper = addWhisper(content, tags);
      console.log(`Whisper added (ID: ${newWhisper.id})`);
      break;
    }
    case 'list': {
      const tagsArgIndex = args.indexOf('--tags');
      const filterTag = (tagsArgIndex !== -1 && args[tagsArgIndex + 1]) ? args[tagsArgIndex + 1] : undefined;
      const whispers = listWhispers(filterTag);
      if (whispers.length === 0) {
        console.log('No whispers found.');
        break;
      }
      whispers.forEach(w => {
        console.log(`ID: ${w.id}`);
        console.log(`  Content: ${w.content}`);
        console.log(`  Tags: ${w.tags.join(', ')}`);
        console.log(`  Timestamp: ${new Date(w.timestamp).toLocaleString()}`);
        console.log('---');
      });
      break;
    }
    case 'search': {
      const queryArgIndex = args.findIndex(arg => arg.startsWith('"') || arg.startsWith("'"));
      if (queryArgIndex === -1) {
        console.error('Error: Search query not provided. Usage: nightly-whisper-archive search "keyword"');
        process.exit(1);
      }
      let query = args[queryArgIndex];
      if (query.startsWith('"') && query.endsWith('"')) {
        query = query.slice(1, -1);
      } else if (query.startsWith("'") && query.endsWith("'")) {
        query = query.slice(1, -1);
      }

      const whispers = searchWhispers(query);
      if (whispers.length === 0) {
        console.log(`No whispers found matching "${query}".`);
        break;
      }
      whispers.forEach(w => {
        console.log(`ID: ${w.id}`);
        console.log(`  Content: ${w.content}`);
        console.log(`  Tags: ${w.tags.join(', ')}`);
        console.log(`  Timestamp: ${new Date(w.timestamp).toLocaleString()}`);
        console.log('---');
      });
      break;
    }
    case 'show': {
      const id = args[1];
      if (!id) {
        console.error('Error: Whisper ID not provided. Usage: nightly-whisper-archive show <id>');
        process.exit(1);
      }
      const whisper = getWhisperById(id);
      if (whisper) {
        console.log(`ID: ${whisper.id}`);
        console.log(`  Content: ${whisper.content}`);
        console.log(`  Tags: ${whisper.tags.join(', ')}`);
        console.log(`  Timestamp: ${new Date(whisper.timestamp).toLocaleString()}`);
      } else {
        console.log(`Whisper with ID "${id}" not found.`);
      }
      break;
    }
    default:
      console.error(`Unknown command: ${command}`);
      console.log('Usage: nightly-whisper-archive <command> [options]');
      console.log('Commands: add "content" [--tags tag1,tag2] | list [--tags tag] | search "query" | show <id>');
      process.exit(1);
  }
}

// Only run main if not imported (e.g., by tests)
if (require.main === module) {
  main();
}

// Export for testing
export { addWhisper, listWhispers, searchWhispers, getWhisperById, ARCHIVE_FILE, loadArchive, saveArchive };
