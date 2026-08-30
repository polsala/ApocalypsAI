import React, { useState, useEffect } from 'react';
import ChronoCompass from './components/ChronoCompass';
import mockAnomalies from './data/mockAnomalies';

function App() {
  const [anomalies, setAnomalies] = useState([]);

  useEffect(() => {
    // In a real scenario, this would fetch data from an API.
    // For this utility, we use mock data.
    setAnomalies(mockAnomalies);
  }, []);

  return (
    <div style={styles.appContainer}>
      <h1 style={styles.appTitle}>Nightly Chrono-Compass</h1>
      <p style={styles.appSubtitle}>Visualizing Temporal Anomalies & Drifts</p>
      <ChronoCompass anomalies={anomalies} />
    </div>
  );
}

const styles = {
  appContainer: {
    fontFamily: 'monospace, sans-serif',
    backgroundColor: '#1a1a2e',
    color: '#e0e0e0',
    minHeight: '100vh',
    padding: '20px',
    textAlign: 'center'
  },
  appTitle: {
    color: '#e94560',
    marginBottom: '10px'
  },
  appSubtitle: {
    color: '#0f3460',
    marginBottom: '30px'
  }
};

export default App;
