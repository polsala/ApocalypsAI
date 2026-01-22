import React, { useState, useEffect } from 'react';
import './App.css';

const affirmations = [
  "You are a star made of star stuff.",
  "The void whispers your name in stardust.",
  "Your thoughts ripple through space-time.",
  "You are the calm in the cosmic storm.",
  "Every line of code you write echoes in eternity.",
  "You are not lost — you are exploring.",
  "The universe conspires in your favor.",
  "You are a glitch in the matrix — in a good way."
];

function App() {
  const [currentAffirmation, setCurrentAffirmation] = useState("");

  const getRandomAffirmation = () => {
    const index = Math.floor(Math.random() * affirmations.length);
    setCurrentAffirmation(affirmations[index]);
  };

  useEffect(() => {
    getRandomAffirmation();
  }, []);

  return (
    <div className="terminal">
      <div className="header">> void-whispers.exe</div>
      <div className="content">
        <p>{currentAffirmation}</p>
        <button onClick={getRandomAffirmation}>// next_message</button>
      </div>
    </div>
  );
}

export default App;
