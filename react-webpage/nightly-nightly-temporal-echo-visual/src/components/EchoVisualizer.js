import React from 'react';
import './EchoVisualizer.css';

const characterReplacements = {
  'a': ['á', 'à', 'ä', 'â'], 'e': ['é', 'è', 'ë', 'ê'], 'i': ['í', 'ì', 'ï', 'î'],
  'o': ['ó', 'ò', 'ö', 'ô'], 'u': ['ú', 'ù', 'ü', 'û'], 's': ['§', '$', 'š'],
  't': ['†', '‡'], 'l': ['£', 'ł'], 'c': ['ç', '©'], 'n': ['ñ'],
  ' ': [' ', '​'] // Non-breaking space, zero-width space
};

function EchoVisualizer({ text, distortionLevel }) {
  if (!text) {
    return <p className="echo-text">No text to visualize.</p>;
  }

  const characters = text.split('');

  return (
    <div className="echo-visualizer">
      <p className="echo-text">
        {characters.map((char, index) => {
          const randomSeed = (index * 0.12345 + distortionLevel * 0.6789) % 1; // Deterministic pseudo-random
          const distortionFactor = randomSeed * distortionLevel;

          const style = {
            '--hue-shift': `${distortionFactor * 60}deg`, // Shift hue up to 60 degrees
            '--translate-x': `${distortionFactor * 4}px`, // Shift X up to 4px
            '--translate-y': `${distortionFactor * 4}px`, // Shift Y up to 4px
            '--scale': `${1 + distortionFactor * 0.1}`, // Scale up to 10%
            '--opacity': `${1 - distortionFactor * 0.3}`, // Reduce opacity up to 30%
            '--blur': `${distortionFactor * 1}px`, // Blur up to 1px
            '--letter-spacing': `${distortionFactor * 0.5}px` // Adjust letter spacing
          };

          let displayChar = char;
          if (distortionFactor > 0.7 && characterReplacements[char.toLowerCase()]) {
            const replacements = characterReplacements[char.toLowerCase()];
            const replacementIndex = Math.floor(randomSeed * replacements.length);
            displayChar = replacements[replacementIndex];
          }

          return (
            <span
              key={index}
              className="echo-char"
              style={style}
            >
              {displayChar}
            </span>
          );
        })}
      </p>
    </div>
  );
}

export default EchoVisualizer;
