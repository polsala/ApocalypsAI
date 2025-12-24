import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';

const forecastData = [
  { day: 'Monday', emoji: '☀️' },
  { day: 'Tuesday', emoji: '☁️' },
  { day: 'Wednesday', emoji: '🌧️' },
  { day: 'Thursday', emoji: '⛈️' },
  { day: 'Friday', emoji: '❄️' },
];

function EmojiWeatherForecast() {
  const [visible, setVisible] = useState(true);

  return (
    <div>
      <h1>Emoji Weather Forecast</h1>
      <button onClick={() => setVisible(!visible)}>
        {visible ? 'Hide Forecast' : 'Show Forecast'}
      </button>
      {visible && (
        <ul>
          {forecastData.map((item, idx) => (
            <li key={idx}>
              {item.day}: {item.emoji}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

const root = createRoot(document.getElementById('app'));
root.render(<EmojiWeatherForecast />);
