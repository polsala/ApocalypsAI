import React, { useState, useEffect } from "react";

const THEMES = {
  morning: ["☀️","🌅","🥐","☕","🐦"],
  afternoon: ["🌞","🍹","🏖️","🕶️","🚲"],
  evening: ["🌇","🍷","🎶","🛋️","📚"],
  night: ["🌙","⭐","🛏️","🌌","🦉"]
};

function getTheme(hour) {
  if (hour >= 5 && hour < 12) return "morning";
  if (hour >= 12 && hour < 17) return "afternoon";
  if (hour >= 17 && hour < 21) return "evening";
  return "night";
}

function randomSelection(arr, count) {
  const copy = [...arr];
  const result = [];
  for (let i = 0; i < count && copy.length > 0; i++) {
    const idx = Math.floor(Math.random() * copy.length);
    result.push(copy.splice(idx, 1)[0]);
  }
  return result;
}

export default function App() {
  const [emojiList, setEmojiList] = useState([]);

  const generate = () => {
    const hour = new Date().getHours();
    const theme = getTheme(hour);
    const emojis = randomSelection(THEMES[theme], 5);
    setEmojiList(emojis);
  };

  useEffect(() => {
    generate();
  }, []);

  return (
    <div style={{fontFamily:"sans-serif",textAlign:"center",marginTop:"2rem"}}>
      <h1>Emoji Moodboard</h1>
      <div data-testid="emoji" style={{fontSize:"2rem",margin:"1rem"}}>
        {emojiList.map((e,i)=> <span key={i}>{e} </span>)}
      </div>
      <button onClick={generate}>Refresh</button>
    </div>
  );
}
