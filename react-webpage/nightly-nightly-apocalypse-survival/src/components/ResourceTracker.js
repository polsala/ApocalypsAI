import React from 'react';

const resources = [
  { name: 'Water', level: 75 },
  { name: 'Food', level: 60 },
  { name: 'Ammo', level: 40 },
  { name: 'Shelter Integrity', level: 90 }
];

function ResourceTracker() {
  return (
    <div className="resource-tracker">
      <h2>Resources</h2>
      <ul>
        {resources.map((res, index) => (
          <li key={index}>
            {res.name}: {res.level}%
            <progress value={res.level} max="100"></progress>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ResourceTracker;
