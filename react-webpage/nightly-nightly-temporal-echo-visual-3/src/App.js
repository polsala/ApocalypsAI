import React, { useState, useEffect, useCallback } from 'react';
import { analyzeTextForEchoes } from './utils/temporalEchoProcessor';
import InputForm from './components/InputForm';
import EchoVisualizer from './components/EchoVisualizer';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [keywordsInput, setKeywordsInput] = useState('');
  const [echoData, setEchoData] = useState({ labels: [], datasets: [] });

  const processEchoes = useCallback(() => {
    if (!inputText || !keywordsInput) {
      setEchoData({ labels: [], datasets: [] });
      return;
    }

    const keywords = keywordsInput.split(',').map(k => k.trim()).filter(k => k.length > 0);
    if (keywords.length === 0) {
      setEchoData({ labels: [], datasets: [] });
      return;
    }

    const data = analyzeTextForEchoes(inputText, keywords, 100); // Slice text every 100 lines
    
    const newDatasets = keywords.map((keyword, index) => ({
      label: keyword,
      data: data.map(slice => slice[keyword] || 0),
      borderColor: `hsl(${index * 60}, 70%, 60%)`,
      backgroundColor: `hsla(${index * 60}, 70%, 60%, 0.2)`,
      tension: 0.3,
      fill: false,
    }));

    setEchoData({
      labels: data.map((_, i) => `Slice ${i + 1}`),
      datasets: newDatasets,
    });
  }, [inputText, keywordsInput]);

  useEffect(() => {
    const handler = setTimeout(() => {
      processEchoes();
    }, 500); // Debounce input processing to avoid re-rendering on every keystroke
    return () => clearTimeout(handler);
  }, [processEchoes]);

  return (
    <div className="app-container">
      <h1>Temporal Echo Visualizer</h1>
      <InputForm
        inputText={inputText}
        setInputText={setInputText}
        keywordsInput={keywordsInput}
        setKeywordsInput={setKeywordsInput}
      />
      <div className="visualizer-section">
        {echoData.datasets.length > 0 ? (
          <EchoVisualizer data={echoData} />
        ) : (
          <p className="no-data-message">Enter text and keywords to see the temporal echoes!</p>
        )}
      </div>
    </div>
  );
}

export default App;
