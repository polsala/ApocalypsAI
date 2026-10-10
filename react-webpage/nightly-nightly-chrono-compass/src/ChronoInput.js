import React, { useState } from 'react';

function ChronoInput({ onAddEntry }) {
  const [energy, setEnergy] = useState(5);
  const [focus, setFocus] = useState(5);
  const [timeSpeed, setTimeSpeed] = useState(5); // 1=very slow, 5=normal, 10=very fast

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddEntry({ energy, focus, timeSpeed });
    // Reset for next entry, or keep current values
    setEnergy(5);
    setFocus(5);
    setTimeSpeed(5);
  };

  return (
    <div className="chrono-input-container">
      <h2>Log Your Current Temporal State</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="energy">Energy Level: <span>{energy}/10</span></label>
          <input
            type="range"
            id="energy"
            min="1"
            max="10"
            value={energy}
            onChange={(e) => setEnergy(parseInt(e.target.value))}
          />
        </div>
        <div className="input-group">
          <label htmlFor="focus">Focus Level: <span>{focus}/10</span></label>
          <input
            type="range"
            id="focus"
            min="1"
            max="10"
            value={focus}
            onChange={(e) => setFocus(parseInt(e.target.value))}
          />
        </div>
        <div className="input-group">
          <label htmlFor="timeSpeed">Perceived Time Speed: <span>{timeSpeed}/10</span></label>
          <input
            type="range"
            id="timeSpeed"
            min="1"
            max="10"
            value={timeSpeed}
            onChange={(e) => setTimeSpeed(parseInt(e.target.value))}
          />
          <small>(1=Very Slow, 5=Normal, 10=Very Fast)</small>
        </div>
        <button type="submit">Log Entry</button>
      </form>
    </div>
  );
}

export default ChronoInput;
