import React, { useState, useEffect } from 'react';
import './App.css';

// Helper function for deterministic pseudo-random number generation
const pseudoRandom = (seed) => {
  let x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
};

// Exported for testing purposes
export const generateConfluenceData = (keyword) => {
  if (!keyword) return { nodes: [], links: [] };

  const baseSeed = keyword.toLowerCase().split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);

  const nodes = [{ id: keyword, label: keyword, x: 250, y: 250, color: '#FFD700' }]; // Gold for the central concept
  const links = [];

  const numEchoes = Math.floor(pseudoRandom(baseSeed + 1) * 3) + 2; // 2-4 main echoes

  for (let i = 0; i < numEchoes; i++) {
    const echoSeed = baseSeed + i * 100 + 7;
    const yearOffset = Math.floor(pseudoRandom(echoSeed + 2) * 2000) - 1000; // -1000 to +1000 years
    const echoLabel = `${keyword} Echo ${i + 1} (${yearOffset > 0 ? '+' : ''}${yearOffset}y)`;
    const echoId = `echo-${keyword}-${i}`;

    const angle = pseudoRandom(echoSeed + 3) * Math.PI * 2;
    const radius = 100 + pseudoRandom(echoSeed + 4) * 50; // 100-150px radius
    const x = 250 + Math.cos(angle) * radius;
    const y = 250 + Math.sin(angle) * radius;

    nodes.push({ id: echoId, label: echoLabel, x, y, color: '#ADD8E6' }); // Light blue for echoes
    links.push({ source: keyword, target: echoId, type: 'temporal-link', color: '#87CEEB' });

    // Add some sub-echoes for more complexity
    if (pseudoRandom(echoSeed + 7) > 0.4 && i < numEchoes - 1) { // 40% chance for a sub-echo
      const subEchoSeed = echoSeed + 10 + i;
      const subEchoLabel = `Sub-Echo ${i + 1}-${Math.floor(pseudoRandom(subEchoSeed + 8) * 2) + 1}`;
      const subEchoId = `sub-echo-${keyword}-${i}-${Math.floor(pseudoRandom(subEchoSeed + 9) * 2) + 1}`;

      const subAngle = pseudoRandom(subEchoSeed + 10) * Math.PI * 2;
      const subRadius = 30 + pseudoRandom(subEchoSeed + 11) * 20; // 30-50px radius
      const subX = x + Math.cos(subAngle) * subRadius;
      const subY = y + Math.sin(subAngle) * subRadius;

      nodes.push({ id: subEchoId, label: subEchoLabel, x: subX, y: subY, color: '#90EE90' }); // Light green for sub-echoes
      links.push({ source: echoId, target: subEchoId, type: 'minor-link', color: '#98FB98' });
    }
  }

  return { nodes, links };
};

function App() {
  const [concept, setConcept] = useState('');
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  const handleGenerate = () => {
    setGraphData(generateConfluenceData(concept));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chronal Confluence Canvas</h1>
        <p>Unravel the temporal echoes of your concepts!</p>
      </header>
      <div className="input-section">
        <input
          type="text"
          placeholder="Enter a concept (e.g., 'apocalypse', 'hope')"
          value={concept}
          onChange={(e) => setConcept(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleGenerate();
            }
          }}
        />
        <button onClick={handleGenerate}>Generate Confluence</button>
      </div>
      <div className="graph-container">
        <svg width="500" height="500" viewBox="0 0 500 500">
          {graphData.links.map((link, index) => {
            const sourceNode = graphData.nodes.find(node => node.id === link.source);
            const targetNode = graphData.nodes.find(node => node.id === link.target);
            if (!sourceNode || !targetNode) return null;
            return (
              <line
                key={index}
                x1={sourceNode.x}
                y1={sourceNode.y}
                x2={targetNode.x}
                y2={targetNode.y}
                stroke={link.color || '#ccc'}
                strokeWidth="2"
                data-testid="link-line"
              />
            );
          })}
          {graphData.nodes.map((node) => (
            <g key={node.id} transform={`translate(${node.x}, ${node.y})`}>
              <circle
                r="15"
                fill={node.color || '#61dafb'}
                stroke="#333"
                strokeWidth="1"
                data-testid="node-circle"
              />
              <text
                x="20"
                y="5"
                fontSize="12"
                textAnchor="start"
                fill="#333"
              >
                {node.label}
              </text>
            </g>
          ))}
        </svg>
      </div>
    </div>
  );
}

export default App;
