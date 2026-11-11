const fs = require('fs');
const path = require('path');

function parseArgs(args) {
    const parsed = {};
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg.startsWith('--')) {
            const key = arg.substring(2);
            const value = args[i + 1];
            if (value && !value.startsWith('--')) {
                parsed[key] = value;
                i++;
            } else {
                parsed[key] = true; // Handle boolean flags if any
            }
        }
    }
    return parsed;
}

const MOOD_TAGS = {
    exploration: ['exploration', 'journey', 'discovery', 'wander'],
    contemplation: ['contemplation', 'melancholy', 'somber', 'reflection'],
    action: ['action', 'combat', 'upbeat', 'raid', 'survival'],
    chill: ['chill', 'relax', 'calm', 'peace']
};

function generatePlaylist(songs, mood) {
    const targetTags = MOOD_TAGS[mood.toLowerCase()] || [mood.toLowerCase()];

    const filteredSongs = songs.filter(song => {
        if (!song.tags || song.tags.length === 0) {
            return false; // Only include songs with tags for mood filtering
        }
        return song.tags.some(tag => targetTags.includes(tag.toLowerCase()));
    });

    return filteredSongs;
}

function formatPlaylist(mood, songs) {
    let output = `--- Nightly Apocalypse Tunes: ${mood.charAt(0).toUpperCase() + mood.slice(1)} Playlist ---\n\n`;

    if (songs.length === 0) {
        output += "No tunes found for this mood. Perhaps the silence is more fitting.\n";
    } else {
        songs.forEach((song, index) => {
            output += `${index + 1}. ${song.title} by ${song.artist}\n`;
        });
    }

    output += `\n----------------------------------------------------\n`;
    return output;
}

function run() {
    const args = parseArgs(process.argv.slice(2));
    const filePath = args.file;
    const mood = args.mood;

    if (!filePath || !mood || mood === true) { // mood === true handles cases like `--mood --file ...`
        console.error("Usage: node src/index.js --file <path_to_songs.json> --mood <mood_name>");
        process.exit(1);
    }

    try {
        const rawData = fs.readFileSync(filePath, 'utf8');
        const songs = JSON.parse(rawData);

        if (!Array.isArray(songs)) {
            throw new Error("Song file must contain a JSON array of songs.");
        }

        const playlist = generatePlaylist(songs, mood);
        console.log(formatPlaylist(mood, playlist));

    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}

// Only run if this file is executed directly
if (require.main === module) {
    run();
}

module.exports = {
    parseArgs,
    generatePlaylist,
    formatPlaylist,
    MOOD_TAGS // Export for testing
};
