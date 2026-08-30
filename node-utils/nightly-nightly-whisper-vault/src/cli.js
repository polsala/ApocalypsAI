#!/usr/bin/env node

const WhisperVault = require('./whisperVault');
const path = require('path');

const VAULT_FILE_NAME = '.whisper_vault.json';
const vaultFilePath = path.join(process.cwd(), VAULT_FILE_NAME);

function getEncryptionKey() {
    // Check for --key flag first
    const keyFlagIndex = process.argv.indexOf('--key');
    if (keyFlagIndex > -1 && process.argv[keyFlagIndex + 1]) {
        return process.argv[keyFlagIndex + 1];
    }

    // Fallback to environment variable
    if (process.env.WHISPER_KEY) {
        return process.env.WHISPER_KEY;
    }

    console.error("Error: Encryption key not provided. Use --key <your_key> or set WHISPER_KEY environment variable.");
    process.exit(1);
}

async function main() {
    const args = process.argv.slice(2);
    const command = args[0];
    const encryptionKey = getEncryptionKey();

    const vault = new WhisperVault(vaultFilePath, encryptionKey);

    switch (command) {
        case 'add': {
            const message = args[1];
            if (!message) {
                console.error("Usage: add \"<message>\" [--ttl <hours>]");
                process.exit(1);
            }
            const ttlIndex = args.indexOf('--ttl');
            const ttlHours = ttlIndex > -1 ? parseInt(args[ttlIndex + 1], 10) : null;
            if (ttlHours !== null && (isNaN(ttlHours) || ttlHours <= 0)) {
                console.error("Error: --ttl must be a positive number of hours.");
                process.exit(1);
            }
            const id = vault.addWhisper(message, ttlHours);
            console.log(`Whisper added with ID: ${id}${ttlHours ? ` (expires in ${ttlHours} hours)` : ''}`);
            break;
        }
        case 'list': {
            const whispers = vault.listWhispers();
            if (whispers.length === 0) {
                console.log("No active whispers in the vault.");
            } else {
                console.log("Active Whispers:");
                whispers.forEach(w => {
                    console.log(`  ID: ${w.id}`);
                    console.log(`    Created: ${w.createdAt}`);
                    console.log(`    Expires: ${w.expiresAt}`);
                    console.log('---');
                });
            }
            break;
        }
        case 'reveal': {
            const id = args[1];
            if (!id) {
                console.error("Usage: reveal <whisper_id>");
                process.exit(1);
            }
            const content = vault.revealWhisper(id);
            if (content) {
                console.log(`Whisper content (ID: ${id}):\n${content}`);
            } else {
                console.log(`Whisper with ID '${id}' not found or has expired.`);
            }
            break;
        }
        case 'purge': {
            const purgedCount = vault.purgeExpired();
            console.log(`Purged ${purgedCount} expired whispers.`);
            break;
        }
        default: {
            console.log("Usage: node src/cli.js <command> [options]");
            console.log("Commands:");
            console.log("  add \"<message>\" [--ttl <hours>] - Add a new whisper");
            console.log("  list                               - List all active whispers");
            console.log("  reveal <whisper_id>                - Reveal a specific whisper's content");
            console.log("  purge                              - Remove all expired whispers");
            console.log("Options:");
            console.log("  --key <your_key>                   - Specify encryption key (overrides WHISPER_KEY env var)");
            break;
        }
    }
}

main();
