import React from 'react';
import './App.css';
import TemporalEchoChamber from './TemporalEchoChamber';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Temporal Echo Visualizer</h1>
      </header>
      <main>
        <TemporalEchoChamber />
      </main>
    </div>
  );
}

export default App;
