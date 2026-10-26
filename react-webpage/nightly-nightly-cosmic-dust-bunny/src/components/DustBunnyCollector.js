import React, { useState } from 'react';
import '../styles/DustBunny.css';

function DustBunnyCollector({ onAddBunny }) {
  const [bunnyDescription, setBunnyDescription] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddBunny(bunnyDescription);
    setBunnyDescription('');
  };

  return (
    <form className="dust-bunny-collector" onSubmit={handleSubmit}>
      <input
        type="text"
        value={bunnyDescription}
        onChange={(e) => setBunnyDescription(e.target.value)}
        placeholder="What tiny cosmic thought did you find?"
        aria-label="Dust bunny description"
      />
      <button type="submit">Collect Dust Bunny</button>
    </form>
  );
}

export default DustBunnyCollector;
