const assert = require('assert');
const { getArgs, getHemisphere, findMostInfluentialAnomaly } = require('../src/index');
const fs = require('fs');
const path = require('path');

// Mock rationale: We need to control the cosmic anomalies data for deterministic tests.
// This mock data is a subset or replica of the actual cosmic_anomalies.json for testing purposes.
const mockAnomaliesData = JSON.stringify([
    {
        "id": "orions-belt",
        "name": "Orion's Belt",
        "description": "Mock Orion's Belt.",
        "hemisphere": ["Northern", "Equatorial"],
        "visibility_months": [10, 11, 12, 1, 2, 3],
        "influence_score": 80
    },
    {
        "id": "andromeda-galaxy",
        "name": "Andromeda Galaxy",
        "description": "Mock Andromeda Galaxy.",
        "hemisphere": ["Northern", "Equatorial"],
        "visibility_months": [8, 9, 10, 11, 12],
        "influence_score": 95
    },
    {
        "id": "southern-cross",
        "name": "Southern Cross",
        "description": "Mock Southern Cross.",
        "hemisphere": ["Southern", "Equatorial"],
        "visibility_months": [3, 4, 5, 6, 7],
        "influence_score": 75
    },
    {
        "id": "carina-nebula",
        "name": "Carina Nebula",
        "description": "Mock Carina Nebula.",
        "hemisphere": ["Southern"],
        "visibility_months": [1, 2, 3, 4, 5],
        "influence_score": 90
    },
    {
        "id": "lyra-constellation",
        "name": "Lyra Constellation",
        "description": "Mock Lyra Constellation.",
        "hemisphere": ["Northern", "Equatorial"],
        "visibility_months": [5, 6, 7, 8, 9],
        "influence_score": 70
    },
    {
        "id": "milky-way-core",
        "name": "Milky Way Galactic Core",
        "description": "Mock Milky Way Galactic Core.",
        "hemisphere": ["Southern", "Equatorial"],
        "visibility_months": [5, 6, 7, 8],
        "influence_score": 98
    }
]);

// Mock rationale: Intercept fs.readFileSync to provide mock data instead of actual file system access.
// This ensures tests are deterministic and do not rely on the presence or content of a physical file.
const originalReadFileSync = fs.readFileSync;
fs.readFileSync = (filePath, encoding) => {
    if (filePath.includes('cosmic_anomalies.json')) {
        return mockAnomaliesData;
    }
    return originalReadFileSync(filePath, encoding);
};

console.log('Running tests for Nightly Cosmic Compass...');

// Test getArgs function
(function testGetArgs() {
    const originalArgv = process.argv;
    process.argv = ['node', 'index.js', '--lat=40.7128', '--lon=-74.0060', '--date=2023-10-26'];
    const args = getArgs();
    assert.strictEqual(args.lat, '40.7128', 'getArgs should parse latitude correctly');
    assert.strictEqual(args.lon, '-74.0060', 'getArgs should parse longitude correctly');
    assert.strictEqual(args.date, '2023-10-26', 'getArgs should parse date correctly');
    process.argv = originalArgv; // Restore original argv
    console.log('✓ getArgs tests passed.');
})();

// Test getHemisphere function
(function testGetHemisphere() {
    assert.strictEqual(getHemisphere(50), 'Northern', '50N should be Northern');
    assert.strictEqual(getHemisphere(0), 'Equatorial', '0 should be Equatorial');
    assert.strictEqual(getHemisphere(-30), 'Southern', '-30S should be Southern');
    assert.strictEqual(getHemisphere(4), 'Equatorial', '4N should be Equatorial (buffer)');
    assert.strictEqual(getHemisphere(-4), 'Equatorial', '-4S should be Equatorial (buffer)');
    console.log('✓ getHemisphere tests passed.');
})();

// Test findMostInfluentialAnomaly function
(function testFindMostInfluentialAnomaly() {
    // Mock rationale: Control the date for deterministic visibility checks.

    // Test 1: Northern Hemisphere, October (Andromeda should be highest influence)
    let testDate = new Date('2023-10-15T12:00:00Z'); // October
    let anomaly = findMostInfluentialAnomaly(40, testDate);
    assert.strictEqual(anomaly.id, 'andromeda-galaxy', 'Andromeda should be most influential in Northern, Oct');

    // Test 2: Southern Hemisphere, May (Milky Way Core should be highest influence)
    testDate = new Date('2023-05-15T12:00:00Z'); // May
    anomaly = findMostInfluentialAnomaly(-30, testDate);
    assert.strictEqual(anomaly.id, 'milky-way-core', 'Milky Way Core should be most influential in Southern, May');

    // Test 3: Equatorial, December (Andromeda should be highest influence)
    testDate = new Date('2023-12-15T12:00:00Z'); // December
    anomaly = findMostInfluentialAnomaly(0, testDate);
    assert.strictEqual(anomaly.id, 'andromeda-galaxy', 'Andromeda should be most influential in Equatorial, Dec');

    // Test 4: Northern Hemisphere, July (Lyra should be highest influence)
    testDate = new Date('2023-07-15T12:00:00Z'); // July
    anomaly = findMostInfluentialAnomaly(40, testDate);
    assert.strictEqual(anomaly.id, 'lyra-constellation', 'Lyra should be most influential in Northern, July');

    // Test 5: No anomalies at all for a given month/hemisphere (e.g., far Southern, September)
    testDate = new Date('2023-09-15T12:00:00Z'); // September
    anomaly = findMostInfluentialAnomaly(-60, testDate); // Far Southern, September
    assert.strictEqual(anomaly, null, 'Should find no anomaly for far Southern in September');

    console.log('✓ findMostInfluentialAnomaly tests passed.');
})();

console.log('All tests completed.');

// Restore original fs.readFileSync to avoid affecting other modules if this script were part of a larger system.
fs.readFileSync = originalReadFileSync;
