import React, { useState, useEffect } from 'react';
import DriftChart from './components/DriftChart';

// Mock data fetching function
const fetchDriftData = async () => {
  // # Mock rationale: Simulate an asynchronous API call to fetch temporal drift data.
  // In a real scenario, this would fetch from a backend API.
  // For testing and self-containment, we return a hardcoded array.
  return new Promise(resolve => {
    setTimeout(() => {
      resolve([
        { id: 'd001', timestamp: '2024-07-20T10:00:00Z', severity: 'low', description: 'Minor temporal ripple detected near Sector Gamma.' },
        { id: 'd002', timestamp: '2024-07-20T11:30:00Z', severity: 'medium', description: 'Localized time dilation event in Sub-Quadrant 7.' },
        { id: 'd003', timestamp: '2024-07-20T13:45:00Z', severity: 'high', description: 'Significant chronal displacement originating from Nexus Point 3.' },
        { id: 'd004', timestamp: '2024-07-20T15:10:00Z', severity: 'low', description: 'Faint echo of a past event in the archives.' },
        { id: 'd005', timestamp: '2024-07-20T16:00:00Z', severity: 'medium', description: 'Temporal flux detected, requiring monitoring.' },
        { id: 'd006', timestamp: '2024-07-20T18:20:00Z', severity: 'high', description: 'Major causality loop detected, immediate stabilization required.' }
      ]);
    }, 500); // Simulate network latency
  });
};

function App() {
  const [driftData, setDriftData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getDriftData = async () => {
      try {
        const data = await fetchDriftData();
        setDriftData(data);
      } catch (error) {
        console.error('Failed to fetch temporal drift data:', error);
      } finally {
        setLoading(false);
      }
    };
    getDriftData();
  }, []);

  return (
    <div className="App">
      <h1>ApocalypsAI Temporal Drift Dashboard</h1>
      <div className="dashboard-container">
        {loading ? (
          <p>Calibrating temporal sensors... please wait.</p>
        ) : (
          <DriftChart data={driftData} />
        )}
      </div>
    </div>
  );
}

export default App;
export { fetchDriftData }; // Export for testing purposes
