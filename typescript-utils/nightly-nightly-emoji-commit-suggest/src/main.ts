import { readFileSync } from 'fs';
import { stdin, stdout } from 'process';

export interface EmojiSuggestion {
  emoji: string;
  description: string;
}

export function getEmojiForCommit(message: string): EmojiSuggestion {
  const lower = message.toLowerCase();
  if (/fix|bug/.test(lower)) {
    return { emoji: '🐛', description: 'Bug' };
  }
  if (/feat|feature/.test(lower)) {
    return { emoji: '🚀', description: 'Feature' };
  }
  if (/docs/.test(lower)) {
    return { emoji: '📚', description: 'Docs' };
  }
  if (/refactor/.test(lower)) {
    return { emoji: '🔧', description: 'Refactor' };
  }
  if (/test/.test(lower)) {
    return { emoji: '🧪', description: 'Test' };
  }
  if (/chore/.test(lower)) {
    return { emoji: '🧹', description: 'Chore' };
  }
  if (/style/.test(lower)) {
    return { emoji: '🎨', description: 'Style' };
  }
  if (/breaking change/.test(lower)) {
    return { emoji: '💥', description: 'Breaking Change' };
  }
  return { emoji: '💡', description: 'General' };
}

function main() {
  const args = process.argv.slice(2);
  if (args.length > 0) {
    const message = args.join(' ');
    const suggestion = getEmojiForCommit(message);
    console.log(`${suggestion.emoji} ${suggestion.description}`);
  } else {
    // Read from stdin
    let data = '';
    stdin.setEncoding('utf8');
    stdin.on('data', chunk => data += chunk);
    stdin.on('end', () => {
      const suggestion = getEmojiForCommit(data.trim());
      console.log(`${suggestion.emoji} ${suggestion.description}`);
    });
  }
}

if (require.main === module) {
  main();
}
