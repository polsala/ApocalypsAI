import React, { useState, useEffect, useCallback } from 'react';
import ChronoBloom from './ChronoBloom';

function App() {
  const [blooms, setBlooms] = useState([]);
  const [newBloomName, setNewBloomName] = useState('');
  const [newBloomDuration, setNewBloomDuration] = useState(30); // in minutes

  // Effect to update bloom progress every second
  useEffect(() => {
    const interval = setInterval(() => {
      setBlooms(currentBlooms =>
        currentBlooms.map(bloom => ({
          ...bloom,
          progress: Math.min(100, ((Date.now() - bloom.startTime) / (bloom.duration * 60 * 1000)) * 100)
        }))
      );
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const addBloom = useCallback(() => {
    if (newBloomName.trim() && newBloomDuration > 0) {
      const newBloom = {
        id: Date.now(),
        name: newBloomName.trim(),
        startTime: Date.now(),
        duration: newBloomDuration, // in minutes
        color: `hsl(${Math.floor(Math.random() * 360)}, 70%, 60%)`, // Random vibrant color
        progress: 0
      };
      setBlooms(prevBlooms => [...prevBlooms, newBloom]);
      setNewBloomName('');
      setNewBloomDuration(30);
    }
  }, [newBloomName, newBloomDuration]);

  const deleteBloom = useCallback((id) => {
    setBlooms(prevBlooms => prevBlooms.filter(bloom => bloom.id !== id));
  }, []);

  const handleKeyPress = useCallback((event) => {
    if (event.key === 'Enter') {
      addBloom();
    }
  }, [addBloom]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chrono-Bloom Cultivator</h1>
        <p>Plant digital blooms to track your time and tasks.</p>
      </header>

      <div className="bloom-input-section">
        <input
          type="text"
          placeholder="Bloom Name (e.g., 'Scavenge Sector 7')"
          value={newBloomName}
          onChange={(e) => setNewBloomName(e.target.value)}
          onKeyPress={handleKeyPress}
          aria-label="Bloom Name"
        />
        <input
          type="number"
          placeholder="Duration (minutes)"
          value={newBloomDuration}
          onChange={(e) => setNewBloomDuration(Math.max(1, parseInt(e.target.value) || 1))}
          onKeyPress={handleKeyPress}
          min="1"
          aria-label="Duration in minutes"
        />
        <button onClick={addBloom}>Plant Bloom</button>
      </div>

      <div className="blooms-container">
        {blooms.length === 0 ? (
          <p className="no-blooms-message">No blooms planted yet. Start cultivating!</p>
        ) : (
          blooms.map(bloom => (
            <ChronoBloom
              key={bloom.id}
              id={bloom.id}
              name={bloom.name}
              startTime={bloom.startTime}
              duration={bloom.duration}
              color={bloom.color}
              progress={bloom.progress}
              onDelete={deleteBloom}
            />
          ))
        )}
      </div>
    </div>
  );
}

export default App;
