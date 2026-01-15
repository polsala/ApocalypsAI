import React, { useState, useEffect } from 'react';
import MetricCard from './components/MetricCard';
import SurvivalTip from './components/SurvivalTip';
import './App.css';

// Mock data - In a real app, this would come from an API
import mockMetrics from './data/mockMetrics';
import mockTips from './data/mockTips';

function App() {
  const [metrics, setMetrics] = useState([]);
  const [currentTip, setCurrentTip] = useState('');

  useEffect(() => {
    // Simulate fetching data
    setMetrics(mockMetrics);
    const randomIndex = Math.floor(Math.random() * mockTips.length);
    setCurrentTip(mockTips[randomIndex]);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Apocalypse Dashboard</h1>
        <p>Keeping you informed, one disaster at a time.</p>
      </header>
      <main>
        <section className="metrics-section">
          <h2>Current Apocalyptic Metrics</h2>
          <div className="metrics-grid">
            {metrics.map(metric => (
              <MetricCard key={metric.id} metric={metric} />
            ))}
          </div>
        </section>
        <section className="tips-section">
          <h2>Daily Survival Tip</h2>
          <SurvivalTip tip={currentTip} />
        </section>
      </main>
      <footer>
        <p>&copy; 2023 ApocalypsAI. Stay safe out there!</p>
      </footer>
    </div>
  );
}

export default App;
