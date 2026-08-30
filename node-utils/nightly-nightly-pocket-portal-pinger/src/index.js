import { promises as fs } from 'fs';
import fetch from 'node-fetch';

async function checkPortal(portalPath) {
    if (portalPath.startsWith('http://') || portalPath.startsWith('https://')) {
        try {
            // Use HEAD request for efficiency, as we only care about status
            const response = await fetch(portalPath, { method: 'HEAD', timeout: 5000 });
            if (response.ok) {
                return { status: 'Stable', code: response.status, type: 'URL' };
            } else if (response.status >= 400 && response.status < 500) {
                return { status: 'Fluctuating', code: response.status, type: 'URL' };
            } else {
                return { status: 'Collapsed', code: response.status, type: 'URL' };
            }
        } catch (error) {
            return { status: 'Unreachable', error: error.message, type: 'URL' };
        }
    } else {
        // Assume local file path
        try {
            await fs.access(portalPath, fs.constants.F_OK);
            return { status: 'Stable', type: 'File' };
        } catch (error) {
            return { status: 'Fluctuating', error: error.message, type: 'File' };
        }
    }
}

async function main() {
    const args = process.argv.slice(2);
    const portalListFile = args[0];

    if (!portalListFile) {
        console.error('Usage: node src/index.js <path-to-portal-list-file>');
        process.exit(1);
    }

    try {
        const data = await fs.readFile(portalListFile, 'utf8');
        const portals = data.split('\n').map(line => line.trim()).filter(line => line.length > 0);

        console.log('Initiating Pocket Portal Pinger...');
        console.log('---------------------------------');

        for (const portal of portals) {
            const result = await checkPortal(portal);
            let message = `[${result.type}] ${portal}: `;
            if (result.status === 'Stable') {
                message += `Dimensional Stability: ${result.status}`;
                if (result.code) message += ` (HTTP ${result.code})`;
            } else if (result.status === 'Fluctuating') {
                message += `Dimensional Stability: ${result.status}`;
                if (result.code) message += ` (HTTP ${result.code})`;
                if (result.error) message += ` (Error: ${result.error})`;
            } else if (result.status === 'Collapsed') {
                message += `Dimensional Stability: ${result.status}`;
                if (result.code) message += ` (HTTP ${result.code})`;
            } else if (result.status === 'Unreachable') {
                message += `Dimensional Stability: ${result.status} (Error: ${result.error})`;
            }
            console.log(message);
        }
        console.log('---------------------------------');
        console.log('Pocket Portal Pinger complete.');

    } catch (error) {
        console.error(`Error reading portal list file: ${error.message}`);
        process.exit(1);
    }
}

// Only run main if not in a test environment
if (process.env.NODE_ENV !== 'test') {
    main();
}

// Export for testing
export { checkPortal, main };
