const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const SIGIL_LOG_FILE = path.join(__dirname, '..', 'sigils.json');

const adjectives = [
    "Whispering", "Rusty", "Silent", "Glimmering", "Forgotten",
    "Ancient", "Mystic", "Ethereal", "Shadowy", "Vibrant",
    "Broken", "Shifting", "Cosmic", "Temporal", "Void-touched"
];

const nouns = [
    "Orb", "Cog", "Echo", "Shard", "Relic",
    "Glyph", "Rune", "Nexus", "Fragment", "Beacon",
    "Whisper", "Portal", "Cipher", "Amulet", "Chronicle"
];

function generateSigil(fileContent) {
    const hash = crypto.createHash('md5').update(fileContent).digest('hex');
    const randomAdjective = adjectives[Math.floor(Math.random() * adjectives.length)];
    const randomNoun = nouns[Math.floor(Math.random() * nouns.length)];
    return `${hash.substring(0, 8)}-${randomAdjective}-${randomNoun}`;
}

function readSigilLog() {
    try {
        if (fs.existsSync(SIGIL_LOG_FILE)) {
            const logContent = fs.readFileSync(SIGIL_LOG_FILE, 'utf8');
            return JSON.parse(logContent);
        }
    } catch (error) {
        console.error("Error reading sigil log:", error.message);
    }
    return [];
}

function writeSigilLog(logEntries) {
    try {
        fs.writeFileSync(SIGIL_LOG_FILE, JSON.stringify(logEntries, null, 2), 'utf8');
    } catch (error) {
        console.error("Error writing sigil log:", error.message);
    }
}

async function blessFile(filePath) {
    if (!filePath) {
        console.error("Error: Please provide a file path.");
        process.exit(1);
    }

    const absolutePath = path.resolve(filePath);

    try {
        const fileContent = fs.readFileSync(absolutePath, 'utf8');
        const sigil = generateSigil(fileContent);
        const timestamp = new Date().toISOString();

        const logEntries = readSigilLog();
        logEntries.push({ timestamp, filePath: absolutePath, sigil });
        writeSigilLog(logEntries);

        console.log("File blessed!");
        console.log(`Sigil: ${sigil}`);
        console.log(`Logged to: ${path.basename(SIGIL_LOG_FILE)}`);
        return sigil; // For testing purposes
    } catch (error) {
        if (error.code === 'ENOENT') {
            console.error(`Error: File not found at '${absolutePath}'`);
        } else {
            console.error(`An unexpected error occurred: ${error.message}`);
        }
        process.exit(1);
    }
}

if (require.main === module) {
    const filePath = process.argv[2];
    blessFile(filePath);
}

module.exports = {
    generateSigil,
    readSigilLog,
    writeSigilLog,
    blessFile,
    _adjectives: adjectives, // Export for testing
    _nouns: nouns // Export for testing
};
