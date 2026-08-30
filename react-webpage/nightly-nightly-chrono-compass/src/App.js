import React, { useState, useEffect } from 'react';
import ChronoInput from './ChronoInput';
import ChronoChart from './ChronoChart';
import './App.css';

function App() {
  const [entries, setEntries] = useState([]);

  useEffect(() => {
    // # Mock rationale: localStorage is a browser API. Mocking it in tests ensures
    // # that tests are deterministic and don't rely on actual browser storage state.
    const storedEntries = JSON.parse(localStorage.getItem('chronoCompassEntries')) || [];
    setEntries(storedEntries);
  }, []);

  useEffect(() => {
    // # Mock rationale: localStorage is a browser API. Mocking it in tests ensures
    // # that tests are deterministic and don't rely on actual browser storage state.
    localStorage.setItem('chronoCompassEntries', JSON.stringify(entries));
  }, [entries]);

  const addEntry = (newEntry) => {
    setEntries(prevEntries => {
      const now = new Date();
      // # Mock rationale: The Date object is non-deterministic. In tests, it will be mocked
      // # to return a fixed date/time, ensuring consistent timestamps for entries.
      const timestamp = now.toISOString();
      return [...prevEntries, { ...newEntry, timestamp }];
    });
  };

  // Process entries for chart data
  const getChartData = () => {
    const hours = Array.from({ length: 24 }, (_, i) => `${i}:00`);
    const energyData = new Array(24).fill(0);
    const focusData = new Array(24).fill(0);
    const timeSpeedData = new Array(24).fill(0);
    const counts = new Array(24).fill(0);

    entries.forEach(entry => {
      // # Mock rationale: Date parsing is deterministic, but the original timestamp
      // # comes from a potentially mocked Date object, ensuring consistency.
      const date = new Date(entry.timestamp);
      const hour = date.getHours();
      energyData[hour] += entry.energy;
      focusData[hour] += entry.focus;
      timeSpeedData[hour] += entry.timeSpeed;
      counts[hour]++;
    });

    for (let i = 0; i < 24; i++) {
      if (counts[i] > 0) {
        energyData[i] /= counts[i];
        focusData[i] /= counts[i];
        timeSpeedData[i] /= counts[i];
      }
    }

    return {
      labels: hours,
      datasets: [
        {
          label: 'Average Energy',
          data: energyData,
          borderColor: 'rgba(255, 99, 132, 1)',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          tension: 0.3
        },
        {
          label: 'Average Focus',
          data: focusData,
          borderColor: 'rgba(54, 162, 235, 1)',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          tension: 0.3
        },
        {
          label: 'Average Perceived Time Speed',
          data: timeSpeedData,
          borderColor: 'rgba(75, 192, 192, 1)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          tension: 0.3
        }
      ]
    };
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Chrono-Compass</h1>
        <p>Map your personal temporal landscape.</p>
      </header>
      <main>
        <ChronoInput onAddEntry={addEntry} />
        <div className="chart-container">
          <h2>Temporal Patterns</h2>
          {entries.length > 0 ? (
            <ChronoChart chartData={getChartData()} />
          ) : (
            <p>Log some entries to see your temporal patterns!</p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
