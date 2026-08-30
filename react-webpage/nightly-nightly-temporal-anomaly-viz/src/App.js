import React from 'react';
import './App.css';
import AnomalyDashboard from './components/AnomalyDashboard';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Anomaly Visualizer</h1>
      </header>
      <main>
        <AnomalyDashboard />
      </main>
    </div>
  );
}

export default App;
