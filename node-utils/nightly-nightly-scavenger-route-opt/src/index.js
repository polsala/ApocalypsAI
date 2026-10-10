const fs = require('fs');
const path = require('path');

/**
 * Calculates the Euclidean distance between two points.
 * @param {{x: number, y: number}} p1 - The first point.
 * @param {{x: number, y: number}} p2 - The second point.
 * @returns {number} The distance between the two points.
 */
function calculateDistance(p1, p2) {
    return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
}

/**
 * Optimizes a scavenging route using a nearest-neighbor heuristic.
 * @param {{x: number, y: number, name?: string}} startPoint - The starting coordinates.
 * @param {Array<{name: string, x: number, y: number}>} resourceLocations - An array of resource locations.
 * @returns {{route: Array<{name: string, x: number, y: number}>, totalDistance: number}} The optimized route and total distance.
 */
function optimizeRoute(startPoint, resourceLocations) {
    let currentPoint = { ...startPoint, name: startPoint.name || 'Start' };
    let remainingLocations = [...resourceLocations];
    const optimizedRoute = [currentPoint];
    let totalDistance = 0;

    while (remainingLocations.length > 0) {
        let nearestLocation = null;
        let minDistance = Infinity;
        let nearestIndex = -1;

        for (let i = 0; i < remainingLocations.length; i++) {
            const distance = calculateDistance(currentPoint, remainingLocations[i]);
            if (distance < minDistance) {
                minDistance = distance;
                nearestLocation = remainingLocations[i];
                nearestIndex = i;
            }
        }

        if (nearestLocation) {
            optimizedRoute.push(nearestLocation);
            totalDistance += minDistance;
            currentPoint = nearestLocation;
            remainingLocations.splice(nearestIndex, 1);
        } else {
            // This case should ideally not be reached if remainingLocations is not empty
            break;
        }
    }

    return { route: optimizedRoute, totalDistance };
}

/**
 * Main function to parse CLI arguments and execute the route optimization.
 * @param {string[]} args - Command line arguments (excluding 'node' and script path).
 */
function main(args) {
    const startX = parseFloat(args[0]);
    const startY = parseFloat(args[1]);
    const resourceFilePath = args[2];

    if (isNaN(startX) || isNaN(startY) || !resourceFilePath) {
        console.error('Usage: node src/index.js <startX> <startY> <resourceFilePath>');
        console.error('Example: node src/index.js 10 20 ./resources.json');
        process.exit(1);
    }

    const startPoint = { x: startX, y: startY };
    let resourceLocations;

    try {
        const rawData = fs.readFileSync(path.resolve(resourceFilePath), 'utf8');
        resourceLocations = JSON.parse(rawData);
        if (!Array.isArray(resourceLocations) || !resourceLocations.every(loc => loc.name && typeof loc.x === 'number' && typeof loc.y === 'number')) {
            throw new Error('Resource file must be an array of objects with "name", "x", and "y" properties.');
        }
    } catch (error) {
        console.error(`Error reading or parsing resource file: ${error.message}`);
        process.exit(1);
    }

    const { route, totalDistance } = optimizeRoute(startPoint, resourceLocations);

    console.log('--- Optimized Scavenging Route ---');
    route.forEach((loc, index) => {
        console.log(`${index + 1}. ${loc.name} (${loc.x}, ${loc.y})`);
    });
    console.log(`Total estimated travel distance: ${totalDistance.toFixed(2)} units`);
}

// Export for testing purposes
module.exports = {
    calculateDistance,
    optimizeRoute,
    main
};

// Only run main if the script is executed directly
if (require.main === module) {
    main(process.argv.slice(2));
}
