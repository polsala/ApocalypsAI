import React, { useState } from "react";

const locations = [
  "Radiated Ruins",
  "Dusty Wasteland",
  "Neonâlit Megacity",
  "Frozen Bunker",
  "Sunken Subway",
  "Crumbling Cathedral"
];

const weatherConditions = [
  "acid rain",
  "radioactive dust storm",
  "electric sandstorm",
  "glowing fog",
  "mutated pollen bloom",
  "thermal vortex",
  "silent snowfall of ash"
];

function getRandomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

export default function App() {
  const [forecast, setForecast] = useState(() => ({
    location: getRandomItem(locations),
    condition: getRandomItem(weatherConditions)
  }));

  const refresh = () => {
    setForecast({
      location: getRandomItem(locations),
      condition: getRandomItem(weatherConditions)
    });
  };

  return (
    <div style={{ fontFamily: "sans-serif", textAlign: "center", marginTop: "2rem" }}>
      <h1>ð Apocalypse Weather Forecast ð</h1>
      <p>
        <strong>{forecast.location}</strong> is experiencing{' '}
        <em>{forecast.condition}</em>.
      </p>
      <button onClick={refresh}>Generate New Forecast</button>
    </div>
  );
}

