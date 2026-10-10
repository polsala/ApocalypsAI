const { findCosmicCommute, setRandomSeed, graph, adjList, SeededRandom } = require('../src/index');
const assert = require('assert');

describe('SeededRandom', () => {
    it('should produce deterministic sequences with the same seed', () => {
        const rng1 = new SeededRandom(123);
        const rng2 = new SeededRandom(123);
        assert.strictEqual(rng1.next(), rng2.next(), 'First numbers should match');
        assert.strictEqual(rng1.next(), rng2.next(), 'Second numbers should match');
        assert.notStrictEqual(rng1.next(), new SeededRandom(456).next(), 'Different seeds should produce different numbers');
    });

    it('should handle zero or negative seeds gracefully', () => {
        const rngZero = new SeededRandom(0);
        const rngNeg = new SeededRandom(-100);
        assert.ok(rngZero.next() > 0 && rngZero.next() < 1);
        assert.ok(rngNeg.next() > 0 && rngNeg.next() < 1);
    });
});

describe('Cosmic Commute Planner', () => {
    let originalAdjList;

    beforeEach(() => {
        // Reset random seed before each test to ensure determinism
        setRandomSeed(null); // Use Math.random by default for non-seeded tests
        // Store original adjList to restore after tests that modify it
        originalAdjList = new Map(adjList);
    });

    afterEach(() => {
        // Restore original adjList after each test
        adjList.clear();
        originalAdjList.forEach((value, key) => adjList.set(key, value));
    });

    it('should find a direct path between two connected nodes', () => {
        // # Mock rationale: Using a fixed seed to ensure anomaly simulation is deterministic.
        // With seed 1, the anomaly roll will be predictable.
        setRandomSeed(1);
        const { path, totalTime, error } = findCosmicCommute("Earth_Orbital_Hub", "Mars_Outpost");
        assert.strictEqual(error, undefined);
        assert.ok(path.length > 0, 'Path should not be empty');
        assert.ok(totalTime > 0, 'Total time should be positive');
        assert.strictEqual(path[0].from, "Earth_Orbital_Hub");
        assert.strictEqual(path[path.length - 1].to, "Mars_Outpost");
    });

    it('should find a multi-segment path', () => {
        // # Mock rationale: Using a fixed seed to ensure anomaly simulation is deterministic.
        setRandomSeed(2);
        const { path, totalTime, error } = findCosmicCommute("Earth_Orbital_Hub", "Jupiter_Mining_Colony");
        assert.strictEqual(error, undefined);
        assert.ok(path.length > 1, 'Path should have multiple segments');
        assert.ok(totalTime > 0, 'Total time should be positive');
        assert.strictEqual(path[0].from, "Earth_Orbital_Hub");
        assert.strictEqual(path[path.length - 1].to, "Jupiter_Mining_Colony");
    });

    it('should return an error for invalid start waypoint', () => {
        const { path, totalTime, error } = findCosmicCommute("Invalid_Start", "Mars_Outpost");
        assert.strictEqual(path.length, 0);
        assert.strictEqual(totalTime, Infinity);
        assert.strictEqual(error, "Invalid start or end waypoint.");
    });

    it('should return an error for invalid end waypoint', () => {
        const { path, totalTime, error } = findCosmicCommute("Earth_Orbital_Hub", "Invalid_End");
        assert.strictEqual(path.length, 0);
        assert.strictEqual(totalTime, Infinity);
        assert.strictEqual(error, "Invalid start or end waypoint.");
    });

    it('should return no path found if nodes are disconnected (hypothetical)', () => {
        // # Mock rationale: Directly manipulating the adjList to simulate a disconnected graph.
        // This is a controlled environment change to test a specific failure mode.
        adjList.clear(); // Clear all edges to simulate a disconnected graph
        graph.nodes.forEach(node => adjList.set(node, [])); // Re-add nodes with no edges

        const { path, totalTime, error } = findCosmicCommute("Earth_Orbital_Hub", "Andromeda_Nexus");
        assert.strictEqual(path.length, 0);
        assert.strictEqual(totalTime, Infinity);
        assert.strictEqual(error, "No path found.");
    });

    it('should handle a path to itself (0 time)', () => {
        const { path, totalTime, error } = findCosmicCommute("Earth_Orbital_Hub", "Earth_Orbital_Hub");
        assert.strictEqual(error, undefined);
        assert.strictEqual(path.length, 0, 'Path to self should have no segments');
        assert.strictEqual(totalTime, 0, 'Total time for path to self should be 0');
    });

    it('should correctly apply a simulated boost with a specific seed', () => {
        // # Mock rationale: Seed 100 is chosen to reliably trigger a "Gravity Assist Boost"
        // on the first edge encountered, allowing for deterministic testing of anomaly effects.
        setRandomSeed(100); // This seed should trigger a boost on some early path
        const { path, totalTime } = findCosmicCommute("Earth_Orbital_Hub", "Mars_Outpost");
        assert.ok(path.length > 0);
        const directEdge = graph.edges.find(e => e[0] === "Earth_Orbital_Hub" && e[1] === "Mars_Outpost");
        const baseTime = directEdge ? directEdge[2] : Infinity;

        // Verify if a boost was applied and time is less than base
        const segment = path.find(s => s.from === "Earth_Orbital_Hub" && s.to === "Mars_Outpost");
        if (segment) {
            assert.ok(segment.anomaly === "Gravity Assist Boost" || segment.anomaly === "Clear Skies", "Expected boost or clear skies");
            if (segment.anomaly === "Gravity Assist Boost") {
                assert.ok(segment.time < baseTime, `Simulated time ${segment.time} should be less than base time ${baseTime}`);
            } else {
                assert.strictEqual(segment.time, baseTime);
            }
        }
    });

    it('should correctly apply a simulated delay with a specific seed', () => {
        // # Mock rationale: Seed 5 is chosen to reliably trigger a "Solar Flare Delay"
        // on the first edge encountered, allowing for deterministic testing of anomaly effects.
        setRandomSeed(5); // This seed should trigger a delay on some early path
        const { path, totalTime } = findCosmicCommute("Earth_Orbital_Hub", "Mars_Outpost");
        assert.ok(path.length > 0);
        const directEdge = graph.edges.find(e => e[0] === "Earth_Orbital_Hub" && e[1] === "Mars_Outpost");
        const baseTime = directEdge ? directEdge[2] : Infinity;

        // Verify if a delay was applied and time is greater than base
        const segment = path.find(s => s.from === "Earth_Orbital_Hub" && s.to === "Mars_Outpost");
        if (segment) {
            assert.ok(segment.anomaly === "Solar Flare Delay" || segment.anomaly === "Clear Skies", "Expected delay or clear skies");
            if (segment.anomaly === "Solar Flare Delay") {
                assert.ok(segment.time > baseTime, `Simulated time ${segment.time} should be greater than base time ${baseTime}`);
            } else {
                assert.strictEqual(segment.time, baseTime);
            }
        }
    });
});
