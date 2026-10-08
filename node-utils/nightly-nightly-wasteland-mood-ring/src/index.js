#!/usr/bin/env node

const readline = require('readline');

const moods = {
    "gloomy": {
        description: "The air hangs heavy, like forgotten memories. A time for introspection.",
        suggestion: "Seek shelter in the ruins of old libraries. Perhaps a forgotten tome holds a clue, or at least a dry place to nap."
    },
    "energetic": {
        description: "A restless wind whips through the dust, urging action and exploration.",
        suggestion: "Today is for scavenging! Head towards the shimmering mirage on the horizon. It might be water, or just a very shiny rock."
    },
    "mysterious": {
        description: "Shadows lengthen, and strange whispers echo from unseen places. Curiosity beckons.",
        suggestion: "Follow the faint, glowing fungi. They often lead to hidden caches... or sentient puddles. Either way, an adventure!"
    },
    "calm": {
        description: "A rare tranquility settles over the desolation. A moment for peace.",
        suggestion: "Find a sturdy, un-mutated tree. Sit beneath it, listen to the silence, and contemplate the existential dread of a squirrel."
    },
    "chaotic": {
        description: "The very fabric of reality seems to shimmer and shift. Expect the unexpected.",
        suggestion: "Don your most mismatched socks and prepare for spontaneous teleportation. Or, you know, just stay put and watch the sky for falling toasters."
    },
    "hopeful": {
        description: "A faint glimmer pierces the perpetual twilight. A chance for renewal.",
        suggestion: "Plant a seed! Even if it's just a mutated potato, the act of creation is a rebellion against the void."
    }
};

function classifyInput(input) {
    const lowerInput = input.toLowerCase();
    if (lowerInput.includes('rain') || lowerInput.includes('sad') || lowerInput.includes('dark') || lowerInput.includes('grey')) return 'gloomy';
    if (lowerInput.includes('sun') || lowerInput.includes('run') || lowerInput.includes('bright') || lowerInput.includes('active')) return 'energetic';
    if (lowerInput.includes('secret') || lowerInput.includes('unknown') || lowerInput.includes('whisper') || lowerInput.includes('strange')) return 'mysterious';
    if (lowerInput.includes('peace') || lowerInput.includes('quiet') || lowerInput.includes('still') || lowerInput.includes('serene')) return 'calm';
    if (lowerInput.includes('chaos') || lowerInput.includes('wild') || lowerInput.includes('crazy') || lowerInput.includes('unpredictable')) return 'chaotic';
    if (lowerInput.includes('light') || lowerInput.includes('future') || lowerInput.includes('grow') || lowerInput.includes('optimistic')) return 'hopeful';
    
    // Fallback to a simple hash-based selection for more variety and determinism for unclassified inputs
    let hash = 0;
    for (let i = 0; i < lowerInput.length; i++) {
        hash = lowerInput.charCodeAt(i) + ((hash << 5) - hash); // Simple string hash
    }
    const moodKeys = Object.keys(moods);
    return moodKeys[Math.abs(hash) % moodKeys.length];
}

function getRandomMoodKey() {
    const moodKeys = Object.keys(moods);
    return moodKeys[Math.floor(Math.random() * moodKeys.length)];
}

async function run(argv = process.argv, readlineInterface = readline) {
    let inputPhrase = argv.slice(2).join(' ').trim();

    if (!inputPhrase) {
        const rl = readlineInterface.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        inputPhrase = await new Promise(resolve => {
            rl.question('What\'s the wasteland whispering to you today? (Press Enter for a random mood) ', answer => {
                rl.close();
                resolve(answer.trim());
            });
        });
    }

    const selectedMoodKey = inputPhrase ? classifyInput(inputPhrase) : getRandomMoodKey();
    const selectedMood = moods[selectedMoodKey];

    console.log(`\n--- The Wasteland's Mood Ring ---`);
    console.log(`Mood: ${selectedMoodKey.charAt(0).toUpperCase() + selectedMoodKey.slice(1)}`);
    console.log(`Description: ${selectedMood.description}`);
    console.log(`Suggestion: ${selectedMood.suggestion}`);
    console.log(`---------------------------------\n`);
}

// Export for testing
module.exports = {
    classifyInput,
    getRandomMoodKey,
    moods,
    run
};

if (require.main === module) {
    run();
}
