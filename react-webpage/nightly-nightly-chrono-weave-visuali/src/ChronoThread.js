/**
 * @file ChronoThread.js
 * @description React component for rendering a single chrono-thread with anomaly effects.
 */

import React from 'react';

const ChronoThread = ({ id, points, isAnomalous }) => {
  // Convert points array to SVG path 'd' attribute string
  const pathData = points.map((p, i) => {
    if (i === 0) return `M${p.x},${p.y}`;
    return `L${p.x},${p.y}`;
  }).join(' ');

  return (
    <path
      id={`chrono-thread-${id}`}
      className={`chrono-thread ${isAnomalous ? 'anomalous' : ''}`}
      d={pathData}
      stroke="#6246ea"
    />
  );
};

export default React.memo(ChronoThread);
