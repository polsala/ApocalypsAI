import React from "react";
import { moods } from "./moodData";

function hashDate(dateStr) {
  // simple deterministic hash: sum char codes
  let hash = 0;
  for (let i = 0; i < dateStr.length; i++) {
    hash = (hash + dateStr.charCodeAt(i)) % moods.length;
  }
  return hash;
}

export default function App() {
  const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  const idx = hashDate(today);
  const { phrase, color } = moods[idx];

  const style = {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: color,
    color: "#222",
    fontFamily: "sans-serif",
    fontSize: "2rem"
  };

  return (
    <div style={style}>
      {phrase}
    </div>
  );
}
