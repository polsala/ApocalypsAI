import React, { useState, useEffect } from 'react';
import EchoVisualizer from './components/EchoVisualizer';
import './App.css';

// Mock data for demonstration
const MOCK_ECHOES = [
  {
    id: 'echo-001',
    timestamp: '2023-10-26T10:00:00Z',
    category: 'Anomaly',
    description: 'Minor temporal ripple detected near Sector 7G.'
  },
  {
    id: 'echo-002',
    timestamp: '2023-10-25T14:30:00Z',
    category: 'Resource Fluctuation',
    description: 'Unusual spike in \'Scrap Metal\' readings in the Western Wastes.'
  },
  {
    id: 'echo-003',
    timestamp: '2023-10-26T08:15:00Z',
    category: 'Communication Intercept',
    description: 'Repeated distress signal pattern from unknown origin.'
  },
  {
    id: 'echo-004',
    timestamp: '2023-10-24T20:00:00Z',
    category: 'Anomaly',
    description: 'Flickering reality distortion field near the old power plant.'
  },
  {
    id: 'echo-005',
    timestamp: '2023-10-26T11:45:00Z',
    category: 'Resource Fluctuation',
    description: 'Depletion of \'Water Rations\' in Northern Outpost storage.'
  }
];

function App() {
  const [echoes, setEchoes] = useState([]);
  const [filterTerm, setFilterTerm] = useState('');

  useEffect(() => {
    // In a real application, you would fetch this data from an API or a local JSON file.
    // For this utility, we use mock data.
    setEchoes(MOCK_ECHOES);
  }, []);

  const filteredEchoes = echoes.filter(echo =>
    echo.category.toLowerCase().includes(filterTerm.toLowerCase()) ||
    echo.description.toLowerCase().includes(filterTerm.toLowerCase())
  );

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Echo Chamber Visualizer</h1>
        <input
          type="text"
          placeholder="Filter echoes..."
          value={filterTerm}
          onChange={(e) => setFilterTerm(e.target.value)}
          className="filter-input"
        />
      </header>
      <main>
        <EchoVisualizer echoes={filteredEchoes} />
      </main>
    </div>
  );
}

export default App;
