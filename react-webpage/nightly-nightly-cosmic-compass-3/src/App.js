import React, { useState, useEffect } from 'react';
import './App.css';

// Mock celestial event data for deterministic testing
const mockCelestialEvents = [
  {
    name: 'The Great Nebula Bloom',
    description: 'A spectacular unfurling of cosmic dust, painting the void with vibrant hues. Your alignment is... surprisingly harmonious!',
    alignmentScore: 85,
    visual: '🌸'
  },
  {
    name: 'The Comet's Whisper',
    description: 'A fleeting visitor, leaving trails of stardust and a subtle hum in the ether. You feel a gentle nudge from the universe.',
    alignmentScore: 72,
    visual: '☄️'
  },
  {
    name: 'The Binary Star Waltz',
    description: 'Two celestial bodies locked in an eternal dance, their gravitational pull creating ripples of energy. You are caught in a delightful cosmic pirouette!',
    alignmentScore: 91,
    visual: '💫'
  },
  {
    name: 'The Void's Embrace',
    description: 'A moment of profound stillness, where the vast emptiness offers a unique perspective. Embrace the quiet, your alignment is introspective.',
    alignmentScore: 60,
    visual: '🌌'
  },
  {
    name: 'The Supernova's Echo',
    description: 'A distant explosion, its light reaching you as a reminder of creation and destruction. Your alignment is... explosive!',
    alignmentScore: 78,
    visual: '💥'
  }
];

function App() {
  const [celestialEvent, setCelestialEvent] = useState(null);
  const [alignmentScore, setAlignmentScore] = useState(0);
  const [visual, setVisual] = useState('');

  useEffect(() => {
    // In a real app, this might fetch data. For this utility, we'll use mock data.
    // For deterministic testing, we'll use a fixed index or a seeded random.
    // Here, we'll use a simple modulo to cycle through mock events for consistency.
    const eventIndex = new Date().getDay() % mockCelestialEvents.length; // Use day of week for consistency
    const event = mockCelestialEvents[eventIndex];
    setCelestialEvent(event);
    setAlignmentScore(event.alignmentScore);
    setVisual(event.visual);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>The Cosmic Compass</h1>
        <p>Navigating the whimsical currents of the universe.</p>
      </header>
      <main>
        {celestialEvent ? (
          <div className="celestial-display">
            <h2>{celestialEvent.name}</h2>
            <div className="visual-element">{visual}</div>
            <p>{celestialEvent.description}</p>
            <div className="alignment-meter">
              <h3>Your Cosmic Alignment:</h3>
              <div className="meter-bar-container">
                <div 
                  className="meter-bar"
                  style={{ width: `${alignmentScore}%` }}
                ></div>
              </div>
              <p>{alignmentScore}%</p>
            </div>
          </div>
        ) : (
          <p>Loading cosmic energies...</p>
        )}
      </main>
      <footer>
        <p>&copy; 2023 ApocalypsAI - For entertainment purposes only.</p>
      </footer>
    </div>
  );
}

export default App;
