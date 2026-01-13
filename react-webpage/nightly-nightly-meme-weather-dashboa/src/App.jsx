import React, { useState } from "react";

const memes = [
  "https://i.imgur.com/1.jpg",
  "https://i.imgur.com/2.jpg",
  "https://i.imgur.com/3.jpg"
];

const fakeWeather = (city) => {
  const temps = ["âï¸ Sunny", "ð§ï¸ Rainy", "âï¸ Stormy", "âï¸ Snowy"];
  const idx = Math.floor(Math.random() * temps.length);
  return `${temps[idx]} in ${city}`;
};

export default function App() {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState("");
  const [memeIdx, setMemeIdx] = useState(0);

  const handleCityChange = (e) => setCity(e.target.value);
  const handleShowWeather = () => setWeather(fakeWeather(city));
  const nextMeme = () => setMemeIdx((memeIdx + 1) % memes.length);

  return (
    <div style={{ fontFamily: "sans-serif", padding: "1rem" }}>
      <h1>ð§­ Meme Weather Dashboard</h1>
      <div>
        <input
          placeholder="Enter city"
          value={city}
          onChange={handleCityChange}
          data-testid="city-input"
        />
        <button onClick={handleShowWeather} data-testid="weather-btn">
          Show Weather
        </button>
      </div>
      {weather && <p data-testid="weather-output">{weather}</p>}
      <div style={{ marginTop: "1rem" }}>
        <img
          src={memes[memeIdx]}
          alt="meme"
          width={300}
          data-testid="meme-image"
        />
        <br />
        <button onClick={nextMeme} data-testid="meme-btn">
          New Meme
        </button>
      </div>
    </div>
  );
}
