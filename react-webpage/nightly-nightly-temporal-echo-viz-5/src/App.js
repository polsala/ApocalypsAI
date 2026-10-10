import React, { useState, useEffect, useCallback } from 'react';
import EchoViz from './EchoViz';
import { simulateEchoes, generateInitialEchoes } from './EchoGenerator';

function App() {
  const [echoData, setEchoData] = useState(() => generateInitialEchoes(10));

  const updateEchoes = useCallback(() => {
    setEchoData(prevEchoes => simulateEchoes(prevEchoes));
  }, []);

  useEffect(() => {
    const interval = setInterval(updateEchoes, 100); // Update every 100ms
    return () => clearInterval(interval);
  }, [updateEchoes]);

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      <h1 style={{ position: 'absolute', top: '20px', left: '50%', transform: 'translateX(-50%)', zIndex: 10, color: '#fff', textShadow: '0 0 5px #000' }}>
        Temporal Echo Visualizer
      </h1>
      <EchoViz echoData={echoData} />
    </div>
  );
}

export default App;
