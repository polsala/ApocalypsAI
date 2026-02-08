import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import EchoDisplay from './EchoDisplay';
import TemporalStabilityMeter from './TemporalStabilityMeter';
import { generateEchoes, calculateStability } from './TemporalProcessor';

const NUM_ECHOES = 5;

function App() {
  const [inputText, setInputText] = useState('');
  const [echoes, setEchoes] = useState([]);
  const [stability, setStability] = useState(100);

  const processText = useCallback(() => {
    if (inputText.trim() === '') {
      setEchoes([]);
      setStability(100);
      return;
    }
    const generatedEchoes = generateEchoes(inputText, NUM_ECHOES);
    setEchoes(generatedEchoes);
    setStability(calculateStability(inputText));
  }, [inputText]);

  useEffect(() => {
    const handler = setTimeout(() => {
      processText();
    }, 300); // Debounce input for better performance

    return () => {
      clearTimeout(handler);
    };
  }, [inputText, processText]);

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Temporal Echo Visualizer</h1>
        <p>Witness your words ripple through the chronal fabric.</p>
      </header>
      <main>
        <div className="input-section">
          <textarea
            placeholder="Enter text to see its temporal echoes..."
            value={inputText}
            onChange={handleInputChange}
            rows="5"
          />
        </div>
        <div className="visualization-section">
          <TemporalStabilityMeter stability={stability} />
          <div className="echo-container">
            {echoes.length === 0 && inputText.trim() !== '' ? (
              <p className="no-echoes">Generating echoes...</p>
            ) : echoes.length === 0 && inputText.trim() === '' ? (
              <p className="no-echoes">Start typing to see echoes.</p>
            ) : (
              echoes.map((echo, index) => (
                <EchoDisplay
                  key={index}
                  text={echo.text}
                  style={echo.style}
                  delay={index * 0.1} // Stagger animation
                />
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
