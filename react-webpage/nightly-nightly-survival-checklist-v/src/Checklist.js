import React, { useState } from 'react';

function Checklist({ items }) {
  const [checked, setChecked] = useState(() => items.reduce((acc, item) => ({ ...acc, [item.id]: false }), {}));

  const toggle = (id) => {
    setChecked((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const completed = Object.values(checked).filter(Boolean).length;
  const total = items.length;
  const progress = Math.round((completed / total) * 100);

  return (
    <div>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {items.map((item) => (
          <li key={item.id} style={{ marginBottom: '8px' }}>
            <label>
              <input
                type="checkbox"
                checked={checked[item.id]}
                onChange={() => toggle(item.id)}
                style={{ marginRight: '8px' }}
              />
              {item.text}
            </label>
          </li>
        ))}
      </ul>
      <div style={{ marginTop: '20px' }}>
        <progress value={completed} max={total} style={{ width: '100%' }} />
        <p>{completed} of {total} completed ({progress}%)</p>
      </div>
    </div>
  );
}

export default Checklist;
