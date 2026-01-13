import React, { useState } from "react";

const weatherOptions = [
  { condition: "Acid rain", emoji: "âï¸", activity: "Dance under the drizzle" },
  { condition: "Radiation fog", emoji: "ð«ï¸", activity: "Play hideâandâseek with the glow" },
  { condition: "Solar flare", emoji: "âï¸", activity: "Sunâbathing with SPF 1000" },
  { condition: "Dust storm", emoji: "ðªï¸", activity: "Build a sandcastle" },
  { condition: "Glowing aurora", emoji: "ð", activity: "Stargaze and make wishes" }
];

function getRandom() {
  return weatherOptions[Math.floor(Math.random() * weatherOptions.length)];
}

export default function App() {
  const [forecast, setForecast] = useState(getRandom());

  const refresh = () => setForecast(getRandom());

  return (
    <div style={{ fontFamily: "sans-serif", textAlign: "center", marginTop: "2rem" }}>
      <h1>Apocalypse Weather Moodboard</h1>
      <p style={{ fontSize: "2rem" }}>{forecast.emoji} {forecast.condition}</p>
      <p>Suggested activity: <strong>{forecast.activity}</strong></p>
      <button onClick={refresh}>Refresh</button>
    </div>
  );
}

