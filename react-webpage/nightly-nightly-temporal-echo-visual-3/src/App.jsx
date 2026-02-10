import React from 'react';
import EchoVisualizer from './components/EchoVisualizer';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Witness the subtle distortions of spacetime.</p>
      </header>
      <main>
        <EchoVisualizer />
      </main>
    </div>
  );
}

export default App;
