const cosmicAlignments = [
    {
        name: "Stellar Winds",
        emoji: "🌬️",
        suggestions: [
            "Seek out a forgotten constellation in your local library's archives.",
            "Map out the secret pathways of your local park.",
            "Learn three new facts about a distant galaxy.",
            "Explore a new genre of music or art you've never considered.",
            "Trace the journey of a single cloud across the sky.",
            "Research the history of a celestial body.",
            "Discover a new recipe and try to cook it without looking at the instructions after the first read.",
            "Find a new perspective by observing your surroundings from an unusual height or angle."
        ]
    },
    {
        name: "Lunar Glow",
        emoji: "🌕",
        suggestions: [
            "Compose a haiku about the silence between stars.",
            "Meditate on the gentle ebb and flow of the tides.",
            "Write a letter to your future self, to be opened on the next full moon.",
            "Create a soothing playlist inspired by moonlight.",
            "Spend an hour in quiet contemplation, observing the night sky (or a candle flame).",
            "Practice a gentle art form, like sketching or knitting.",
            "Reflect on a past memory and find a new detail you hadn't noticed before.",
            "Indulge in a warm beverage and simply exist."
        ]
    },
    {
        name: "Solar Flare",
        emoji: "☀️",
        suggestions: [
            "Launch a bold new idea into the world, no matter how small.",
            "Tackle that one task you've been procrastinating with fiery determination.",
            "Organize a small, spontaneous gathering with friends.",
            "Start a new physical activity that gets your blood pumping.",
            "Brainstorm ten 'impossible' solutions to a current challenge.",
            "Shine a light on someone else's day with a genuine compliment or act of kindness.",
            "Take a brisk walk and let the sun energize your thoughts.",
            "Confront a small fear head-on, like making that difficult phone call."
        ]
    },
    {
        name: "Nebula's Embrace",
        emoji: "✨",
        suggestions: [
            "Draft a manifesto for a squirrel revolution.",
            "Paint a picture using only colors you've never combined before.",
            "Write a short story from the perspective of a sentient dust bunny.",
            "Invent a new constellation and its accompanying myth.",
            "Daydream for 30 minutes without any specific goal.",
            "Create a collage from discarded materials.",
            "Listen to a piece of instrumental music and imagine a story unfolding.",
            "Design a fantastical creature and describe its habitat."
        ]
    },
    {
        name: "Comet's Trail",
        emoji: "☄️",
        suggestions: [
            "Embark on a spontaneous quest for the perfect pebble.",
            "Rearrange a piece of furniture in your home for a fresh perspective.",
            "Take a different route to a familiar destination.",
            "Try a food you've never tasted before.",
            "Send a message to an old friend you haven't spoken to in ages.",
            "Learn a single word in a new language and use it today.",
            "Break a small routine in a surprising way.",
            "Go somewhere you've never been, even if it's just a different aisle in the grocery store."
        ]
    }
];

/**
 * Generates a deterministic cosmic index from a string.
 * @param {string} inputString
 * @returns {number}
 */
function getCosmicIndex(inputString) {
    let hash = 0;
    if (inputString.length === 0) return hash;
    for (let i = 0; i < inputString.length; i++) {
        const char = inputString.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash |= 0; // Convert to 32bit integer
    }
    return Math.abs(hash); // Ensure positive index
}

/**
 * Gets a cosmic suggestion based on the input string.
 * @param {string} input
 * @returns {string} The cosmic suggestion.
 */
function getSuggestion(input) {
    const inputString = input.trim().toLowerCase();
    if (!inputString) {
        // Default if no input, for determinism, use a fixed string
        return getSuggestion("default cosmic query");
    }

    const cosmicIndex = getCosmicIndex(inputString);

    const alignmentIndex = cosmicIndex % cosmicAlignments.length;
    const alignment = cosmicAlignments[alignmentIndex];

    const suggestionIndex = cosmicIndex % alignment.suggestions.length;
    const suggestion = alignment.suggestions[suggestionIndex];

    return `${alignment.emoji} The ${alignment.name} whispers: '${suggestion}'`;
}

module.exports = { getSuggestion, getCosmicIndex, cosmicAlignments };
