import React, { useState, useEffect } from 'react';
import './App.css';

const MOOD_MESSAGES = {
  hopeful: {
    color: '#8BC34A', // Light Green
    message: 'The irradiated daisies are blooming! A good day to forage. The void seems... less void-y.'
  },
  cautious: {
    color: '#FFEB3B', // Yellow
    message: 'A faint hum on the horizon. Keep your eyes peeled, but don\'t panic... yet. The air smells faintly of ozone and regret.'
  },
  perilous: {
    color: '#F44336', // Red
    message: 'The void whispers your name, and it sounds hungry. Perhaps a good day to stay in the bunker. Don\'t forget your lucky lead-lined hat.'
  }
};

function App() {
  const [scavengerHaul, setScavengerHaul] = useState('moderate');
  const [mutantEncounters, setMutantEncounters] = useState('few');
  const [skyCondition, setSkyCondition] = useState('cloudy');
  const [waterSupply, setWaterSupply] = useState('adequate');
  const [currentMood, setCurrentMood] = useState(MOOD_MESSAGES.cautious);

  useEffect(() => {
    const calculateMood = () => {
      let score = 0;

      // Scavenger Haul Quality: poor (1), moderate (2), bountiful (3)
      if (scavengerHaul === 'poor') score += 1;
      else if (scavengerHaul === 'moderate') score += 2;
      else if (scavengerHaul === 'bountiful') score += 3;

      // Recent Mutant Encounters: many (1), few (2), none (3)
      if (mutantEncounters === 'many') score += 1;
      else if (mutantEncounters === 'few') score += 2;
      else if (mutantEncounters === 'none') score += 3;

      // Sky Condition: ominous-green-glow (1), cloudy (2), clear (3)
      if (skyCondition === 'ominous-green-glow') score += 1;
      else if (skyCondition === 'cloudy') score += 2;
      else if (skyCondition === 'clear') score += 3;

      // Water Supply: scarce (1), adequate (2), abundant (3)
      if (waterSupply === 'scarce') score += 1;
      else if (waterSupply === 'adequate') score += 2;
      else if (waterSupply === 'abundant') score += 3;

      // Determine mood based on score (min 4, max 12)
      if (score >= 10) {
        setCurrentMood(MOOD_MESSAGES.hopeful);
      } else if (score >= 7) {
        setCurrentMood(MOOD_MESSAGES.cautious);
      } else {
        setCurrentMood(MOOD_MESSAGES.perilous);
      }
    };

    calculateMood();
  }, [scavengerHaul, mutantEncounters, skyCondition, waterSupply]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Wasteland Mood Ring</h1>
        <p>Gauge the current vibe of the apocalypse!</p>
      </header>
      <div className="mood-container">
        <div className="mood-ring" style={{ backgroundColor: currentMood.color }}>
          <p className="mood-message">{currentMood.message}</p>
        </div>
        <div className="input-form">
          <div className="input-group">
            <label htmlFor="scavengerHaul">Scavenger Haul Quality:</label>
            <select id="scavengerHaul" value={scavengerHaul} onChange={(e) => setScavengerHaul(e.target.value)}>
              <option value="poor">Poor</option>
              <option value="moderate">Moderate</option>
              <option value="bountiful">Bountiful</option>
            </select>
          </div>

          <div className="input-group">
            <label htmlFor="mutantEncounters">Recent Mutant Encounters:</label>
            <select id="mutantEncounters" value={mutantEncounters} onChange={(e) => setMutantEncounters(e.target.value)}>
              <option value="none">None</option>
              <option value="few">Few</option>
              <option value="many">Many</option>
            </select>
          </div>

          <div className="input-group">
            <label htmlFor="skyCondition">Sky Condition:</label>
            <select id="skyCondition" value={skyCondition} onChange={(e) => setSkyCondition(e.target.value)}>
              <option value="clear">Clear</option>
              <option value="cloudy">Cloudy</option>
              <option value="ominous-green-glow">Ominous Green Glow</option>
            </select>
          </div>

          <div className="input-group">
            <label htmlFor="waterSupply">Water Supply:</label>
            <select id="waterSupply" value={waterSupply} onChange={(e) => setWaterSupply(e.target.value)}>
              <option value="abundant">Abundant</option>
              <option value="adequate">Adequate</option>
              <option value="scarce">Scarce</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
