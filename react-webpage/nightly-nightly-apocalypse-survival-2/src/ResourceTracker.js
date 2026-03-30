import React from 'react';

const ResourceTracker = ({ resources }) => {
  return (
    <div className="resource-tracker">
      <h2>Resource Levels</h2>
      <ul>
        <li>Water: {resources.water}%</li>
        <li>Food: {resources.food}%</li>
        <li>Ammunition: {resources.ammo}%</li>
      </ul>
    </div>
  );
};

export default ResourceTracker;
