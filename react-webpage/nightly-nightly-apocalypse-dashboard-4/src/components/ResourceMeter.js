import React from 'react';

function ResourceMeter({ scarcityLevel }) {
  const getMeterClass = (level) => {
    if (level < 30) return 'low';
    if (level < 70) return 'medium';
    return 'high';
  };

  return (
    <section className="dashboard-section">
      <h2>Resource Scarcity Meter</h2>
      <div className="meter-container">
        <div className={`meter-bar ${getMeterClass(scarcityLevel)}`} style={{ width: `${scarcityLevel}%` }}>
          {scarcityLevel}%
        </div>
      </div>
    </section>
  );
}

export default ResourceMeter;
