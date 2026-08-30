import React, { useState, useCallback } from 'react';
import EventInputForm from './components/EventInputForm';
import EchoDisplay from './components/EchoDisplay';
import './App.css';

// Simple deterministic hash-like function for echo generation
const generateEchoes = (eventName) => {
  if (!eventName) return [];

  const seed = eventName.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
  const echoes = [];

  const timeOffsets = [
    "3 cycles ago", "next Tuesday in a parallel dimension", "a whisper from the void",
    "the day before yesterday's tomorrow", "a fleeting moment in the 5th continuum",
    "when the twin moons align", "just after the last temporal tremor"
  ];
  const intensities = [
    "faint shimmer", "subtle ripple", "strong resonance", "blinding flash",
    "barely perceptible hum", "deep thrum", "ethereal glow"
  ];
  const descriptions = [
    "a butterfly's wingbeat in a forgotten past",
    "the faint scent of ozone from a future paradox",
    "a shadow lengthening in an alternate present",
    "a forgotten melody playing backwards",
    "the echo of a laugh from a timeline that never was",
    "a sudden chill in the air, then gone",
    "a fleeting glimpse of what might have been"
  ];

  for (let i = 0; i < 3 + (seed % 3); i++) { // Generate 3-5 echoes
    const offsetIndex = (seed + i * 7) % timeOffsets.length;
    const intensityIndex = (seed + i * 11) % intensities.length;
    const descIndex = (seed + i * 13) % descriptions.length;

    echoes.push({
      id: `${eventName}-${i}-${seed}`,
      timeOffset: timeOffsets[offsetIndex],
      intensity: intensities[intensityIndex],
      description: descriptions[descIndex]
    });
  }
  return echoes;
};

function App() {
  const [eventName, setEventName] = useState('');
  const [echoes, setEchoes] = useState([]);

  const handleGenerateEchoes = useCallback((name) => {
    setEventName(name);
    setEchoes(generateEchoes(name));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Unravel the ripples of events across the timelines.</p>
      </header>
      <main>
        <EventInputForm onGenerate={handleGenerateEchoes} />
        <EchoDisplay echoes={echoes} />
      </main>
      <footer>
        <p>&copy; ApocalypsAI Integrator</p>
      </footer>
    </div>
  );
}

export default App;
