import React, { useState, useEffect } from 'react';
import './App.css';

const ARTIFACTS = [
  { threshold: 10, name: 'Glimmering Shard', description: 'A tiny piece of a forgotten star.' },
  { threshold: 50, name: 'Nebula Whisper', description: 'The faint echo of a cosmic cloud.' },
  { threshold: 100, name: 'Stardust Bloom', description: 'A flower born from celestial particles.' },
  { threshold: 250, name: 'Void Compass', description: 'Points to the next great discovery.' },
  { threshold: 500, name: 'Galactic Core Fragment', description: 'A dense, ancient relic of creation.' }
];

function App() {
  const [dustCount, setDustCount] = useState(() => {
    // Initialize from localStorage
    const savedDust = localStorage.getItem('cosmicDustCount');
    return savedDust ? parseInt(savedDust, 10) : 0;
  });
  const [unlockedArtifacts, setUnlockedArtifacts] = useState(() => {
    const savedArtifacts = localStorage.getItem('unlockedCosmicArtifacts');
    return savedArtifacts ? JSON.parse(savedArtifacts) : [];
  });

  useEffect(() => {
    localStorage.setItem('cosmicDustCount', dustCount.toString());
  }, [dustCount]);

  useEffect(() => {
    localStorage.setItem('unlockedCosmicArtifacts', JSON.stringify(unlockedArtifacts));
  }, [unlockedArtifacts]);

  const collectDust = () => {
    setDustCount(prevCount => {
      const newCount = prevCount + 1;
      // Check for new artifacts
      ARTIFACTS.forEach(artifact => {
        if (newCount >= artifact.threshold && !unlockedArtifacts.some(a => a.name === artifact.name)) {
          setUnlockedArtifacts(prevArtifacts => [...prevArtifacts, artifact]);
          alert(`New Cosmic Artifact Unlocked: ${artifact.name}!\n${artifact.description}`);
        }
      });
      return newCount;
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Cosmic Dust Collector</h1>
        <p className="dust-count">Cosmic Dust Collected: <span>{dustCount}</span></p>
        <button className="collect-button" onClick={collectDust}>
          Collect Cosmic Dust
        </button>

        {unlockedArtifacts.length > 0 && (
          <div className="artifacts-section">
            <h2>Discovered Artifacts</h2>
            <ul className="artifact-list">
              {unlockedArtifacts.map((artifact, index) => (
                <li key={index} className="artifact-item">
                  <strong>{artifact.name}</strong>: {artifact.description}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="stars-background">
          {[...Array(50)].map((_, i) => (
            <div
              key={i}
              className="star"
              style={{
                top: `${Math.random() * 100}%`,
                left: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
                animationDuration: `${2 + Math.random() * 3}s`
              }}
            ></div>
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;
