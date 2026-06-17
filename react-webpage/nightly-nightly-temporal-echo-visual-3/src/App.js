import React from 'react';
import './App.css';
import EchoVisualizer from './EchoVisualizer';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Observing the ripples in time's fabric.</p>
      </header>
      <main>
        <EchoVisualizer />
      </main>
    </div>
  );
}

export default App;
