import React, { useState, useEffect, useMemo } from 'react';
import mockEchoes from './data/mockEchoes';
import EchoDisplay from './components/EchoDisplay';
import EchoFilter from './components/EchoFilter';
import './App.css';

function App() {
  const [echoes, setEchoes] = useState([]);
  const [filters, setFilters] = useState({
    type: '',
    minIntensity: '',
  });

  useEffect(() => {
    // Simulate fetching data
    setEchoes(mockEchoes);
  }, []);

  const availableEchoTypes = useMemo(() => {
    const types = new Set(mockEchoes.map(echo => echo.type));
    return Array.from(types).sort();
  }, []);

  const filteredEchoes = useMemo(() => {
    return echoes.filter(echo => {
      const matchesType = filters.type === '' || echo.type === filters.type;
      const matchesIntensity = filters.minIntensity === '' || echo.intensity >= filters.minIntensity;
      return matchesType && matchesIntensity;
    });
  }, [echoes, filters]);

  const handleFilterChange = (filterName, value) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      [filterName]: value,
    }));
  };

  return (
    <div className="App">
      <header>
        <h1>Nightly Temporal Echo Visualizer</h1>
        <p>Observe the shimmering distortions of time.</p>
      </header>
      <main>
        <EchoFilter
          filters={filters}
          onFilterChange={handleFilterChange}
          echoTypes={availableEchoTypes}
        />
        <ul className="echo-list">
          {filteredEchoes.length > 0 ? (
            filteredEchoes.map(echo => (
              <EchoDisplay key={echo.id} echo={echo} />
            ))
          ) : (
            <li className="echo-item">No temporal echoes matching current filters.</li>
          )}
        </ul>
      </main>
    </div>
  );
}

export default App;
