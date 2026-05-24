import React, { useState, useEffect, useCallback } from 'react';
import ResourceGauge from './ResourceGauge';

const App = () => {
  const initialResources = {
    'Hydro-Essence': 50,
    'Sustenance Scraps': 50,
    'Spirit Spark': 70,
    'Mind Mettle': 80,
    'Salvage Shards': 30,
  };

  const [resources, setResources] = useState(() => {
    // Load from localStorage or use initial values
    // Mock rationale: localStorage is a browser API and needs to be mocked for deterministic, offline tests.
    try {
      const savedResources = localStorage.getItem('apocalypsai_resources');
      return savedResources ? JSON.parse(savedResources) : initialResources;
    } catch (error) {
      console.error("Failed to load resources from localStorage:", error);
      return initialResources;
    }
  });

  useEffect(() => {
    // Save to localStorage whenever resources change
    // Mock rationale: localStorage is a browser API and needs to be mocked for deterministic, offline tests.
    try {
      localStorage.setItem('apocalypsai_resources', JSON.stringify(resources));
    } catch (error) {
      console.error("Failed to save resources to localStorage:", error);
    }
  }, [resources]);

  const updateResource = useCallback((name, delta) => {
    setResources(prevResources => {
      const newValue = Math.max(0, Math.min(100, prevResources[name] + delta));
      return {
        ...prevResources,
        [name]: newValue,
      };
    });
  }, []);

  return (
    <div className="app-container">
      <h1>Nightly Resource Barometer</h1>
      <p className="tagline">Keep your post-apocalyptic supplies in check!</p>
      <div className="gauges-grid">
        {Object.entries(resources).map(([name, value]) => (
          <ResourceGauge
            key={name}
            name={name}
            value={value}
            onIncrease={() => updateResource(name, 5)}
            onDecrease={() => updateResource(name, -5)}
          />
        ))}
      </div>
      <p className="footer-note">Values persist in your browser's local storage.</p>
    </div>
  );
};

export default App;
