import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [moraleEntries, setMoraleEntries] = useState(() => {
    // Load from localStorage on initial render
    const savedEntries = localStorage.getItem('moraleEntries');
    return savedEntries ? JSON.parse(savedEntries) : [];
  });
  const [currentMorale, setCurrentMorale] = useState(5);
  const [currentFeedback, setCurrentFeedback] = useState('');

  // Save to localStorage whenever moraleEntries changes
  useEffect(() => {
    localStorage.setItem('moraleEntries', JSON.stringify(moraleEntries));
  }, [moraleEntries]);

  const generateFeedback = (level) => {
    if (level <= 2) {
      return "The void whispers despair, but even a void has echoes of hope. Hang in there, survivor!";
    } else if (level <= 4) {
      return "A bit dusty today, eh? Remember, even rust can be polished into a weapon.";
    } else if (level <= 6) {
      return "Steady as a mutant cockroach! Keep scuttling forward, friend.";
    } else if (level <= 8) {
      return "Feeling spry! Did you find a fresh can of pre-apocalypse peaches? Share the joy!";
    } else {
      return "Radiant as a supernova! Your morale could power a small settlement. Shine on, you crazy diamond!";
    }
  };

  const handleMoraleChange = (event) => {
    setCurrentMorale(parseInt(event.target.value, 10));
  };

  const logMorale = () => {
    const feedback = generateFeedback(currentMorale);
    const newEntry = {
      id: Date.now(), // Unique ID for key prop
      level: currentMorale,
      date: new Date().toLocaleString(),
      feedback: feedback,
    };
    setMoraleEntries((prevEntries) => [newEntry, ...prevEntries]);
    setCurrentFeedback(feedback);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Morale Meter</h1>
        <p>Gauge the community's spirit!</p>
      </header>
      <main>
        <section className="morale-input-section">
          <h2>How's your spirit today? ({currentMorale}/10)</h2>
          <input
            type="range"
            min="1"
            max="10"
            value={currentMorale}
            onChange={handleMoraleChange}
            className="morale-slider"
            aria-label="Morale Level"
          />
          <button onClick={logMorale} className="log-button">
            Log Morale
          </button>
          {currentFeedback && (
            <p className="current-feedback">{currentFeedback}</p>
          )}
        </section>

        <section className="morale-history-section">
          <h2>Morale History</h2>
          {moraleEntries.length === 0 ? (
            <p>No morale entries yet. Log your first one!</p>
          ) : (
            <ul className="morale-list">
              {moraleEntries.map((entry) => (
                <li key={entry.id} className="morale-item">
                  <span className="morale-level">Level: {entry.level}/10</span>
                  <span className="morale-date"> ({entry.date})</span>
                  <p className="morale-feedback">"{entry.feedback}"</p>
                </li>
              ))}
            </ul>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
