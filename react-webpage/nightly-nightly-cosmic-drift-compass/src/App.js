import React, { useState, useEffect } from 'react';
import './App.css';
import Compass from './Compass';

const celestialBodiesData = [
  { name: 'Whispering Nebula', icon: '🌌', baseAngle: 0 },
  { name: 'Glimmering Comet', icon: '☄️', baseAngle: 90 },
  { name: 'Silent Moon Fragment', icon: '🌕', baseAngle: 180 },
  { name: 'Wandering Star', icon: '✨', baseAngle: 270 },
];

const getAlignmentAdvice = (drift) => {
  const normalizedDrift = drift % 360;
  if (normalizedDrift >= 0 && normalizedDrift < 45) {
    return "The Whispering Nebula aligns. Seek quiet contemplation and hidden truths.";
  } else if (normalizedDrift >= 45 && normalizedDrift < 135) {
    return "The Glimmering Comet streaks. Embrace change and swift action.";
  } else if (normalizedDrift >= 135 && normalizedDrift < 225) {
    return "The Silent Moon Fragment beckons. Reflect on your past and nurture growth.";
  } else if (normalizedDrift >= 225 && normalizedDrift < 315) {
    return "The Wandering Star guides. Explore new paths and trust your instincts.";
  } else {
    return "All cosmic energies converge. A moment of profound balance and opportunity.";
  }
};

function App() {
  const [cosmicDrift, setCosmicDrift] = useState(0);
  const [alignmentAdvice, setAlignmentAdvice] = useState("");

  useEffect(() => {
    setAlignmentAdvice(getAlignmentAdvice(cosmicDrift));
  }, [cosmicDrift]);

  const advanceDrift = () => {
    setCosmicDrift(prevDrift => (prevDrift + 30) % 360); // Advance by 30 degrees, cycle at 360
  };

  const celestialBodies = celestialBodiesData.map(body => ({
    ...body,
    currentAngle: (body.baseAngle + cosmicDrift) % 360,
  }));

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Cosmic Drift Compass</h1>
        <p>Current Cosmic Drift: {cosmicDrift}°</p>
      </header>
      <main>
        <Compass celestialBodies={celestialBodies} />
        <div className="advice-section">
          <h2>Alignment Advice:</h2>
          <p className="advice-text">{alignmentAdvice}</p>
          <button onClick={advanceDrift} className="drift-button">
            Advance Cosmic Drift
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;
