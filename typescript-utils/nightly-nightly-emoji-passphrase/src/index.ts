#!/usr/bin/env node
interface Options {
  length?: number;
  delimiter?: string;
  emoji?: boolean;
}

const WORDS = ['alpha','bravo','charlie','delta','echo','foxtrot','golf','hotel','india','juliet'] as const;
const EMOJI_MAP: Record<string,string> = {
  alpha: '🅰️',
  bravo: '🥦',
  charlie: '🐱',
  delta: '🔺',
  echo: '📢',
  foxtrot: '🩰',
  golf: '⛳',
  hotel: '🏨',
  india: '🇮🇳',
  juliet: '🎭',
};

export function generatePassphrase(opts: Options = {}): string {
  const length = opts.length ?? 4;
  const delimiter = opts.delimiter ?? ' ';
  const useEmoji = opts.emoji ?? false;
  const tokens: string[] = [];
  for (let i = 0; i < length; i++) {
    const idx = Math.floor(Math.random() * WORDS.length);
    const word = WORDS[idx];
    tokens.push(useEmoji ? EMOJI_MAP[word] : word);
  }
  return tokens.join(delimiter);
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  const options: Options = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '-l' || arg === '--length') {
      const val = parseInt(args[++i], 10);
      if (!isNaN(val)) options.length = val;
    } else if (arg === '-d' || arg === '--delimiter') {
      options.delimiter = args[++i];
    } else if (arg === '-e' || arg === '--emoji') {
      options.emoji = true;
    }
  }
  const pass = generatePassphrase(options);
  console.log(pass);
}
