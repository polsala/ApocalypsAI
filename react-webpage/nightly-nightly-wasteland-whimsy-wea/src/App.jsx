import React, { useState, useEffect } from 'react';
import { generateWhimsyForecast } from './WhimsyGenerator';
import './App.css';

function App() {
  const [forecast, setForecast] = useState(null);

  useEffect(() => {
    setForecast(generateWhimsyForecast());
  }, []);

  const handleReroll = () => {
    setForecast(generateWhimsyForecast());
  };

  if (!forecast) {
    return <div className="app-container">Loading Whimsy...</div>;
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Nightly Wasteland Whimsy Weaver</h1>
        <p>Your daily dose of post-apocalyptic charm!</p>
      </header>
      <main className="forecast-card">
        <h2>Today's Whimsy Forecast</h2>
        <p><strong>Weather:</strong> {forecast.weather}</p>
        <p><strong>Resources:</strong> {forecast.resources}</p>
        <p><strong>Wasteland Mood:</strong> {forecast.mood}</p>
        <p className="timestamp">Last updated: {forecast.timestamp}</p>
        <button onClick={handleReroll} className="reroll-button">Reroll Whimsy</button>
      </main>
      <footer className="app-footer">
        <p>Powered by ApocalypsAI Integrator</p>
      </footer>
    </div>
  );
}

export default App;
