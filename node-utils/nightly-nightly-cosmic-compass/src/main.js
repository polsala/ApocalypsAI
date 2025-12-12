const moment = require('moment');

// Simple pseudo-random number generator seeded by time
class SeededRandom {
    constructor(seed) {
        this.seed = seed;
    }

    next() {
        this.seed = (this.seed * 9301 + 49297) % 233280;
        return this.seed / 233280.0;
    }
}

function formatRA(decimal) {
    const hours = Math.floor(decimal * 24);
    const minutesDecimal = (decimal * 24 - hours) * 60;
    const minutes = Math.floor(minutesDecimal);
    const secondsDecimal = (minutesDecimal - minutes) * 60;
    const seconds = secondsDecimal.toFixed(1);
    return `${hours}h ${minutes}m ${seconds}s`;
}

function formatDec(decimal) {
    const degrees = Math.floor(decimal * 180) - 90;
    const minutesDecimal = Math.abs((decimal * 180 - 90) - degrees) * 60;
    const minutes = Math.floor(minutesDecimal);
    const secondsDecimal = (minutesDecimal - minutes) * 60;
    const seconds = secondsDecimal.toFixed(1);
    const sign = degrees >= 0 ? '+' : '-';
    return `${sign}${Math.abs(degrees)}° ${minutes}' ${seconds}\"`;
}

const constellations = [
    "The Glimmering Quill",
    "The Whispering Nebula",
    "The Celestial Serpent",
    "The Wandering Comet",
    "The Starfall Bloom",
    "The Aurora Weaver",
    "The Cosmic Harp",
    "The Lunar Moth",
    "The Sunstone Phoenix",
    "The Void Blossom"
];

const epochs = [
    "Stardust Era",
    "Nebula Dawn",
    "Galactic Twilight",
    "Cosmic Bloom",
    "Quantum Epoch",
    "Stellar Drift",
    "Astral Age",
    "Event Horizon Era",
    "Singularity Spring",
    "Chronos Cycle"
];

function generateCosmicCoordinates() {
    const now = moment();
    const seed = now.valueOf(); // Use timestamp as seed
    const rng = new SeededRandom(seed);

    // Generate values between 0 and 1
    const raDecimal = rng.next();
    const decDecimal = rng.next();

    // Map to celestial coordinate ranges
    const formattedRA = formatRA(raDecimal);
    const formattedDec = formatDec(decDecimal);

    // Select a random epoch and constellation
    const epochIndex = Math.floor(rng.next() * epochs.length);
    const constellationIndex = Math.floor(rng.next() * constellations.length);

    return {
        RA: formattedRA,
        Dec: formattedDec,
        Epoch: epochs[epochIndex],
        Constellation: constellations[constellationIndex]
    };
}

console.log(JSON.stringify(generateCosmicCoordinates(), null, 2));
