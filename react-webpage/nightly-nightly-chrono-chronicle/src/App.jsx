import React from 'react';
import { formatDate, getPrediction } from './date-utils';

const App = () => {
  const now = new Date();
  const formatted = formatDate(now);
  const prediction = getPrediction(now);
  return (
    <div style={{fontFamily: 'sans-serif', padding: '2rem'}}>{'
'}      <h1>Apocalypse Chrono Chronicle</h1>{'
'}      <p>Today is {formatted}.</p>{'
'}      <p>{prediction}</p>{'
'}    </div>
  );
};

export default App;
