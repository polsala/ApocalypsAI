import React from 'react';

const affirmations = [
  "You are stronger than the wasteland.",
  "Every day above ground is a victory.",
  "Your resilience echoes across the ruins.",
  "Adapt. Survive. Thrive."
];

function AffirmationBoard() {
  const randomAffirmation = affirmations[Math.floor(Math.random() * affirmations.length)];
  return (
    <div className="affirmation-board">
      <h2>Daily Affirmation</h2>
      <blockquote>{randomAffirmation}</blockquote>
    </div>
  );
}

export default AffirmationBoard;
