import React, { useState } from 'react';
import EchoDisplay from './components/EchoDisplay.jsx';

// Mock rationale: This function provides deterministic echo generation for consistent testing
// and predictable behavior based on the input 'anchor' string, avoiding true randomness.
const generateDeterministicEchoes = (anchor) => {
  const echoes = [];
  // Simple seed based on string properties for determinism
  const seed = anchor.length + (anchor.charCodeAt(0) || 0) + (anchor.charCodeAt(anchor.length - 1) || 0);

  const pastWhispers = [
    "A faint memory of plentiful harvests.",
    "The distant clang of pre-collapse industry.",
    "Whispers of forgotten technologies.",
    "The warmth of a sun that used to shine brighter.",
    "Echoes of laughter from a time before.",
    "The taste of clean water, long forgotten.",
    "A vision of bustling markets, now silent."
  ];
  const futureRipples = [
    "A shimmer of hope, or a mirage?",
    "The faint scent of rain on parched earth.",
    "A warning of shifting sands.",
    "The promise of a new dawn, or a deeper night?",
    "A distant hum of unknown machinery.",
    "The shadow of a coming storm.",
    "A fleeting glimpse of a safer haven."
  ];

  // Select echoes deterministically
  echoes.push({
    id: `past-${seed % pastWhispers.length}`,
    type: "Past Whisper",
    content: pastWhispers[seed % pastWhispers.length],
    intensity: (seed % 5) + 1,
    color: '#88aaff'
  });
  echoes.push({
    id: `future-${(seed + 1) % futureRipples.length}`,
    type: "Future Ripple",
    content: futureRipples[(seed + 1) % futureRipples.length],
    intensity: (seed % 5) + 3,
    color: '#ffaa88'
  });
  echoes.push({
    id: `distortion-${seed}`,
    type: "Distortion Index",
    content: `${(seed * 0.123).toFixed(2)} units of temporal flux.`, // More descriptive
    intensity: (seed % 10) + 1,
    color: '#aaff88'
  });

  return echoes;
};

function App() {
  const [temporalAnchor, setTemporalAnchor] = useState('');
  const [echoes, setEchoes] = useState([]);

  const handleGenerate = () => {
    if (temporalAnchor.trim() === '') {
      setEchoes([]);
      return;
    }
    setEchoes(generateDeterministicEchoes(temporalAnchor));
  };

  return (
    <div className="App">
      <h1>Temporal Echo Visualizer</h1>
      <div className="input-section">
        <input
          type="text"
          placeholder="Enter Temporal Anchor (e.g., 'The Great Silence')"
          value={temporalAnchor}
          onChange={(e) => setTemporalAnchor(e.target.value)}
          aria-label="Temporal Anchor Input"
        />
        <button onClick={handleGenerate}>Generate Echoes</button>
      </div>
      <div className="echo-container">
        {echoes.length === 0 && temporalAnchor.trim() !== '' && (
          <p className="no-echoes">No echoes detected for this anchor. Try another!</p>
        )}
        {echoes.map((echo) => (
          <EchoDisplay key={echo.id} echo={echo} />
        ))}
      </div>
    </div>
  );
}

export default App;
