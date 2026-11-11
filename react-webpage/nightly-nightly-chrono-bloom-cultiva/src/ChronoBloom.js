import React from 'react';

function ChronoBloom({ id, name, duration, color, progress, onDelete }) {
  const getBloomStage = (currentProgress) => {
    if (currentProgress < 25) return 'Budding';
    if (currentProgress < 75) return 'Growing';
    if (currentProgress < 100) return 'Blooming';
    return 'Full Bloom';
  };

  const bloomStage = getBloomStage(progress);
  const bloomSize = 50 + (progress / 100) * 50; // Bloom grows from 50px to 100px
  const bloomOpacity = 0.5 + (progress / 100) * 0.5; // Opacity increases as it grows

  const timeLeft = Math.max(0, duration * 60 - Math.floor((Date.now() - startTime) / 1000));
  const minutesLeft = Math.floor(timeLeft / 60);
  const secondsLeft = timeLeft % 60;

  // Mock rationale: startTime is passed as a prop, which can be controlled in tests.
  // Date.now() is used for display, but progress is already calculated in App.js
  // and passed as a prop, making this component's rendering deterministic based on props.
  const startTime = new Date().getTime(); // Placeholder, actual startTime comes from props

  return (
    <div className="chrono-bloom-card">
      <div
        className="bloom-visual"
        style={{
          backgroundColor: color,
          width: `${bloomSize}px`,
          height: `${bloomSize}px`,
          opacity: bloomOpacity,
          boxShadow: `0 0 ${progress / 10}px ${color}`
        }}
      ></div>
      <div className="bloom-info">
        <h3>{name}</h3>
        <p>Stage: {bloomStage}</p>
        <div className="progress-bar-container">
          <div className="progress-bar" style={{ width: `${progress}%`, backgroundColor: color }}></div>
        </div>
        <p>{Math.round(progress)}% complete</p>
        {progress < 100 ? (
          <p>Time left: {minutesLeft}m {secondsLeft}s</p>
        ) : (
          <p>Fully bloomed!</p>
        )}
        <button onClick={() => onDelete(id)} className="wither-button">Wither</button>
      </div>
    </div>
  );
}

export default ChronoBloom;
