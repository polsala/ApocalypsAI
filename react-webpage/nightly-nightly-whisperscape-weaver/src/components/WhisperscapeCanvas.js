import React from 'react';
import './WhisperscapeCanvas.css';

function WhisperscapeCanvas({ whispers }) {
  return (
    <div className="whisperscape-canvas">
      <h2>The Whisperscape</h2>
      {whispers.length === 0 ? (
        <p className="no-whispers">No whispers yet. Be the first to weave one!</p>
      ) : (
        <div className="whisper-grid">
          {whispers.map((whisper) => (
            <div key={whisper.id} className="whisper-bubble">
              {whisper.text}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default WhisperscapeCanvas;
