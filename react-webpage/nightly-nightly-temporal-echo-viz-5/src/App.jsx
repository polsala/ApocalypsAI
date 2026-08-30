import React, { useState, useEffect } from 'react';
import { generateEchoParameters } from './EchoGenerator';
import EchoVisualizer from './EchoVisualizer';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [echoParams, setEchoParams] = useState(null);

  useEffect(() => {
    if (inputText.trim() === '') {
      setEchoParams(null);
      return;
    }
    const params = generateEchoParameters(inputText);
    setEchoParams(params);
  }, [inputText]);

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  return (
    <div className="App">
      <h1>Temporal Echo Signature Visualizer</h1>
      <p>Enter any text to see its unique temporal echo pattern.</p>
      <input
        type="text"
        value={inputText}
        onChange={handleInputChange}
        placeholder="Type your temporal signature here..."
        aria-label="Temporal Signature Input"
      />
      <div className="visualizer-container">
        {echoParams ? (
          <EchoVisualizer params={echoParams} />
        ) : (
          <p className="placeholder-text">Your echo awaits...</p>
        )}
      </div>
    </div>
  );
}

export default App;
