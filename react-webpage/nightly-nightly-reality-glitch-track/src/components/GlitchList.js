import React from 'react';
import GlitchItem from './GlitchItem';

function GlitchList({ glitches }) {
  return (
    <div className="glitch-list-container">
      <h2>Reported Glitches</h2>
      {glitches.length === 0 ? (
        <p style={{ textAlign: 'center', color: '#bbb' }}>No glitches reported yet. All clear... for now.</p>
      ) : (
        <div>
          {glitches.map((glitch) => (
            <GlitchItem key={glitch.id} glitch={glitch} />
          ))}
        </div>
      )}
    </div>
  );
}

export default GlitchList;
