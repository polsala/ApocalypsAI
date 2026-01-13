import React, { useState } from 'react';
import { zones, conditions } from './data';

function randomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

export default function App() {
  const [forecast, setForecast] = useState('');
  const generate = () => {
    const zone = randomItem(zones);
    const condition = randomItem(conditions);
    setForecast(`${zone}: ${condition}`);
  };
  return (
    <div style={{fontFamily: 'sans-serif', padding: '2rem'}}>*
      <h1>Apocalyptic Forecast Generator</h1>
      <button onClick={generate}>Generate Forecast</button>
      {forecast && <p data-testid="forecast">{forecast}</p>}
    </div>
  );
}
