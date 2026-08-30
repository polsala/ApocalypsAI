import React, { useState, useEffect, useCallback } from 'react';
import CelestialBody from './CelestialBody';
import AlignmentDisplay from './AlignmentDisplay';
import { fetchCelestialData } from './api';

const App = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [celestialData, setCelestialData] = useState({ positions: [], influences: [] });
  const [loading, setLoading] = useState(true);

  const loadCelestialData = useCallback(async (date) => {
    setLoading(true);
    const data = await fetchCelestialData(date);
    setCelestialData(data);
    setLoading(false);
  }, []);

  useEffect(() => {
    loadCelestialData(currentDate);
  }, [currentDate, loadCelestialData]);

  const handleDateChange = (event) => {
    setCurrentDate(new Date(event.target.value + 'T12:00:00')); // Set to midday to avoid timezone issues
  };

  const formatDateForInput = (date) => {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  return (
    <div style={{
      fontFamily: 'Arial, sans-serif',
      textAlign: 'center',
      backgroundColor: '#1a1a2e',
      color: '#e0e0e0',
      padding: '20px',
      borderRadius: '10px',
      boxShadow: '0 8px 20px rgba(0, 0, 0, 0.5)'
    }}>
      <h1 style={{ color: '#9932CC' }}>Nightly Celestial Alignment Tracker</h1>

      <div style={{ marginBottom: '20px' }}>
        <label htmlFor="date-picker" style={{ marginRight: '10px', fontSize: '1.1em' }}>Select Date:</label>
        <input
          type="date"
          id="date-picker"
          value={formatDateForInput(currentDate)}
          onChange={handleDateChange}
          style={{
            padding: '8px',
            borderRadius: '5px',
            border: '1px solid #6a0dad',
            backgroundColor: '#3a3a5e',
            color: '#e0e0e0'
          }}
        />
      </div>

      <div style={{
        position: 'relative',
        width: '350px',
        height: '350px',
        borderRadius: '50%',
        border: '2px dashed #6a0dad',
        margin: '30px auto',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#0f0f1a'
      }}>
        {loading ? (
          <p>Loading cosmic energies...</p>
        ) : (
          celestialData.positions.map((body, index) => (
            <CelestialBody
              key={body.name}
              name={body.name}
              angle={body.angle}
              color={body.color}
              orbitRadius={150} // Fixed orbit radius for all bodies
            />
          ))
        )}
        <div style={{
          position: 'absolute',
          width: '40px',
          height: '40px',
          borderRadius: '50%',
          backgroundColor: '#FFD700',
          boxShadow: '0 0 15px #FFD700',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontSize: '0.8em',
          fontWeight: 'bold',
          color: 'black'
        }} title="Central Nexus">
          N
        </div>
      </div>

      {loading ? (
        <p>Calculating influences...</p>
      ) : (
        <AlignmentDisplay influences={celestialData.influences} />
      )}
    </div>
  );
};

export default App;
