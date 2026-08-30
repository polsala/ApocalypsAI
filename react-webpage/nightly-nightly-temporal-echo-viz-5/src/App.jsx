import React, { useState, useEffect } from 'react';
import AnomalyTimeline from './components/AnomalyTimeline';

function App() {
  const [anomalies, setAnomalies] = useState([]);
  const [newAnomalyTimestamp, setNewAnomalyTimestamp] = useState('');
  const [newAnomalyDescription, setNewAnomalyDescription] = useState('');
  const [newAnomalySeverity, setNewAnomalySeverity] = useState(3); // Default severity

  useEffect(() => {
    // Load initial data or provide some defaults for demonstration
    const initialAnomalies = [
      { id: 'a1', timestamp: new Date('2024-07-19T10:00:00Z'), description: 'Minor temporal ripple detected', severity: 2 },
      { id: 'a2', timestamp: new Date('2024-07-20T14:30:00Z'), description: 'Localized time dilation event', severity: 4 },
      { id: 'a3', timestamp: new Date('2024-07-21T08:15:00Z'), description: 'Echo of a past paradox', severity: 3 },
    ];
    setAnomalies(initialAnomalies);
  }, []);

  const handleAddAnomaly = (e) => {
    e.preventDefault();
    if (newAnomalyTimestamp && newAnomalyDescription) {
      const newAnomaly = {
        id: `a${anomalies.length + 1}-${Date.now()}`, // Unique ID
        timestamp: new Date(newAnomalyTimestamp),
        description: newAnomalyDescription,
        severity: parseInt(newAnomalySeverity, 10),
      };
      setAnomalies([...anomalies, newAnomaly].sort((a, b) => a.timestamp - b.timestamp));
      setNewAnomalyTimestamp('');
      setNewAnomalyDescription('');
      setNewAnomalySeverity(3);
    }
  };

  return (
    <div className="App">
      <h1>Temporal Echo Visualizer</h1>

      <form onSubmit={handleAddAnomaly} className="anomaly-form">
        <h2>Add New Anomaly</h2>
        <div>
          <label htmlFor="timestamp">Timestamp:</label>
          <input
            id="timestamp"
            type="datetime-local"
            value={newAnomalyTimestamp}
            onChange={(e) => setNewAnomalyTimestamp(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="description">Description:</label>
          <input
            id="description"
            type="text"
            value={newAnomalyDescription}
            onChange={(e) => setNewAnomalyDescription(e.target.value)}
            placeholder="e.g., Minor time loop"
            required
          />
        </div>
        <div>
          <label htmlFor="severity">Severity (1-5):</label>
          <input
            id="severity"
            type="number"
            min="1"
            max="5"
            value={newAnomalySeverity}
            onChange={(e) => setNewAnomalySeverity(e.target.value)}
            required
          />
        </div>
        <button type="submit">Add Anomaly</button>
      </form>

      <AnomalyTimeline anomalies={anomalies} />
    </div>
  );
}

export default App;
