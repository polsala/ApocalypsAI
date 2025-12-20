const { program } = require('commander');

// Simple mapping for vowel substitution and consonant shifts
const vowelMap = {
    'a': 'orp',
    'e': 'elp',
    'i': 'ip',
    'o': 'o',
    'u': 'up'
};

const consonantMap = {
    'b': 'bop',
    'c': 'caz',
    'd': 'daz',
    'f': 'flib',
    'g': 'glorp',
    'h': 'hazz',
    'j': 'jizz',
    'k': 'kazz',
    'l': 'lop',
    'm': 'morp',
    'n': 'norp',
    'p': 'paz',
    'q': 'quaz',
    'r': 'raz',
    's': 'snorp',
    't': 'taz',
    'v': 'vord',
    'w': 'worp',
    'x': 'xaz',
    'y': 'yazz',
    'z': 'zorp'
};

function encode(text) {
    let encoded = '';
    const lowerText = text.toLowerCase();
    for (let i = 0; i < lowerText.length; i++) {
        const char = lowerText[i];
        if (char in vowelMap) {
            encoded += vowelMap[char];
        } else if (char in consonantMap) {
            encoded += consonantMap[char];
        } else {
            encoded += char; // Keep non-alphabetic characters as is
        }
    }
    // Add some random alien-like suffixes/prefixes for more flair
    const suffixes = ['!', '?', '.', '...', '!!!'];
    const prefixes = ['Zorp ', 'Flib ', 'Glarp ', 'Worp '];
    if (Math.random() > 0.5) {
        encoded = prefixes[Math.floor(Math.random() * prefixes.length)] + encoded;
    }
    if (Math.random() > 0.5) {
        encoded += suffixes[Math.floor(Math.random() * suffixes.length)];
    }
    return encoded.charAt(0).toUpperCase() + encoded.slice(1);
}

function decode(text) {
    // This is a simplified decoder. It tries to reverse the most common transformations.
    // It's not perfect and might not always recover the exact original string.
    let decoded = text.toLowerCase();

    // Remove common prefixes and suffixes
    const prefixes = ['Zorp ', 'Flib ', 'Glarp ', 'Worp '];
    for (const prefix of prefixes) {
        if (decoded.startsWith(prefix.toLowerCase())) {
            decoded = decoded.substring(prefix.length);
            break;
        }
    }
    const suffixes = ['!', '?', '.', '...', '!!!'];
    for (const suffix of suffixes) {
        if (decoded.endsWith(suffix)) {
            decoded = decoded.substring(0, decoded.length - suffix.length);
            break;
        }
    }

    // Reverse vowel and consonant mappings (simplified)
    // This is a heuristic and might require manual adjustment for complex cases.
    for (const [vowel, mapped] of Object.entries(vowelMap)) {
        decoded = decoded.split(mapped).join(vowel);
    }
    for (const [consonant, mapped] of Object.entries(consonantMap)) {
        decoded = decoded.split(mapped).join(consonant);
    }

    // Clean up potential double spaces or extra characters from mapping
    decoded = decoded.replace(/\s+/g, ' ').trim();

    return decoded.charAt(0).toUpperCase() + decoded.slice(1);
}

program
    .version('1.0.0')
    .description('Cosmic Chatter Translator: Encode and decode messages into alien chatter.');

program
    .command('encode <text>')
    .description('Encode text into cosmic chatter')
    .action((text) => {
        console.log(encode(text));
    });

program
    .command('decode <text>')
    .description('Decode cosmic chatter back to text')
    .action((text) => {
        console.log(decode(text));
    });

program.parse(process.argv);

module.exports = { encode, decode };
