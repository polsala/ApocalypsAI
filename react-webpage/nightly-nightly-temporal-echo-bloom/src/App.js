import React from 'react';
import EchoBloom from './EchoBloom';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Bloom</h1>
        <p>Click on the echoes to harmonize their temporal frequencies.</p>
      </header>
      <main className="App-main">
        <EchoBloom />
      </main>
    </div>
  );
}

export default App;
