import React, { useState, useEffect } from 'react';
import './App.css';
import EchoInput from './components/EchoInput';
import EchoVisualizer from './components/EchoVisualizer';
import { analyzeEchoes, defaultStopwords } from './utils/analyzer';

function App() {
  const [events, setEvents] = useState(() => {
    const savedEvents = localStorage.getItem('temporalEchoEvents');
    return savedEvents ? JSON.parse(savedEvents) : [];
  });
  const [echoes, setEchoes] = useState({});

  useEffect(() => {
    localStorage.setItem('temporalEchoEvents', JSON.stringify(events));
    setEchoes(analyzeEchoes(events, defaultStopwords));
  }, [events]);

  const addEvent = (timestamp, message) => {
    setEvents(prevEvents => [...prevEvents, { timestamp, message }]);
  };

  const clearEvents = () => {
    setEvents([]);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Echo Chamber Visualizer</h1>
        <p>Uncover the recurring whispers of time.</p>
      </header>
      <main>
        <section className="input-section">
          <EchoInput onAddEvent={addEvent} />
          <button onClick={clearEvents} className="clear-button">Clear All Events</button>
        </section>
        <section className="visualizer-section">
          <h2>Temporal Echoes</h2>
          <EchoVisualizer echoes={echoes} />
        </section>
      </main>
    </div>
  );
}

export default App;
