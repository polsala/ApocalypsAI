import React, { useState, useEffect } from 'react';
import ChronoMap from './components/ChronoMap';
import CorrectionSuggestions from './components/CorrectionSuggestions';

const App = () => {
  const [temporalData, setTemporalData] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState(null);

  useEffect(() => {
    // Simulate fetching temporal data
    // # Mock rationale: In a real scenario, this would be an API call.
    // For this standalone utility, we use static, simulated data.
    const simulatedData = [
      { id: 'region-alpha', name: 'Alpha Sector', stability: 0.85, drift: 0.02, coordinates: { x: 50, y: 30 } },
      { id: 'region-beta', name: 'Beta Quadrant', stability: 0.45, drift: 0.15, coordinates: { x: 150, y: 80 } },
      { id: 'region-gamma', name: 'Gamma Expanse', stability: 0.92, drift: 0.01, coordinates: { x: 250, y: 50 } },
      { id: 'region-delta', name: 'Delta Nexus', stability: 0.60, drift: 0.08, coordinates: { x: 100, y: 120 } },
      { id: 'region-epsilon', name: 'Epsilon Void', stability: 0.20, drift: 0.30, coordinates: { x: 200, y: 150 } }
    ];
    setTemporalData(simulatedData);
  }, []);

  const handleRegionClick = (regionId) => {
    const region = temporalData.find(r => r.id === regionId);
    setSelectedRegion(region);
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '20px',
      backgroundColor: '#36393f',
      padding: '20px',
      borderRadius: '8px',
      boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)'
    }}>
      <h1 style={{ color: '#61dafb', textAlign: 'center' }}>Nightly Chrono-Compass</h1>
      <p style={{ textAlign: 'center', fontSize: '0.9em', color: '#bbb' }}>
        Visualize temporal stability across regions and identify critical drift correction points.
      </p>

      <ChronoMap data={temporalData} onRegionClick={handleRegionClick} selectedRegionId={selectedRegion?.id} />

      {selectedRegion && (
        <CorrectionSuggestions region={selectedRegion} />
      )}
    </div>
  );
};

export default App;
