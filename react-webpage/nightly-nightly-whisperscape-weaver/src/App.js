import React, { useState, useEffect } from 'react';
import './App.css';
import WhisperInput from './components/WhisperInput';
import WhisperscapeCanvas from './components/WhisperscapeCanvas';

function App() {
  const [whispers, setWhispers] = useState(() => {
    // # Mock rationale: Use localStorage for persistence.
    // In a real app, this would interact with a backend API.
    // For this standalone utility, local storage provides a simple, offline persistence mechanism.
    const savedWhispers = localStorage.getItem('whisperscape-whispers');
    return savedWhispers ? JSON.parse(savedWhispers) : [];
  });

  useEffect(() => {
    // # Mock rationale: Persist whispers to localStorage.
    // This simulates saving data without requiring a backend.
    localStorage.setItem('whisperscape-whispers', JSON.stringify(whispers));
  }, [whispers]);

  const addWhisper = (newWhisper) => {
    if (newWhisper.trim()) {
      setWhispers((prevWhispers) => [
        ...prevWhispers,
        { id: Date.now(), text: newWhisper.trim() },
      ]);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Whisperscape Weaver</h1>
        <p>Weave your thoughts into the collective consciousness.</p>
      </header>
      <main>
        <WhisperInput onAddWhisper={addWhisper} />
        <WhisperscapeCanvas whispers={whispers} />
      </main>
    </div>
  );
}

export default App;
