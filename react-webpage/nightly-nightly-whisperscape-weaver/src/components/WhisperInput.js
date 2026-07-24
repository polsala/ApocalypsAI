import React, { useState } from 'react';
import './WhisperInput.css';

function WhisperInput({ onAddWhisper }) {
  const [whisperText, setWhisperText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddWhisper(whisperText);
    setWhisperText('');
  };

  return (
    <form className="whisper-input-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={whisperText}
        onChange={(e) => setWhisperText(e.target.value)}
        placeholder="Type your whisper here..."
        maxLength="140"
        aria-label="Whisper input"
      />
      <button type="submit" disabled={!whisperText.trim()}>
        Weave Whisper
      </button>
    </form>
  );
}

export default WhisperInput;
