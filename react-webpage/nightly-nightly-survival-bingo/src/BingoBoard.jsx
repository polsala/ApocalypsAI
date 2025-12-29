import React, { useState } from 'react';

export default function BingoBoard({ board }) {
  const [checked, setChecked] = useState(Array(25).fill(false));

  const toggle = (idx) => {
    const newChecked = [...checked];
    newChecked[idx] = !newChecked[idx];
    setChecked(newChecked);
  };

  return (
    <div className="board">
      {board.flat().map((text, idx) => (
        <div
          key={idx}
          className={`cell ${checked[idx] ? 'checked' : ''}`}
          onClick={() => toggle(idx)}
        >
          {text}
        </div>
      ))}
    </div>
  );
}
