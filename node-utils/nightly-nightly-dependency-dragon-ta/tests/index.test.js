import { getPackageJson, getLatestNpmVersion, compareVersions, main } from '../src/index.js';
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import assert from 'assert';
import sinon from 'sinon'; // For mocking fetch and fs

// Helper for __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

describe('Nightly Dependency Dragon Tamer', () => {
    let readFileStub;
    let fetchStub;
    let consoleLogStub;
    let processExitStub;

    beforeEach(() => {
        readFileStub = sinon.stub(fs, 'readFile');
        fetchStub = sinon.stub(global, 'fetch');
        consoleLogStub = sinon.stub(console, 'log');
        processExitStub = sinon.stub(process, 'exit');
    });

    afterEach(() => {
        sinon.restore();
    });

    describe('getPackageJson', () => {
        it('should read and parse package.json correctly', async () => {
            // Mock rationale: Simulates reading a package.json file from disk without actual file I/O.
            readFileStub.withArgs(path.join('/test/path', 'package.json'), 'utf8')
                .returns(Promise.resolve(JSON.stringify({ name: 'test-app', version: '1.0.0' })));

            const pkg = await getPackageJson('/test/path');
            assert.deepStrictEqual(pkg, { name: 'test-app', version: '1.0.0' });
        });

        it('should handle file not found error', async () => {
            // Mock rationale: Simulates a file not found error when trying to read package.json.
            const error = new Error('File not found');
            error.code = 'ENOENT';
            readFileStub.withArgs(path.join('/nonexistent', 'package.json'), 'utf8')
                .returns(Promise.reject(error));

            await getPackageJson('/nonexistent');
            assert(consoleLogStub.calledWithMatch('Error: package.json not found'));
            assert(processExitStub.calledWith(1));
        });

        it('should handle JSON parsing error', async () => {
            // Mock rationale: Simulates a malformed package.json file.
            readFileStub.withArgs(path.join('/malformed', 'package.json'), 'utf8')
                .returns(Promise.resolve('{"name": "test", "version": "1.0.0"')); // Invalid JSON

            await getPackageJson('/malformed');
            assert(consoleLogStub.calledWithMatch('Error reading or parsing package.json'));
            assert(processExitStub.calledWith(1));
        });
    });

    describe('getLatestNpmVersion', () => {
        it('should return the latest version for a package', async () => {
            // Mock rationale: Simulates a successful npm registry API response for a package.
            fetchStub.withArgs('https://registry.npmjs.org/express')
                .returns(Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({ 'dist-tags': { latest: '4.18.2' } })
                }));

            const latest = await getLatestNpmVersion('express');
            assert.strictEqual(latest, '4.18.2');
        });

        it('should return null if package not found (404)', async () => {
            // Mock rationale: Simulates a 404 response from npm registry, indicating package not found.
            fetchStub.withArgs('https://registry.npmjs.org/nonexistent-package')
                .returns(Promise.resolve({
                    ok: false,
                    status: 404,
                    statusText: 'Not Found'
                }));

            const latest = await getLatestNpmVersion('nonexistent-package');
            assert.strictEqual(latest, null);
        });

        it('should return null and log warning for other fetch errors', async () => {
            // Mock rationale: Simulates a network error or other non-404 HTTP error from npm registry.
            fetchStub.withArgs('https://registry.npmjs.org/error-package')
                .returns(Promise.resolve({
                    ok: false,
                    status: 500,
                    statusText: 'Internal Server Error'
                }));

            const latest = await getLatestNpmVersion('error-package');
            assert.strictEqual(latest, null);
            assert(consoleLogStub.calledWithMatch('Warning: Could not check npm for error-package. Error: Failed to fetch package info for error-package: Internal Server Error'));
        });

        it('should return null and log warning for network errors', async () => {
            // Mock rationale: Simulates a network connectivity issue during fetch.
            fetchStub.withArgs('https://registry.npmjs.org/network-error')
                .returns(Promise.reject(new Error('Network down')));

            const latest = await getLatestNpmVersion('network-error');
            assert.strictEqual(latest, null);
            assert(consoleLogStub.calledWithMatch('Warning: Could not check npm for network-error. Error: Network down'));
        });
    });

    describe('compareVersions', () => {
        it('should identify major version updates', () => {
            assert.strictEqual(compareVersions('1.0.0', '2.0.0'), 'Major');
            assert.strictEqual(compareVersions('0.9.0', '1.0.0'), 'Major');
        });

        it('should identify minor version updates', () => {
            assert.strictEqual(compareVersions('1.0.0', '1.1.0'), 'Minor');
            assert.strictEqual(compareVersions('1.5.0', '1.6.2'), 'Minor');
        });

        it('should identify patch version updates', () => {
            assert.strictEqual(compareVersions('1.0.0', '1.0.1'), 'Patch');
            assert.strictEqual(compareVersions('1.2.3', '1.2.4'), 'Patch');
        });

        it('should identify up-to-date versions', () => {
            assert.strictEqual(compareVersions('1.0.0', '1.0.0'), 'Up-to-date');
            assert.strictEqual(compareVersions('1.2.3', '1.2.3'), 'Up-to-date');
        });

        it('should handle invalid inputs gracefully', () => {
            assert.strictEqual(compareVersions(null, '1.0.0'), 'unknown');
            assert.strictEqual(compareVersions('1.0.0', null), 'unknown');
            assert.strictEqual(compareVersions('invalid', '1.0.0'), 'Major'); // Behaves as if 0.0.0
            assert.strictEqual(compareVersions('1.0.0', 'invalid'), 'Up-to-date'); // Behaves as if 1.0.0
        });
    });

    describe('main', () => {
        it('should report outdated dependencies', async () => {
            // Mock rationale: Simulates a package.json with outdated dependencies and corresponding npm registry responses.
            readFileStub.withArgs(path.join(process.cwd(), 'package.json'), 'utf8')
                .returns(Promise.resolve(JSON.stringify({
                    name: 'test-project',
                    version: '1.0.0',
                    dependencies: {
                        'express': '^4.17.1',
                        'lodash': '~4.17.20'
                    },
                    devDependencies: {
                        'jest': '26.6.3'
                    }
                })));

            fetchStub.withArgs('https://registry.npmjs.org/express')
                .returns(Promise.resolve({ ok: true, json: () => Promise.resolve({ 'dist-tags': { latest: '4.18.2' } }) }));
            fetchStub.withArgs('https://registry.npmjs.org/lodash')
                .returns(Promise.resolve({ ok: true, json: () => Promise.resolve({ 'dist-tags': { latest: '4.17.21' } }) }));
            fetchStub.withArgs('https://registry.npmjs.org/jest')
                .returns(Promise.resolve({ ok: true, json: () => Promise.resolve({ 'dist-tags': { latest: '29.7.0' } }) }));

            await main();

            assert(consoleLogStub.calledWithMatch('🐉 Taming the Dependency Dragons... 🐉'));
            assert(consoleLogStub.calledWithMatch('Scanning package.json at:'));
            assert(consoleLogStub.calledWithMatch('  - express: Current 4.17.1 -> Latest 4.18.2 (\x1b[31mOutdated: Major\x1b[0m)'));
            assert(consoleLogStub.calledWithMatch('  - lodash: Current 4.17.20 -> Latest 4.17.21 (\x1b[36mOutdated: Patch\x1b[0m)'));
            assert(consoleLogStub.calledWithMatch('  - jest: Current 26.6.3 -> Latest 29.7.0 (\x1b[31mOutdated: Major\x1b[0m)'));
            assert(consoleLogStub.calledWithMatch('Summary: 3 dragons found, 3 need taming!'));
        });

        it('should report all dependencies are up-to-date', async () => {
            // Mock rationale: Simulates a package.json where all dependencies are already at their latest versions.
            readFileStub.withArgs(path.join(process.cwd(), 'package.json'), 'utf8')
                .returns(Promise.resolve(JSON.stringify({
                    name: 'test-project',
                    version: '1.0.0',
                    dependencies: {
                        'express': '4.18.2'
                    }
                })));

            fetchStub.withArgs('https://registry.npmjs.org/express')
                .returns(Promise.resolve({ ok: true, json: () => Promise.resolve({ 'dist-tags': { latest: '4.18.2' } }) }));

            await main();

            assert(consoleLogStub.calledWithMatch('All your dependency dragons are well-behaved and up-to-date! ✨'));
        });

        it('should handle packages not found on npm gracefully', async () => {
            // Mock rationale: Simulates a package.json with a dependency that doesn't exist on npm.
            readFileStub.withArgs(path.join(process.cwd(), 'package.json'), 'utf8')
                .returns(Promise.resolve(JSON.stringify({
                    name: 'test-project',
                    version: '1.0.0',
                    dependencies: {
                        'nonexistent-package': '1.0.0'
                    }
                })));

            fetchStub.withArgs('https://registry.npmjs.org/nonexistent-package')
                .returns(Promise.resolve({ ok: false, status: 404, statusText: 'Not Found' }));

            await main();

            assert(consoleLogStub.calledWithMatch('All your dependency dragons are well-behaved and up-to-date! ✨')); // No outdated packages reported
            assert(consoleLogStub.notCalledWithMatch('nonexistent-package')); // Should not report it as outdated
        });
    });
});
