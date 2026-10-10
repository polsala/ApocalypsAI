const assert = require('assert');
const sinon = require('sinon'); // For mocking fs and console
const { calculateDistance, optimizeRoute, main } = require('../src/index');
const fs = require('fs'); // Need to import fs to mock it

describe('Nightly Scavenger Route Optimizer', () => {
    let consoleLogStub;
    let consoleErrorStub;
    let processExitStub;

    beforeEach(() => {
        // Mock rationale: Capture console output and prevent process exit during tests.
        consoleLogStub = sinon.stub(console, 'log');
        consoleErrorStub = sinon.stub(console, 'error');
        processExitStub = sinon.stub(process, 'exit');
    });

    afterEach(() => {
        consoleLogStub.restore();
        consoleErrorStub.restore();
        processExitStub.restore();
        sinon.restore(); // Restore all stubs that were created with sinon.stub
    });

    describe('calculateDistance', () => {
        it('should calculate the Euclidean distance between two points', () => {
            const p1 = { x: 0, y: 0 };
            const p2 = { x: 3, y: 4 };
            assert.strictEqual(calculateDistance(p1, p2), 5);
        });

        it('should return 0 for identical points', () => {
            const p1 = { x: 5, y: 5 };
            const p2 = { x: 5, y: 5 };
            assert.strictEqual(calculateDistance(p1, p2), 0);
        });

        it('should handle negative coordinates', () => {
            const p1 = { x: -1, y: -1 };
            const p2 = { x: 2, y: 3 };
            // sqrt((2 - (-1))^2 + (3 - (-1))^2) = sqrt(3^2 + 4^2) = sqrt(9 + 16) = sqrt(25) = 5
            assert.strictEqual(calculateDistance(p1, p2), 5);
        });
    });

    describe('optimizeRoute', () => {
        it('should return a route with only the start point if no resources are provided', () => {
            const startPoint = { x: 0, y: 0 };
            const resourceLocations = [];
            const { route, totalDistance } = optimizeRoute(startPoint, resourceLocations);
            assert.deepStrictEqual(route, [{ x: 0, y: 0, name: 'Start' }]);
            assert.strictEqual(totalDistance, 0);
        });

        it('should optimize a simple route with two resources', () => {
            const startPoint = { x: 0, y: 0 };
            const resourceLocations = [
                { name: 'Water Source', x: 10, y: 0 },
                { name: 'Food Cache', x: 0, y: 5 }
            ];
            const { route, totalDistance } = optimizeRoute(startPoint, resourceLocations);

            // Expected order: Start (0,0) -> Food Cache (0,5) (dist 5) -> Water Source (10,0) (dist sqrt((10-0)^2 + (0-5)^2) = sqrt(100+25) = sqrt(125) approx 11.18)
            // Total: 5 + 11.18 = 16.18
            assert.strictEqual(route.length, 3);
            assert.deepStrictEqual(route[0], { x: 0, y: 0, name: 'Start' });
            assert.deepStrictEqual(route[1], { name: 'Food Cache', x: 0, y: 5 });
            assert.deepStrictEqual(route[2], { name: 'Water Source', x: 10, y: 0 });
            assert.ok(Math.abs(totalDistance - (5 + Math.sqrt(125))) < 0.001);
        });

        it('should optimize a more complex route', () => {
            const startPoint = { x: 0, y: 0 };
            const resourceLocations = [
                { name: 'A', x: 1, y: 0 },
                { name: 'B', x: 0, y: 1 },
                { name: 'C', x: 10, y: 10 }
            ];
            const { route, totalDistance } = optimizeRoute(startPoint, resourceLocations);

            // Start (0,0)
            // Nearest to (0,0) is A (1,0) (dist 1) or B (0,1) (dist 1). Due to iteration order, 'A' will be picked first.
            // Route: Start -> A (1,0)
            // Remaining: B (0,1), C (10,10)
            // From A (1,0):
            //   To B (0,1): sqrt((1-0)^2 + (0-1)^2) = sqrt(1+1) = sqrt(2) approx 1.414
            //   To C (10,10): sqrt((1-10)^2 + (0-10)^2) = sqrt(81+100) = sqrt(181) approx 13.45
            // Nearest is B (0,1)
            // Route: Start -> A (1,0) -> B (0,1)
            // Remaining: C (10,10)
            // From B (0,1):
            //   To C (10,10): sqrt((0-10)^2 + (1-10)^2) = sqrt(100+81) = sqrt(181) approx 13.45
            // Route: Start -> A (1,0) -> B (0,1) -> C (10,10)
            // Total distance: 1 + sqrt(2) + sqrt(181) approx 1 + 1.414 + 13.453 = 15.867

            assert.strictEqual(route.length, 4);
            assert.deepStrictEqual(route[0], { x: 0, y: 0, name: 'Start' });
            assert.deepStrictEqual(route[1], { name: 'A', x: 1, y: 0 });
            assert.deepStrictEqual(route[2], { name: 'B', x: 0, y: 1 });
            assert.deepStrictEqual(route[3], { name: 'C', x: 10, y: 10 });
            assert.ok(Math.abs(totalDistance - (1 + Math.sqrt(2) + Math.sqrt(181))) < 0.001);
        });
    });

    describe('main', () => {
        it('should print usage and exit if arguments are missing', () => {
            main([]);
            assert.ok(consoleErrorStub.calledWith('Usage: node src/index.js <startX> <startY> <resourceFilePath>'));
            assert.ok(processExitStub.calledWith(1));
        });

        it('should print error and exit if resource file is invalid JSON', () => {
            // Mock rationale: Avoid actual file system access for deterministic tests.
            sinon.stub(fs, 'readFileSync').returns('this is not json');
            main(['10', '20', 'invalid.json']);
            assert.ok(consoleErrorStub.calledWithMatch(/Error reading or parsing resource file: Unexpected token/));
            assert.ok(processExitStub.calledWith(1));
        });

        it('should print error and exit if resource file has invalid structure', () => {
            // Mock rationale: Avoid actual file system access for deterministic tests.
            sinon.stub(fs, 'readFileSync').returns(JSON.stringify([{ name: 'A', x: 1 }])); // Missing 'y'
            main(['10', '20', 'malformed.json']);
            assert.ok(consoleErrorStub.calledWithMatch(/Resource file must be an array of objects with "name", "x", and "y" properties./));
            assert.ok(processExitStub.calledWith(1));
        });

        it('should successfully optimize and print a route', () => {
            const mockResources = [
                { name: 'Supply Drop', x: 5, y: 5 },
                { name: 'Abandoned Bunker', x: 1, y: 1 }
            ];
            // Mock rationale: Avoid actual file system access for deterministic tests.
            sinon.stub(fs, 'readFileSync').returns(JSON.stringify(mockResources));

            main(['0', '0', 'resources.json']);

            assert.ok(consoleLogStub.calledWith('--- Optimized Scavenging Route ---'));
            assert.ok(consoleLogStub.calledWith('1. Start (0, 0)'));
            assert.ok(consoleLogStub.calledWith('2. Abandoned Bunker (1, 1)')); // sqrt(1^2 + 1^2) = sqrt(2)
            assert.ok(consoleLogStub.calledWith('3. Supply Drop (5, 5)')); // from (1,1) to (5,5): sqrt((5-1)^2 + (5-1)^2) = sqrt(4^2 + 4^2) = sqrt(16+16) = sqrt(32)
            // Total distance: sqrt(2) + sqrt(32) approx 1.414 + 5.657 = 7.071
            assert.ok(consoleLogStub.calledWithMatch(/Total estimated travel distance: 7.07 units/));
            assert.ok(processExitStub.notCalled);
        });
    });
});
