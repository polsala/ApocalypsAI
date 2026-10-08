import React, { useState, useEffect, useCallback } from 'react';
import EchoDisplay from './EchoDisplay';
import { generateEcho, frequencies, TemporalEcho } from './EchoGenerator';

const App: React.FC = () => {
  const [currentFrequency, setCurrentFrequency] = useState(frequencies[0]);
  const [echoes, setEchoes] = useState<TemporalEcho[]>([]);

  const handleFadeOut = useCallback((id: string) => {
    setEchoes(prevEchoes => prevEchoes.filter(echo => echo.id !== id));
  }, []);

  useEffect(() => {
    const echoInterval = setInterval(() => {
      const newEcho = generateEcho(currentFrequency);
      setEchoes(prevEchoes => [...prevEchoes, newEcho]);
    }, 2000); // Generate a new echo every 2 seconds

    return () => clearInterval(echoInterval);
  }, [currentFrequency]);

  return (
    <div style={{ position: 'relative', width: '100%', height: '100vh', overflow: 'hidden' }}>
      <h1 style={{ textAlign: 'center', color: '#e0e0e0', zIndex: 100 }}>Chronal Chatterbox</h1>
      <div style={{ textAlign: 'center', marginBottom: '20px', zIndex: 100 }}>
        <label htmlFor="frequency-select" style={{ marginRight: '10px', color: '#b0b0ff' }}>Tune Frequency:</label>
        <select
          id="frequency-select"
          value={currentFrequency}
          onChange={(e) => setCurrentFrequency(e.target.value)}
          style={{
            padding: '8px',
            borderRadius: '5px',
            border: '1px solid #555',
            backgroundColor: '#333',
            color: '#e0e0e0',
            cursor: 'pointer'
          }}
        >
          {frequencies.map(freq => (
            <option key={freq} value={freq}>{freq}</option>
          ))}
        </select>
      </div>

      {echoes.map(echo => (
        <EchoDisplay key={echo.id} echo={echo} onFadeOut={handleFadeOut} />
      ))}
    </div>
  );
};

export default App;
