const assert = require('assert');
const path = require('path');
const { parseArgs, generatePlaylist, formatPlaylist, MOOD_TAGS } = require('../src/index');

// Mock rationale: We need to test the core logic without actually reading files
// or interacting with the real process.argv. For unit tests, we'll test the
// exported functions directly with controlled inputs, avoiding file system
// operations or process argument parsing that would require complex mocking.

const mockSongs = [
    {
        "title": "Wasteland Wanderer",
        "artist": "The Rad-Scorpions",
        "tags": ["exploration", "somber", "journey"]
    },
    {
        "title": "Raid on Sector 7",
        "artist": "Mutant Mayhem",
        "tags": ["action", "upbeat", "combat"]
    },
    {
        "title": "Echoes of the Old World",
        "artist": "The Silent Survivors",
        "tags": ["contemplation", "melancholy"]
    },
    {
        "title": "Scavenger's Anthem",
        "artist": "Dusty Road Crew",
        "tags": ["exploration", "upbeat"]
    },
    {
        "title": "Calm Before the Storm",
        "artist": "The Quiet Ones",
        "tags": ["chill", "contemplation"]
    },
    {
        "title": "Untagged Song",
        "artist": "Unknown",
        "tags": []
    },
    {
        "title": "Another Untagged",
        "artist": "Unknown",
        "tags": null
    }
];

function test(name, fn) {
    try {
        fn();
        console.log(`✓ ${name}`);
    } catch (error) {
        console.error(`✗ ${name}`);
        console.error(error);
        process.exit(1);
    }
}

test('parseArgs should correctly parse file and mood arguments', () => {
    const args = ['--file', 'songs.json', '--mood', 'exploration'];
    const parsed = parseArgs(args);
    assert.deepStrictEqual(parsed, { file: 'songs.json', mood: 'exploration' });
});

test('parseArgs should handle boolean flags (e.g., --verbose)', () => {
    const args = ['--verbose', '--file', 'songs.json'];
    const parsed = parseArgs(args);
    assert.deepStrictEqual(parsed, { verbose: true, file: 'songs.json' });
});

test('parseArgs should handle flags without a value as boolean true', () => {
    const args = ['--mood', '--file', 'songs.json']; // 'mood' will be true, 'file' will be 'songs.json'
    const parsed = parseArgs(args);
    assert.deepStrictEqual(parsed, { mood: true, file: 'songs.json' });
});

test('generatePlaylist should filter songs by "exploration" mood', () => {
    const playlist = generatePlaylist(mockSongs, 'exploration');
    assert.strictEqual(playlist.length, 2);
    assert.strictEqual(playlist[0].title, 'Wasteland Wanderer');
    assert.strictEqual(playlist[1].title, 'Scavenger\'s Anthem');
});

test('generatePlaylist should filter songs by "action" mood', () => {
    const playlist = generatePlaylist(mockSongs, 'action');
    assert.strictEqual(playlist.length, 1);
    assert.strictEqual(playlist[0].title, 'Raid on Sector 7');
});

test('generatePlaylist should filter songs by "contemplation" mood', () => {
    const playlist = generatePlaylist(mockSongs, 'contemplation');
    assert.strictEqual(playlist.length, 2);
    assert.strictEqual(playlist[0].title, 'Echoes of the Old World');
    assert.strictEqual(playlist[1].title, 'Calm Before the Storm');
});

test('generatePlaylist should filter songs by "chill" mood', () => {
    const playlist = generatePlaylist(mockSongs, 'chill');
    assert.strictEqual(playlist.length, 1);
    assert.strictEqual(playlist[0].title, 'Calm Before the Storm');
});

test('generatePlaylist should return empty array if no songs match mood', () => {
    const playlist = generatePlaylist(mockSongs, 'nonexistent-mood');
    assert.strictEqual(playlist.length, 0);
});

test('generatePlaylist should return empty array if songs have no tags', () => {
    const playlist = generatePlaylist([
        { title: "No Tags", artist: "Anon", tags: [] },
        { title: "Null Tags", artist: "Anon", tags: null }
    ], 'exploration');
    assert.strictEqual(playlist.length, 0);
});

test('formatPlaylist should correctly format an empty playlist', () => {
    const output = formatPlaylist('survival', []);
    assert.ok(output.includes('--- Nightly Apocalypse Tunes: Survival Playlist ---'));
    assert.ok(output.includes('No tunes found for this mood. Perhaps the silence is more fitting.'));
});

test('formatPlaylist should correctly format a non-empty playlist', () => {
    const playlist = [
        { title: "Song A", artist: "Artist X" },
        { title: "Song B", artist: "Artist Y" }
    ];
    const output = formatPlaylist('raid', playlist);
    assert.ok(output.includes('--- Nightly Apocalypse Tunes: Raid Playlist ---'));
    assert.ok(output.includes('1. Song A by Artist X'));
    assert.ok(output.includes('2. Song B by Artist Y'));
});

console.log('All tests passed!');
