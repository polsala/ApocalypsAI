import React, { useState, useEffect } from 'react';
import './styles/App.css';
import DustBunnyCollector from './components/DustBunnyCollector';
import DustBunnyDisplay from './components/DustBunnyDisplay';

function App() {
  const [dustBunnies, setDustBunnies] = useState(() => {
    // Load from local storage on initial render
    const savedBunnies = localStorage.getItem('cosmicDustBunnies');
    return savedBunnies ? JSON.parse(savedBunnies) : [];
  });

  useEffect(() => {
    // Save to local storage whenever dustBunnies changes
    localStorage.setItem('cosmicDustBunnies', JSON.stringify(dustBunnies));
  }, [dustBunnies]);

  const addDustBunny = (description) => {
    if (description.trim()) {
      const newBunny = {
        id: Date.now(), // Simple unique ID
        description: description.trim(),
        collectedAt: new Date().toISOString(),
      };
      setDustBunnies((prevBunnies) => [...prevBunnies, newBunny]);
    }
  };

  const clearAllDustBunnies = () => {
    setDustBunnies([]);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌌 Cosmic Dust Bunny Collector 🌌</h1>
        <p>Gather your fleeting thoughts and tiny tasks!</p>
      </header>
      <main>
        <DustBunnyCollector onAddBunny={addDustBunny} />
        <button className="clear-button" onClick={clearAllDustBunnies}>
          Sweep Away All Dust Bunnies
        </button>
        <DustBunnyDisplay dustBunnies={dustBunnies} />
      </main>
      <footer>
        <p>&copy; ApocalypsAI Integrator Agent</p>
      </footer>
    </div>
  );
}

export default App;
