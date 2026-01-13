import React, { useState, useEffect } from 'react';
import './App.css';

function getEmojiForHour(hour) {
  // 12â¯pm â 1â¯pm is the âovercastâ surprise hour
  if (hour === 12) {
    return 'âï¸';
  }
  // Daytime: 6â¯am â 5â¯pm (inclusive)
  if (hour >= 6 && hour <= 17) {
    return 'ð';
  }
  // Nighttime: otherwise
  return 'ð';
}

function formatTime(date) {
  const hrs = String(date.getHours()).padStart(2, '0');
  const mins = String(date.getMinutes()).padStart(2, '0');
  const secs = String(date.getSeconds()).padStart(2, '0');
  return `${hrs}:${mins}:${secs}`;
}

export default function App() {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const emoji = getEmojiForHour(now.getHours());

  return (
    <div className="clock-container">
      <h1 className="time">{formatTime(now)}</h1>
      <div className="emoji" aria-label="weather emoji">{emoji}</div>
      <p className="caption">Current hour: {now.getHours()}</p>
    </div>
  );
}

