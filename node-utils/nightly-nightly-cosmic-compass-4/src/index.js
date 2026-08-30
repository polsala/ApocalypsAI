#!/usr/bin/env node

const readline = require('readline');

const starNames = [
    "Nebula Prime", "Quasar Nexus", "Pulsar Point", "Galaxy Gate", "Comet Cluster",
    "Asteroid Belt Alpha", "Stardust Sanctuary", "Cosmic Crossroads", "Void Vista", "Celestial Spire",
    "Orion's Belt Buckle", "Andromeda's Whisper", "Milky Way Marvel", "Supernova Station", "Black Hole Bistro"
];

const starTypes = [
    "Blue Giant", "Red Dwarf", "Yellow Sun", "White Dwarf", "Neutron Star",
    "Brown Dwarf", "Protostar", "Binary System", "Trinary System", "Dwarf Star"
];

function getRandomElement(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function generateCoordinate() {
    // Generates coordinates between -1000 and 1000, with 2 decimal places
    const coord = (Math.random() * 2000 - 1000).toFixed(2);
    return parseFloat(coord); // Ensure it's a number for potential future calculations
}

function generateCosmicCompass() {
    const starName = getRandomElement(starNames);
    const galacticX = generateCoordinate();
    const galacticY = generateCoordinate();
    const galacticZ = generateCoordinate();
    const starType = getRandomElement(starTypes);

    return {
        starName,
        galacticCoordinates: {
            X: galacticX,
            Y: galacticY,
            Z: galacticZ
        },
        starType
    };
}

function displayCompass(compassData) {
    console.log(`Star System: ${compassData.starName}`);
    console.log(`Galactic Coordinates: X: ${compassData.galacticCoordinates.X}, Y: ${compassData.galacticCoordinates.Y}, Z: ${compassData.galacticCoordinates.Z}`);
    console.log(`Star Type: ${compassData.starType}`);
}

if (require.main === module) {
    const compassData = generateCosmicCompass();
    displayCompass(compassData);
}

module.exports = { generateCosmicCompass, displayCompass };
