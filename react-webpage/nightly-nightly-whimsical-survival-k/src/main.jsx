import React, { useState } from 'react';
import WhimsyItems from './whimsy-items';

const App = () => {
  const [items, setItems] = useState([]);
  const [scenario, setScenario] = useState('post-apocalyptic');
  const [whimsyLevel, setWhimsy] = useState(50);

  const addItem = (item) => {
    setItems([...items, item]);
  };

  const generateWhimsy = () => {
    const randomItems = WhimsyItems[scenario]
      .sort(() => 0.5 - Math.random())
      .slice(0, Math.ceil(WhimsyItems[scenario].length * whimsyLevel/100));
    return randomItems;
  };

  return (
    <div className="container">
      <h1>🧳 Whimsical Survival Kit Builder</h1>
      <ScenarioSelector value={scenario} onChange={setScenario} />
      <WhimsySlider value={whimsyLevel} onChange={setWhimsy} />
      <KitBuilder items={items} addItem={addItem} />
      <ExportKit items={generateWhimsy()} />
    </div>
  );
};

export default App;
