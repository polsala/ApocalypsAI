const fs = require('fs');
const path = require('path');

function applyDecay(text, decayRate = 0.05, randomFn = Math.random) {
    let decayedText = '';
    const corruptionChars = '!@#$%^&*()_+{}[]|\\;:\'",.<>/?`~';
    for (let i = 0; i < text.length; i++) {
        const char = text[i];
        if (randomFn() < decayRate) {
            const decayType = Math.floor(randomFn() * 3); // 0: replace, 1: delete, 2: insert
            if (decayType === 0) {
                // Replace with a random corruption char
                decayedText += corruptionChars[Math.floor(randomFn() * corruptionChars.length)];
            } else if (decayType === 1) {
                // Delete character (do nothing)
            } else {
                // Insert a random corruption char before current char
                decayedText += corruptionChars[Math.floor(randomFn() * corruptionChars.length)];
                decayedText += char;
            }
        } else {
            decayedText += char;
        }
    }
    return decayedText;
}

async function decayFile(filePath, iterations = 1, decayRate = 0.05, outputPath = null) {
    let content;
    try {
        content = await fs.promises.readFile(filePath, 'utf8');
    } catch (error) {
        console.error(`Error reading file ${filePath}: ${error.message}`);
        process.exit(1);
    }

    let currentContent = content;
    for (let i = 0; i < iterations; i++) {
        currentContent = applyDecay(currentContent, decayRate);
    }

    if (outputPath) {
        try {
            await fs.promises.writeFile(outputPath, currentContent, 'utf8');
            console.log(`Decayed content written to ${outputPath}`);
        } catch (error) {
            console.error(`Error writing to file ${outputPath}: ${error.message}`);
            process.exit(1);
        }
    } else {
        console.log(currentContent);
    }
}

// CLI entry point
if (require.main === module) {
    const args = process.argv.slice(2);
    const filePath = args[0];
    const iterations = parseInt(args[1]) || 1;
    const decayRate = parseFloat(args[2]) || 0.05;
    const outputPath = args[3] || null;

    if (!filePath) {
        console.log('Usage: node src/index.js <filePath> [iterations] [decayRate] [outputPath]');
        console.log('  <filePath>   : Path to the text file to decay.');
        console.log('  [iterations] : Number of decay passes (default: 1).');
        console.log('  [decayRate]  : Probability of a character decaying per pass (0.0-1.0, default: 0.05).');
        console.log('  [outputPath] : Optional path to save the decayed content. If omitted, prints to stdout.');
        process.exit(0);
    }

    decayFile(filePath, iterations, decayRate, outputPath);
}

module.exports = { applyDecay, decayFile };
