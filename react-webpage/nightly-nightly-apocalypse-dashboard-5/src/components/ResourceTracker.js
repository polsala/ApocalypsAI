import React from 'react';

function ResourceTracker({ resources }) {
  return (
    <section className="resource-tracker">
      <h2>Survival Resource Status</h2>
      <ul>
        {Object.entries(resources).map(([resource, value]) => (
          <li key={resource}>
            {resource.charAt(0).toUpperCase() + resource.slice(1)}: {value}%
            <div className="progress-bar-container">
              <div 
                className="progress-bar"
                style={{ width: `${value}%`, backgroundColor: value > 50 ? 'lightgreen' : value > 20 ? 'gold' : 'salmon' }}
              ></div>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default ResourceTracker;
