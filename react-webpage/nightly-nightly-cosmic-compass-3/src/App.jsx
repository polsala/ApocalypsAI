import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data for celestial bodies and scenarios
const celestialBodies = [
  { id: 1, name: 'Sol', type: 'star', baseReadiness: 0.8 },
  { id: 2, name: 'Terra', type: 'planet', baseReadiness: 0.6 },
  { id: 3, name: 'Luna', type: 'moon', baseReadiness: 0.7 },
  { id: 4, name: 'Mars', type: 'planet', baseReadiness: 0.5 },
  { id: 5, name: 'Jupiter', type: 'planet', baseReadiness: 0.4 },
  { id: 6, name: 'Andromeda', type: 'galaxy', baseReadiness: 0.9 },
];

const scenarios = [
  { id: 1, name: 'Solar Flare Frenzy', params: { solarActivity: 1.5, radiationShielding: 0.7 } },
  { id: 2, name: 'Asteroid Avalanche', params: { asteroidDensity: 2.0, gravitationalPull: 0.9 } },
  { id: 3, name: 'Cosmic Dust Bunny Infestation', params: { dustConcentration: 1.8, atmosphericFilter: 0.5 } },
  { id: 4, name: 'Nebula Nuisance', params: { nebulaDensity: 1.2, magneticFieldStrength: 0.8 } },
  { id: 5, name: 'Black Hole Breeze', params: { proximityToBlackHole: 0.3, eventHorizonStability: 0.2 } },
];

function calculateReadiness(body, scenario) {
  let readiness = body.baseReadiness;
  switch (scenario.name) {
    case 'Solar Flare Frenzy':
      if (body.type === 'star') readiness *= scenario.params.solarActivity;
      if (body.type === 'planet' || body.type === 'moon') readiness *= scenario.params.radiationShielding;
      break;
    case 'Asteroid Avalanche':
      if (body.type === 'planet' || body.type === 'moon') readiness *= (1 - (scenario.params.asteroidDensity / 5)); // Higher density = lower readiness
      readiness *= scenario.params.gravitationalPull;
      break;
    case 'Cosmic Dust Bunny Infestation':
      if (body.type === 'planet' || body.type === 'moon') readiness *= scenario.params.atmosphericFilter;
      readiness *= (1 - (scenario.params.dustConcentration / 5));
      break;
    case 'Nebula Nuisance':
      if (body.type === 'planet' || body.type === 'moon') readiness *= scenario.params.magneticFieldStrength;
      readiness *= (1 - (scenario.params.nebulaDensity / 3));
      break;
    case 'Black Hole Breeze':
      if (body.type === 'planet' || body.type === 'moon') readiness *= scenario.params.eventHorizonStability;
      readiness *= (1 - scenario.params.proximityToBlackHole);
      break;
    default:
      break;
  }
  return Math.max(0, Math.min(1, readiness)).toFixed(2);
}

function CelestialBody({ body, readiness }) {
  const readinessColor = readiness > 0.7 ? 'green' : readiness > 0.4 ? 'orange' : 'red';
  return (
    <div className={`celestial-body ${body.type}`}
         style={{ '--readiness-color': readinessColor, '--readiness-value': readiness }}
         title={`${body.name} (${body.type}) - Readiness: ${readiness}`}>
      {body.name}
    </div>
  );
}

function App() {
  const [selectedScenario, setSelectedScenario] = useState(scenarios[0]);
  const [readinessScores, setReadinessScores] = useState({});

  useEffect(() => {
    const scores = {};
    celestialBodies.forEach(body => {
      scores[body.id] = calculateReadiness(body, selectedScenario);
    });
    setReadinessScores(scores);
  }, [selectedScenario]);

  const handleScenarioChange = (event) => {
    const scenarioId = parseInt(event.target.value);
    const scenario = scenarios.find(s => s.id === scenarioId);
    setSelectedScenario(scenario);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Cosmic Compass</h1>
        <p>Navigating the cosmos through hypothetical doomsdays.</p>
      </header>
      <main>
        <div className="controls">
          <label htmlFor="scenario-select">Choose a Scenario:</label>
          <select id="scenario-select" value={selectedScenario.id} onChange={handleScenarioChange}>
            {scenarios.map(scenario => (
              <option key={scenario.id} value={scenario.id}>{scenario.name}</option>
            ))}
          </select>
        </div>
        <div className="celestial-map">
          {celestialBodies.map(body => (
            <CelestialBody key={body.id} body={body} readiness={readinessScores[body.id]} />
          ))}
        </div>
        <div className="scenario-details">
          <h2>{selectedScenario.name}</h2>
          <p>Parameters:</p>
          <ul>
            {Object.entries(selectedScenario.params).map(([key, value]) => (
              <li key={key}>{key}: {value}</li>
            ))}
          </ul>
        </div>
      </main>
      <footer>
        <p>&copy; 2023 ApocalypsAI. For whimsical purposes only.</p>
      </footer>
    </div>
  );
}

export default App;
