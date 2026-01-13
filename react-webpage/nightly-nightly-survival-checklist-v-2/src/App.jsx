import React, { useState } from 'react';

const tasks = [
  { id: 1, text: 'Find water' },
  { id: 2, text: 'Build shelter' },
  { id: 3, text: 'Collect firewood' },
  { id: 4, text: 'Secure food' },
];

function App() {
  const [completed, setCompleted] = useState([]);

  const toggle = id => {
    setCompleted(prev =>
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  const progress = Math.round((completed.length / tasks.length) * 100);

  return (
    <div>
      <h1>Survival Checklist</h1>
      <progress role="progressbar" value={progress} max="100">{progress}%</progress>
      <ul>
        {tasks.map(task => (
          <li key={task.id}>
            <label>
              <input
                type="checkbox"
                checked={completed.includes(task.id)}
                onChange={() => toggle(task.id)}
              />
              {task.text}
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
