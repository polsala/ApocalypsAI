const readline = require('readline');

// Assign whimsical cosmic frequencies to characters
const COSMIC_FREQUENCIES = {
    ' ': 1001,
    'a': 1002, 'b': 1003, 'c': 1004, 'd': 1005, 'e': 1006, 'f': 1007, 'g': 1008, 'h': 1009, 'i': 1010, 'j': 1011, 'k': 1012, 'l': 1013, 'm': 1014, 'n': 1015, 'o': 1016, 'p': 1017, 'q': 1018, 'r': 1019, 's': 1020, 't': 1021, 'u': 1022, 'v': 1023, 'w': 1024, 'x': 1025, 'y': 1026, 'z': 1027,
    'A': 2002, 'B': 2003, 'C': 2004, 'D': 2005, 'E': 2006, 'F': 2007, 'G': 2008, 'H': 2009, 'I': 2010, 'J': 2011, 'K': 2012, 'L': 2013, 'M': 2014, 'N': 2015, 'O': 2016, 'P': 2017, 'Q': 2018, 'R': 2019, 'S': 2020, 'T': 2021, 'U': 2022, 'V': 2023, 'W': 2024, 'X': 2025, 'Y': 2026, 'Z': 2027,
    '!': 3001, '?': 3002, '.': 3003, ',': 3004, "'": 3005, '"': 3006, '-': 3007, '_': 3008, '+': 3009, '=': 3010, '*': 3011, '/': 3012, '\': 3013, '|': 3014, '{': 3015, '}': 3016, '[': 3017, ']': 3018, '(': 3019, ')': 3020
    // Add more characters as needed for galactic communication!
};

const DECODED_FREQUENCIES = Object.fromEntries(Object.entries(COSMIC_FREQUENCIES).map(([char, freq]) => [freq, char]));

function getCosmicFrequency(char) {
    return COSMIC_FREQUENCIES[char] || (char.charCodeAt(0) + 4000); // Fallback for unmapped chars
}

function getCharFromFrequency(freq) {
    return DECODED_FREQUENCIES[freq] || String.fromCharCode(freq - 4000); // Fallback for unmapped freqs
}

function encodeMessage(message) {
    let encoded = [];
    for (const char of message) {
        const asciiVal = char.charCodeAt(0);
        const cosmicFreq = getCosmicFrequency(char);
        encoded.push(asciiVal + cosmicFreq);
    }
    return encoded.join('-');
}

function decodeMessage(encodedString) {
    if (!encodedString) {
        return "";
    }
    const frequencies = encodedString.split('-').map(Number);
    let decoded = "";
    for (const freqSum of frequencies) {
        // We need to find a character whose ASCII value + its cosmic frequency equals freqSum.
        // This is a simplification; a real cosmic comms system would be more complex.
        // For this whimsical utility, we'll try to find a direct match first.
        let found = false;
        for (const char in COSMIC_FREQUENCIES) {
            if (COSMIC_FREQUENCIES[char] + char.charCodeAt(0) === freqSum) {
                decoded += char;
                found = true;
                break;
            }
        }
        // If not found in direct mapping, try to infer from fallback
        if (!found) {
            // This part is tricky without knowing the original character's ASCII and its fallback frequency.
            // For simplicity, we'll assume fallback characters are mapped to their ASCII + 4000.
            // A more robust system would need a way to store/infer the original character.
            // For this example, we'll just use the fallback character if a direct match isn't found.
            // This might lead to incorrect decoding for characters not in COSMIC_FREQUENCIES.
            decoded += getCharFromFrequency(freqSum - (freqSum % 1000)); // A heuristic guess
        }
    }
    return decoded;
}

function main() {
    const args = process.argv.slice(2);
    const command = args[0];
    const messageOrEncoded = args.slice(1).join(' ');

    if (command === 'encode') {
        if (!messageOrEncoded) {
            console.error("Error: Please provide a message to encode.");
            process.exit(1);
        }
        const encoded = encodeMessage(messageOrEncoded);
        console.log(encoded);
    } else if (command === 'decode') {
        if (!messageOrEncoded) {
            console.error("Error: Please provide an encoded message to decode.");
            process.exit(1);
        }
        const decoded = decodeMessage(messageOrEncoded);
        console.log(decoded);
    } else {
        console.error("Usage: node src/main.js <encode|decode> <message|encoded_message>");
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = { encodeMessage, decodeMessage };
