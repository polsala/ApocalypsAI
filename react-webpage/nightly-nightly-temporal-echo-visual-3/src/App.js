import React, { useState } from 'react';
import EchoVisualizer from './EchoVisualizer';
import './App.css';

function App() {
  const [signatureInput, setSignatureInput] = useState('');
  const [currentSignature, setCurrentSignature] = useState('');

  const handleVisualize = () => {
    setCurrentSignature(signatureInput);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Pattern Visualizer</h1>
        <p>Enter a temporal signature to observe its unique echo pattern.</p>
      </header>
      <main className="App-main">
        <div className="input-section">
          <label htmlFor="temporal-signature-input">Temporal Signature:</label>
          <input
            id="temporal-signature-input"
            type="text"
            value={signatureInput}
            onChange={(e) => setSignatureInput(e.target.value)}
            placeholder="e.g., 'Chronal Flux', 'Quantum Ripple'"
            aria-label="Temporal Signature Input"
          />
          <button onClick={handleVisualize}>Visualize Echo</button>
        </div>
        <div className="visualizer-container">
          <EchoVisualizer signature={currentSignature} />
        </div>
      </main>
      <footer className="App-footer">
        <p>A whimsical utility from ApocalypsAI Nightly Integrator.</p>
      </footer>
    </div>
  );
}

export default App;
