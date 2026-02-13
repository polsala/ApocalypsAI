import React, { useState } from "react";

const moodMap = {
  happy: ["😄", "😊", "🥳"],
  sad: ["😢", "☔", "😞"],
  excited: ["🤩", "🚀", "🎉"],
  angry: ["😡", "🔥", "💢"],
  relaxed: ["😌", "🌴", "🧘"]
};

const fallbackEmojis = ["🤔", "❓", "🧐"];

export default function App() {
  const [mood, setMood] = useState("");
  const [emojis, setEmojis] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const key = mood.trim().toLowerCase();
    setEmojis(moodMap[key] || fallbackEmojis);
  };

  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>Emoji Moodboard</h1>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Enter a mood (e.g., happy)"
          value={mood}
          onChange={(e) => setMood(e.target.value)}
          aria-label="mood-input"
        />
        <button type="submit">Show Emojis</button>
      </form>
      <div style={{ marginTop: "1rem", fontSize: "2rem" }} aria-label="emoji-output">
        {emojis.map((e, i) => (
          <span key={i} style={{ margin: "0 0.5rem" }}>
            {e}
          </span>
        ))}
      </div>
    </div>
  );
}
