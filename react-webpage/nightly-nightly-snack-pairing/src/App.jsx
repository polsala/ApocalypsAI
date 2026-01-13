import React, { useState } from 'react';
import { getPairings } from './utils/pairings.js';

const snacks = ['Chocolate', 'Cheese', 'Fruit', 'Nuts', 'Crackers', 'Salsa', 'Popcorn'];

export default function App() {
  const [selected, setSelected] = useState([]);
  const [pairings, setPairings] = useState([]);

  const toggleSnack = (snack) => {
    const newSelected = selected.includes(snack)
      ? selected.filter((s) => s !== snack)
      : [...selected, snack];
    setSelected(newSelected);
    setPairings(getPairings(newSelected));
  };

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '1rem' }}>
      <h1>Snack Pairing Calculator</h1>
      <p>Select your snacks:</p>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
        {snacks.map((snack) => (
          <button
            key={snack}
            onClick={() => toggleSnack(snack)}
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: selected.includes(snack) ? '#4caf50' : '#e0e0e0',
              color: selected.includes(snack) ? '#fff' : '#000',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            {snack}
          </button>
        ))}
      </div>
      <h2>Suggested Pairings:</h2>
      {pairings.length === 0 ? (
        <p>No snacks selected.</p>
      ) : (
        <ul>
          {pairings.map((p, idx) => (
            <li key={idx}>{p}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
