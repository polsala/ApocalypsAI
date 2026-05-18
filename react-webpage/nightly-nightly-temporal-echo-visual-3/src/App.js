import React, { useState, useEffect } from 'react';
import mockEchoes from './data/mockEchoes';
import './App.css'; // Main app styling

function App() {
  const [echoes, setEchoes] = useState([]);
  const [filterType, setFilterType] = useState('All');

  useEffect(() => {
    // In a real app, this would fetch from an API.
    // Mock rationale: Using static mock data ensures deterministic tests without external dependencies.
    setEchoes(mockEchoes);
  }, []);

  const handleFilterChange = (event) => {
    setFilterType(event.target.value);
  };

  const filteredEchoes = echoes.filter(echo => {
    if (filterType === 'All') {
      return true;
    }
    return echo.type === filterType;
  });

  const uniqueEchoTypes = ['All', ...new Set(mockEchoes.map(echo => echo.type))];

  return (
    <div className="App">
      <h1>Temporal Echo Visualizer</h1>

      <div className="filters">
        <label htmlFor="echo-type-filter">Filter by Echo Type:</label>
        <select id="echo-type-filter" onChange={handleFilterChange} value={filterType}>
          {uniqueEchoTypes.map(type => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
      </div>

      <div className="echo-list">
        {filteredEchoes.length > 0 ? (
          filteredEchoes.map(echo => (
            <div key={echo.id} className={`echo-card severity-${echo.severity}`}>
              <h3>{echo.type} - {echo.location}</h3>
              <p><strong>Timestamp:</strong> {new Date(echo.timestamp).toLocaleString()}</p>
              <p><strong>Severity:</strong> {echo.severity} / 5</p>
              <p>{echo.description}</p>
            </div>
          ))
        ) : (
          <p>No temporal echoes of this type detected.</p>
        )}
      </div>
    </div>
  );
}

export default App;
