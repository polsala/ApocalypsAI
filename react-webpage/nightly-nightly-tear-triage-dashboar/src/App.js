import React, { useState, useCallback } from 'react';
import TriageColumn from './components/TriageColumn';
import './App.css';

function App() {
  const initialTears = [
    { id: 'tear-001', name: 'Minor Chronal Ripple', severity: 'Low', status: 'Detected' },
    { id: 'tear-002', name: 'Localized Time Loop', severity: 'Medium', status: 'Detected' },
    { id: 'tear-003', name: 'Echo of a Forgotten Tuesday', severity: 'Low', status: 'Investigating' },
    { id: 'tear-004', name: 'Paradoxical Pocket Dimension', severity: 'High', status: 'Detected' },
    { id: 'tear-005', name: 'Temporal Echo Cascade', severity: 'Medium', status: 'Stabilized' }
  ];

  const [tears, setTears] = useState(initialTears);

  const handleDropTear = useCallback((tearId, newStatus) => {
    setTears(prevTears =>
      prevTears.map(tear =>
        tear.id === tearId ? { ...tear, status: newStatus } : tear
      )
    );
  }, []);

  const columns = [
    { id: 'Detected', title: 'Detected Anomalies' },
    { id: 'Investigating', title: 'Investigating' },
    { id: 'Stabilized', title: 'Stabilized / Contained' }
  ];

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Temporal Tear Triage Dashboard</h1>
        <p>Keep the timelines tidy, one tear at a time.</p>
      </header>
      <div className="triage-board">
        {columns.map(column => (
          <TriageColumn
            key={column.id}
            id={column.id}
            title={column.title}
            tears={tears.filter(tear => tear.status === column.id)}
            onDropTear={handleDropTear}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
