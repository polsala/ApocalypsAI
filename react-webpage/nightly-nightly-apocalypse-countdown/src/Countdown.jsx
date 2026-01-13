import React, { useState, useEffect } from "react";

function Countdown({ target }) {
  const calculate = () => {
    const now = Date.now();
    const diff = Math.max(0, target - now);
    const seconds = Math.floor(diff / 1000) % 60;
    const minutes = Math.floor(diff / (1000 * 60)) % 60;
    const hours = Math.floor(diff / (1000 * 60 * 60)) % 24;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    return { days, hours, minutes, seconds };
  };

  const [time, setTime] = useState(calculate());

  useEffect(() => {
    const id = setInterval(() => setTime(calculate()), 1000);
    return () => clearInterval(id);
  }, [target]);

  const messages = [
    "The sky cracks open...",
    "Rats are gathering...",
    "The last pizza slice is near...",
    "Brace yourself!"
  ];
  const msg = messages[Math.floor(Math.random() * messages.length)];

  return (
    <div>
      <h2>Apocalypse Countdown</h2>
      <p>{msg}</p>
      <p>{time.days}d {time.hours}h {time.minutes}m {time.seconds}s</p>
    </div>
  );
}

export default Countdown;

