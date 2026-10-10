import React from 'react';
import '../styles/DustBunny.css';

function DustBunnyDisplay({ dustBunnies }) {
  return (
    <div className="dust-bunny-display">
      <h2>Your Cosmic Collection ({dustBunnies.length})</h2>
      {dustBunnies.length === 0 ? (
        <p className="no-bunnies">The cosmic chamber is pristine... for now!</p>
      ) : (
        <ul className="bunny-list">
          {dustBunnies.map((bunny) => (
            <li key={bunny.id} className="dust-bunny-item">
              <span className="bunny-icon">✨</span>
              <span className="bunny-description">{bunny.description}</span>
              <span className="bunny-timestamp">Collected: {new Date(bunny.collectedAt).toLocaleTimeString()}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default DustBunnyDisplay;
