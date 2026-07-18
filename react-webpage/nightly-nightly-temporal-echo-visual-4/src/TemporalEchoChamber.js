import React, { useState } from 'react';
import TimelineVisualization from './TimelineVisualization';
import echoDataMap from './data/echoes.json'; // Import the mock data

function TemporalEchoChamber() {
  const [concept, setConcept] = useState('');
  const [echoes, setEchoes] = useState([]);

  const generateEchoes = () => {
    // # Mock rationale: For a standalone utility, we simulate echo generation
    // by looking up a predefined map or generating simple patterns.
    // In a real-world scenario, this would involve an API call to a language model
    // or a sophisticated knowledge graph.
    const lowerConcept = concept.toLowerCase();
    const generatedEchoes = echoDataMap[lowerConcept] || echoDataMap.default;

    // Add a unique ID and a random 'strength' for visualization purposes
    const enrichedEchoes = generatedEchoes.map((echo, index) => ({
      ...echo,
      id: `${lowerConcept}-${echo.term}-${index}`,
      strength: Math.floor(Math.random() * 50) + 50 // Random strength between 50-100
    }));
    setEchoes(enrichedEchoes);
  };

  return (
    <div className="echo-chamber">
      <div className="input-section">
        <input
          type="text"
          value={concept}
          onChange={(e) => setConcept(e.target.value)}
          placeholder="Enter a concept (e.g., 'banana', 'apocalypse', 'AI')"
          aria-label="Concept input"
        />
        <button onClick={generateEchoes}>Generate Echoes</button>
      </div>
      {echoes.length > 0 && (
        <div className="visualization-section">
          <h2>Temporal Echoes of "{concept}"</h2>
          <TimelineVisualization echoes={echoes} />
        </div>
      )}
    </div>
  );
}

export default TemporalEchoChamber;
