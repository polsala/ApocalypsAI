import React, { useState, useMemo } from 'react';
import EchoTimeline from './components/EchoTimeline';
import mockEchoes from './data/mockEchoes';
import './App.css';

function App() {
  const [filterIntensity, setFilterIntensity] = useState(0); // 0 for all, 1-5 for specific
  const [filterOrigin, setFilterOrigin] = useState('All'); // 'All', 'Past', 'Future', 'Alternate Reality'

  const filteredEchoes = useMemo(() => {
    return mockEchoes
      .filter(echo => {
        const matchesIntensity = filterIntensity === 0 || echo.intensity === filterIntensity;
        const matchesOrigin = filterOrigin === 'All' || echo.origin === filterOrigin;
        return matchesIntensity && matchesOrigin;
      })
      .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  }, [filterIntensity, filterOrigin]);

  const originOptions = ['All', 'Past', 'Future', 'Alternate Reality'];

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Temporal Echo Visualizer</h1>
        <p>Unraveling the fabric of spacetime, one echo at a time.</p>
      </header>

      <div className="filters">
        <label htmlFor="intensity-filter">Filter by Intensity:</label>
        <select
          id="intensity-filter"
          value={filterIntensity}
          onChange={(e) => setFilterIntensity(Number(e.target.value))}
        >
          <option value={0}>All</option>
          {[1, 2, 3, 4, 5].map(i => (
            <option key={i} value={i}>{i}</option>
          ))}
        </select>

        <label htmlFor="origin-filter">Filter by Origin:</label>
        <select
          id="origin-filter"
          value={filterOrigin}
          onChange={(e) => setFilterOrigin(e.target.value)}
        >
          {originOptions.map(origin => (
            <option key={origin} value={origin}>{origin}</option>
          ))}
        </select>
      </div>

      <EchoTimeline echoes={filteredEchoes} />

      <footer className="App-footer">
        <p>&copy; ApocalypsAI Nightly Integrator</p>
      </footer>
    </div>
  );
}

export default App;
