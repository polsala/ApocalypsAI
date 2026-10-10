#!/usr/bin/env node

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Helper for __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Simple CLI argument parser
const args = process.argv.slice(2);
let packageJsonPath = process.cwd(); // Default to current working directory

const pathIndex = args.indexOf('--path');
if (pathIndex > -1 && args[pathIndex + 1]) {
    packageJsonPath = args[pathIndex + 1];
}

async function getPackageJson(dirPath) {
    try {
        const filePath = path.join(dirPath, 'package.json');
        const fileContent = await fs.readFile(filePath, 'utf8');
        return JSON.parse(fileContent);
    } catch (error) {
        if (error.code === 'ENOENT') {
            console.error(`Error: package.json not found at ${dirPath}`);
        } else {
            console.error(`Error reading or parsing package.json: ${error.message}`);
        }
        process.exit(1);
    }
}

async function getLatestNpmVersion(packageName) {
    try {
        const response = await fetch(`https://registry.npmjs.org/${packageName}`);
        if (!response.ok) {
            if (response.status === 404) {
                return null; // Package not found
            }
            throw new Error(`Failed to fetch package info for ${packageName}: ${response.statusText}`);
        }
        const data = await response.json();
        return data['dist-tags']?.latest;
    } catch (error) {
        console.error(`Warning: Could not check npm for ${packageName}. Error: ${error.message}`);
        return null;
    }
}

function compareVersions(current, latest) {
    if (!current || !latest) return 'unknown';

    const parse = (v) => v.split('.').map(Number);
    const [cMajor, cMinor, cPatch] = parse(current);
    const [lMajor, lMinor, lPatch] = parse(latest);

    if (lMajor > cMajor) return 'Major';
    if (lMinor > cMinor) return 'Minor';
    if (lPatch > cPatch) return 'Patch';
    return 'Up-to-date';
}

async function main() {
    console.log('🐉 Taming the Dependency Dragons... 🐉\n');
    console.log(`Scanning package.json at: ${packageJsonPath}\n`);

    const packageJson = await getPackageJson(packageJsonPath);
    const allDependencies = {
        ...packageJson.dependencies,
        ...packageJson.devDependencies,
    };

    const outdatedPackages = [];

    for (const [packageName, currentVersion] of Object.entries(allDependencies)) {
        // Remove caret/tilde from version string for comparison
        const cleanCurrentVersion = currentVersion.replace(/^[\^~]/, '');

        const latestVersion = await getLatestNpmVersion(packageName);

        if (latestVersion && cleanCurrentVersion !== latestVersion) {
            const status = compareVersions(cleanCurrentVersion, latestVersion);
            if (status !== 'Up-to-date') {
                outdatedPackages.push({
                    name: packageName,
                    current: cleanCurrentVersion,
                    latest: latestVersion,
                    status: status,
                });
            }
        }
    }

    if (outdatedPackages.length > 0) {
        console.log('Dependencies:\n');
        outdatedPackages.forEach(pkg => {
            const color = pkg.status === 'Major' ? '\x1b[31m' : pkg.status === 'Minor' ? '\x1b[33m' : '\x1b[36m'; // Red, Yellow, Cyan
            console.log(`  - ${pkg.name}: Current ${pkg.current} -> Latest ${pkg.latest} (${color}Outdated: ${pkg.status}\x1b[0m)`);
        });
        console.log(`\nSummary: ${outdatedPackages.length} dragons found, ${outdatedPackages.length} need taming!`);
        console.log("Run 'npm update' or 'npm install <package>@latest' to soothe them.");
    } else {
        console.log('All your dependency dragons are well-behaved and up-to-date! ✨');
    }
}

// Only run main if not being imported (e.g., for tests)
if (import.meta.url === fileURLToPath(process.argv[1])) {
    main();
}

// Export for testing
export { getPackageJson, getLatestNpmVersion, compareVersions, main };
