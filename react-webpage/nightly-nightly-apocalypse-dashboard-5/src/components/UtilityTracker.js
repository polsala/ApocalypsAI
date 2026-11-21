import React from 'react';

function UtilityTracker({ data }) {
  return (
    <section className="utility-tracker">
      <h2>Utility Generation Tracker</h2>
      {data && Object.keys(data).length > 0 ? (
        <ul>
          {Object.entries(data).map(([classifier, count]) => (
            <li key={classifier}>
              <span className="classifier-name">{classifier}</span>
              <span className="count">{count}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p>No utility generation data available. The utility bots are still booting up.</p>
      )}
    </section>
  );
}

export default UtilityTracker;
