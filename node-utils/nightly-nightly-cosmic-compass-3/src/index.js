const cosmicAlignments = [
    { name: "Stellar Core", emoji: "🌌", whisper: "Illumination: Shine a light on this path." },
    { name: "Nebula Veil", emoji: "✨", whisper: "Contemplation: Pause and ponder its cosmic dust." },
    { name: "Galactic Drift", emoji: "🌠", whisper: "Re-evaluation: The universe suggests a new trajectory." },
    { name: "Quantum Quirk", emoji: "🌀", whisper: "Expansion: Grow beyond its current orbit." },
    { name: "Event Horizon", emoji: "🕳️", whisper: "Compression: Condense its essence into a singularity." },
    { name: "Astral Echo", emoji: "🔊", whisper: "Resonance: Listen for its vibrational frequency." },
    { name: "Void Vortex", emoji: "🌪️", whisper: "Dispersion: Let it scatter and reform." },
    { name: "Celestial Bloom", emoji: "🌸", whisper: "Genesis: A new beginning awaits." }
];

function getRandomCosmicGuidance() {
    const index = Math.floor(Math.random() * cosmicAlignments.length);
    return cosmicAlignments[index];
}

function runCompass(items) {
    if (items.length === 0) {
        console.log("The cosmic compass needs items to guide. Provide tasks or ideas!");
        return;
    }

    items.forEach(item => {
        const guidance = getRandomCosmicGuidance();
        console.log(`${guidance.emoji} ${item}: Aligned with the ${guidance.name}. ${guidance.whisper}`);
    });
}

if (require.main === module) {
    const args = process.argv.slice(2);
    runCompass(args);
}

module.exports = { runCompass, getRandomCosmicGuidance, cosmicAlignments };
