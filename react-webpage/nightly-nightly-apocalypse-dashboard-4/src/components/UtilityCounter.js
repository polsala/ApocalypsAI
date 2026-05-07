import React from 'react';

function UtilityCounter({ utilityCounts }) {
  return (
    <section className="dashboard-section">
      <h2>Utility Counts</h2>
      <ul>
        {Object.entries(utilityCounts).map(([classifier, count]) => (
          <li key={classifier}>
            <strong>{classifier}</strong>: {count}
          </li>
        ))}
      </ul>
    </section>
  );
}

export default UtilityCounter;
