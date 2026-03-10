const { manifestGhost, cleanGhosts, listGhosts } = require('./manifestor');
const path = require('path');

const DEFAULT_GHOST_DIR = path.join(process.cwd(), '.ghost_manifest');

async function main() {
    const args = process.argv.slice(2);
    const command = args[0];

    let ghostDir = DEFAULT_GHOST_DIR;
    let content = '';
    let filePaths = [];

    // Basic argument parsing
    for (let i = 1; i < args.length; i++) {
        if (args[i] === '--ghost-dir' && args[i + 1]) {
            ghostDir = args[++i];
        } else if (args[i] === '--content' && args[i + 1]) {
            content = args[++i];
        } else {
            filePaths.push(args[i]);
        }
    }

    switch (command) {
        case 'manifest':
            if (filePaths.length === 0) {
                console.error('Usage: node src/index.js manifest <paths...> [--ghost-dir <dir>] [--content <message>]');
                process.exit(1);
            }
            console.log(`Manifesting ghosts in: ${ghostDir}`);
            for (const filePath of filePaths) {
                const ghostPath = await manifestGhost(filePath, ghostDir, content);
                console.log(`  👻 Manifested: ${ghostPath}`);
            }
            break;
        case 'clean':
            console.log(`Cleaning ghosts from: ${ghostDir}`);
            const cleaned = await cleanGhosts(ghostDir);
            if (cleaned.length > 0) {
                cleaned.forEach(p => console.log(`  🧹 Cleaned: ${p}`));
            } else {
                console.log('  No ghosts to clean.');
            }
            break;
        case 'list':
            console.log(`Listing ghosts in: ${ghostDir}`);
            const ghosts = await listGhosts(ghostDir);
            if (ghosts.length > 0) {
                ghosts.forEach(p => console.log(`  👻 ${p}`));
            } else {
                console.log('  No ghosts found.');
            }
            break;
        default:
            console.error('Unknown command. Usage:');
            console.error('  node src/index.js manifest <paths...> [--ghost-dir <dir>] [--content <message>]');
            console.error('  node src/index.js clean [--ghost-dir <dir>]');
            console.error('  node src/index.js list [--ghost-dir <dir>]');
            process.exit(1);
    }
}

main().catch(console.error);
