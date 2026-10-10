import React, { useState, useEffect } from 'react';
import './App.css';
import GlitchForm from './components/GlitchForm';
import GlitchList from './components/GlitchList';

function App() {
  const [glitches, setGlitches] = useState(() => {
    // Load glitches from local storage on initial render
    const savedGlitches = localStorage.getItem('glitches');
    return savedGlitches ? JSON.parse(savedGlitches) : [];
  });

  useEffect(() => {
    // Save glitches to local storage whenever they change
    localStorage.setItem('glitches', JSON.stringify(glitches));
  }, [glitches]);

  const addGlitch = (newGlitch) => {
    setGlitches((prevGlitches) => [
      { id: Date.now(), timestamp: new Date().toLocaleString(), ...newGlitch },
      ...prevGlitches, // Add new glitches to the top
    ]);
  };

  return (
    <div className="App">
      <h1>Nightly Reality Glitch Tracker</h1>
      <GlitchForm onAddGlitch={addGlitch} />
      <GlitchList glitches={glitches} />
    </div>
  );
}

export default App;
