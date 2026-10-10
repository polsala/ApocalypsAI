import React from 'react';

function ResonanceDisplay({ overallResonance }) {
  const getResonanceMessage = (score) => {
    const numScore = parseFloat(score);
    if (numScore === 0) return "The temporal fabric is calm.";
    if (numScore < 3) return "Faint ripples in the temporal stream.";
    if (numScore < 6) return "Moderate temporal vibrations detected.";
    if (numScore < 8) return "Strong temporal currents are active!";
    return "The temporal echo chamber is buzzing with energy!";
  };

  return (
    <div className="resonance-display">
      <h2>Overall Temporal Resonance</h2>
      <p>
        Current Score: <span className="resonance-score">{overallResonance}</span>
      </p>
      <p>{getResonanceMessage(overallResonance)}</p>
    </div>
  );
}

export default ResonanceDisplay;
