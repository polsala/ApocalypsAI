import React from 'react';
import './WhimsyMeter.css';

function WhimsyMeter({ score }) {
  const getCrystalColor = (s) => {
    if (s > 80) return 'linear-gradient(45deg, #ff00ff, #00ffff)'; // High whimsy: vibrant, chaotic
    if (s > 60) return 'linear-gradient(45deg, #ff66cc, #66ffcc)'; // Good whimsy: playful
    if (s > 40) return 'linear-gradient(45deg, #ffcc00, #ccff00)'; // Moderate whimsy: curious
    if (s > 20) return 'linear-gradient(45deg, #ff9933, #99ff33)'; // Low whimsy: subdued
    return 'linear-gradient(45deg, #cccccc, #666666)';           // Very low whimsy: dull
  };

  const getCrystalGlow = (s) => {
    const glowIntensity = Math.min(s / 100, 1) * 10; // Max 10px glow
    return `0 0 ${glowIntensity}px ${glowIntensity / 2}px rgba(97, 218, 251, ${Math.min(s / 100, 0.8)})`;
  };

  return (
    <div className="whimsy-meter-container">
      <h2>Whimsy Score</h2>
      <div
        className="chaos-crystal"
        style={{
          background: getCrystalColor(score),
          boxShadow: getCrystalGlow(score)
        }}
        title={`Whimsy Score: ${score}`}
      >
        <span className="score-display">{score}</span>
      </div>
      <p className="whimsy-status">
        {score > 80 && "Chaos is beautifully organized!"}
        {score <= 80 && score > 60 && "A delightful hum of creativity."
        }
        {score <= 60 && score > 40 && "Curiosity is stirring the pot."
        }
        {score <= 40 && score > 20 && "A bit quiet, perhaps a nap?"
        }
        {score <= 20 && "The void whispers for more fun..."
        }
      </p>
    </div>
  );
}

export default WhimsyMeter;
