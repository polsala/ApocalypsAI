import React from 'react';

const forecast = [
  { day: 'Today', condition: 'Ashfall', temp: '32°F' },
  { day: 'Tomorrow', condition: 'Radiation Storm', temp: '28°F' },
  { day: 'Day After', condition: 'Clear Skies', temp: '35°F' }
];

function WeatherForecast() {
  return (
    <div className="weather-forecast">
      <h2>Wasteland Weather</h2>
      <ul>
        {forecast.map((day, index) => (
          <li key={index}>
            <strong>{day.day}</strong>: {day.condition}, {day.temp}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default WeatherForecast;
