import React, { useState, useEffect, useCallback } from 'react';
import EchoMonitor from './EchoMonitor';
import './App.css';

const App = () => {
  const [echoData, setEchoData] = useState({
    amplitude: 0,
    frequency: 0,
    stability: 100 // 0-100, 100 is perfectly stable
  });

  const generateEchoData = useCallback(() => {
    const newAmplitude = Math.floor(Math.random() * 100);
    const newFrequency = Math.floor(Math.random() * 50);
    
    // Simulate stability based on amplitude and frequency
    // Higher amplitude/frequency means lower stability
    const instabilityFactor = (newAmplitude * 0.5 + newFrequency * 1.5) / 200; // Normalize to 0-1
    const newStability = Math.max(0, Math.floor(100 - (instabilityFactor * 100)));

    setEchoData({
      amplitude: newAmplitude,
      frequency: newFrequency,
      stability: newStability
    });
  }, []);

  useEffect(() => {
    // Initial data generation
    generateEchoData();

    // Set up interval for continuous data generation
    const intervalId = setInterval(generateEchoData, 1000); // Update every 1 second

    // Clean up interval on component unmount
    return () => clearInterval(intervalId);
  }, [generateEchoData]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p className="subtitle">Monitoring the Fabric of Time</p>
      </header>
      <main className="App-main">
        <EchoMonitor data={echoData} />
      </main>
      <footer className="App-footer">
        <p>&copy; ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
};

export default App;
