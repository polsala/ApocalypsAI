#!/usr/bin/env node

const { Command } = require('commander');

// # Mock rationale: Math.random is non-deterministic. We need a seeded PRNG for tests.
// This simple PRNG is used to ensure tests are reproducible.
class SeededRandom {
    constructor(seed) {
        this.seed = seed % 2147483647; // Ensure seed is within a reasonable range
        if (this.seed <= 0) this.seed += 2147483646;
    }

    next() {
        this.seed = (this.seed * 16807) % 2147483647;
        return (this.seed - 1) / 2147483646;
    }
}

let currentRandom = Math.random; // Default to Math.random

function setRandomSeed(seed) {
    if (seed !== undefined && seed !== null) {
        currentRandom = new SeededRandom(seed).next.bind(new SeededRandom(seed));
    } else {
        currentRandom = Math.random;
    }
}

// Graph definition
const graph = {
    nodes: [
        "Earth_Orbital_Hub",
        "Lunar_Refueling_Station",
        "Mars_Outpost",
        "Jupiter_Mining_Colony",
        "Saturn_Ring_Resort",
        "Alpha_Centauri_Gateway",
        "Orion_Nebula_Observatory",
        "Andromeda_Nexus"
    ],
    edges: [
        // [from, to, base_travel_time]
        ["Earth_Orbital_Hub", "Lunar_Refueling_Station", 5],
        ["Earth_Orbital_Hub", "Mars_Outpost", 15],
        ["Lunar_Refueling_Station", "Mars_Outpost", 12],
        ["Lunar_Refueling_Station", "Jupiter_Mining_Colony", 30],
        ["Mars_Outpost", "Jupiter_Mining_Colony", 20],
        ["Mars_Outpost", "Alpha_Centauri_Gateway", 100],
        ["Jupiter_Mining_Colony", "Saturn_Ring_Resort", 10],
        ["Saturn_Ring_Resort", "Alpha_Centauri_Gateway", 90],
        ["Alpha_Centauri_Gateway", "Orion_Nebula_Observatory", 50],
        ["Orion_Nebula_Observatory", "Andromeda_Nexus", 200],
        ["Alpha_Centauri_Gateway", "Andromeda_Nexus", 250]
    ]
};

// Create adjacency list for easier graph traversal
const adjList = new Map();
graph.nodes.forEach(node => adjList.set(node, []));
graph.edges.forEach(([from, to, time]) => {
    adjList.get(from).push({ to, time });
    adjList.get(to).push({ to: from, time }); // Assuming bidirectional travel
});

// Anomaly simulation
function simulateAnomaly(baseTime) {
    const anomalyRoll = currentRandom();
    if (anomalyRoll < 0.15) { // 15% chance of a delay
        const delayFactor = 1 + currentRandom() * 0.5; // 0% to 50% delay
        return { time: baseTime * delayFactor, description: "Solar Flare Delay" };
    } else if (anomalyRoll < 0.30) { // 15% chance of a boost
        const boostFactor = 1 - currentRandom() * 0.3; // 0% to 30% speed boost
        return { time: baseTime * boostFactor, description: "Gravity Assist Boost" };
    }
    return { time: baseTime, description: "Clear Skies" }; // 70% chance of no anomaly
}

// Dijkstra's algorithm for shortest path
function findCosmicCommute(startNode, endNode) {
    if (!adjList.has(startNode) || !adjList.has(endNode)) {
        return { path: [], totalTime: Infinity, error: "Invalid start or end waypoint." };
    }

    const distances = new Map();
    const previous = new Map();
    const anomalyLog = new Map(); // To store anomaly descriptions for each edge in the path
    const pq = []; // Priority queue: [distance, node, path_so_far]

    graph.nodes.forEach(node => distances.set(node, Infinity));
    distances.set(startNode, 0);
    pq.push({ distance: 0, node: startNode, path: [] });

    while (pq.length > 0) {
        pq.sort((a, b) => a.distance - b.distance); // Simple sort for priority queue
        const { distance: currentDistance, node: currentNode, path: currentPath } = pq.shift();

        if (currentNode === endNode) {
            const fullPath = [startNode, ...currentPath.map(p => p.node)];
            const detailedPath = [];
            for (let i = 0; i < fullPath.length - 1; i++) {
                const from = fullPath[i];
                const to = fullPath[i+1];
                const edgeKey = `${from}-${to}`;
                detailedPath.push({ from, to, ...anomalyLog.get(edgeKey) });
            }
            return { path: detailedPath, totalTime: currentDistance };
        }

        if (currentDistance > distances.get(currentNode)) {
            continue;
        }

        for (const neighbor of adjList.get(currentNode)) {
            const { to: neighborNode, time: baseTime } = neighbor;
            const { time: simulatedTime, description: anomalyDescription } = simulateAnomaly(baseTime);
            const newDistance = currentDistance + simulatedTime;

            if (newDistance < distances.get(neighborNode)) {
                distances.set(neighborNode, newDistance);
                previous.set(neighborNode, currentNode);
                const edgeKey = `${currentNode}-${neighborNode}`;
                anomalyLog.set(edgeKey, { time: simulatedTime, anomaly: anomalyDescription });
                pq.push({ distance: newDistance, node: neighborNode, path: [...currentPath, { node: neighborNode, time: simulatedTime, anomaly: anomalyDescription }] });
            }
        }
    }

    return { path: [], totalTime: Infinity, error: "No path found." };
}

// CLI setup
const program = new Command();

program
    .name('nightly-cosmic-commute-plan')
    .description('A whimsical CLI utility to plan cosmic commutes.')
    .version('1.0.0')
    .argument('<start_waypoint>', 'The starting celestial waypoint')
    .argument('<end_waypoint>', 'The destination celestial waypoint')
    .option('--seed <number>', 'A numeric seed for the random anomaly generator', parseInt)
    .action((startWaypoint, endWaypoint, options) => {
        setRandomSeed(options.seed);

        console.log(`\n🌌 Planning your cosmic commute from ${startWaypoint} to ${endWaypoint}...`);
        if (options.seed) {
            console.log(`(Using anomaly seed: ${options.seed})`);
        }

        const { path, totalTime, error } = findCosmicCommute(startWaypoint, endWaypoint);

        if (error) {
            console.error(`\n🚨 Error: ${error}`);
            console.log(`Available waypoints: ${graph.nodes.join(', ')}`);
            process.exit(1);
        }

        if (totalTime === Infinity) {
            console.log(`\n🚫 No cosmic route found from ${startWaypoint} to ${endWaypoint}.`);
            process.exit(1);
        }

        console.log('\n✨ Optimal Cosmic Route:');
        path.forEach((segment, index) => {
            console.log(`  ${index + 1}. From ${segment.from} to ${segment.to}: ${segment.time.toFixed(2)} units (${segment.anomaly})`);
        });
        console.log(`\n🚀 Total Estimated Travel Time: ${totalTime.toFixed(2)} units`);
        console.log('\nMay your journey be swift and full of wonder!');
    });

// Export for testing
module.exports = {
    findCosmicCommute,
    setRandomSeed,
    graph,
    adjList, // Export adjList for direct manipulation in tests
    SeededRandom // Export for direct testing of the PRNG if needed
};

if (require.main === module) {
    program.parse(process.argv);
}
