import React, { useState, useEffect } from 'react';
import ChronoCompass from './ChronoCompass';
import './styles.css';

const App = () => {
  const [temporalStability, setTemporalStability] = useState(75); // 0-100
  const [resourceAbundance, setResourceAbundance] = useState(60); // 0-100
  const [communityMorale, setCommunityMorale] = useState(85);   // 0-100
  const [weatherAnomaly, setWeatherAnomaly] = useState(20);     // 0-100 (lower is better)

  // # Mock rationale: Simulates real-time data updates from various ApocalypsAI systems.
  // In a real scenario, this would involve API calls or WebSocket connections.
  useEffect(() => {
    const interval = setInterval(() => {
      setTemporalStability(Math.floor(Math.random() * 40) + 60); // 60-99
      setResourceAbundance(Math.floor(Math.random() * 50) + 40); // 40-89
      setCommunityMorale(Math.floor(Math.random() * 30) + 70);   // 70-99
      setWeatherAnomaly(Math.floor(Math.random() * 30) + 10);    // 10-39 (lower is less anomalous)
    }, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const getApocalypseStatus = () => {
    // Simple logic to determine overall status
    const avgStability = temporalStability;
    const avgResources = resourceAbundance;
    const avgMorale = communityMorale;
    const avgWeather = 100 - weatherAnomaly; // Invert for better-is-higher scale

    const overallScore = (avgStability + avgResources + avgMorale + avgWeather) / 4;

    if (overallScore > 85) return "Stable Temporal Flow";
    if (overallScore > 70) return "Minor Reality Glitch";
    if (overallScore > 50) return "Resource Scarcity Alert";
    return "Imminent Chrono-Collapse";
  };

  return (
    <div className="dashboard-container">
      <h1>Nightly Chrono-Compass Dashboard</h1>
      <div className="compass-section">
        <ChronoCompass
          temporalStability={temporalStability}
          resourceAbundance={resourceAbundance}
          communityMorale={communityMorale}
          weatherAnomaly={weatherAnomaly}
        />
        <div className="status-display">
          <h2>Apocalypse Status:</h2>
          <p className={`status-${getApocalypseStatus().replace(/\s/g, '-')}`}>
            {getApocalypseStatus()}
          </p>
        </div>
      </div>
      <div className="metrics-section">
        <div className="metric-card">
          <h3>Temporal Stability Index</h3>
          <p>{temporalStability}%</p>
        </div>
        <div className="metric-card">
          <h3>Resource Abundance Level</h3>
          <p>{resourceAbundance}%</p>
        </div>
        <div className="metric-card">
          <h3>Community Morale Pulse</h3>
          <p>{communityMorale}%</p>
        </div>
        <div className="metric-card">
          <h3>Simulated Weather Anomaly</h3>
          <p>{weatherAnomaly}%</p>
        </div>
      </div>
    </div>
  );
};

export default App;
