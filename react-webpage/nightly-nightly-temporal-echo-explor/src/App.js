import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [echoes, setEchoes] = useState([]);

  useEffect(() => {
    // Mock echo data
    const mockEchoes = [
      { id: 1, time: '12:00:01', intensity: 80 },
      { id: 2, time: '12:00:05', intensity: 60 },
      { id: 3, time: '12:00:10', intensity: 90 },
    ];
    setEchoes(mockEchoes);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Explorer</h1>
        <p>Visualize echoes through time</p>
      </header>
      <main>
        <div className="echo-timeline">
          {echoes.map(echo => (
            <div key={echo.id} className="echo-event" style={{ height: `${echo.intensity}%` }}>
              <span>{echo.time}</span>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
