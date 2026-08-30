import React from 'react';

const allResourceTypes = ['All', 'Water', 'Food', 'Scrap', 'Fuel', 'Meds', 'Tools'];

function ResourceFilter({ activeFilter, onFilterChange }) {
  return (
    <div className="resource-filter">
      {allResourceTypes.map((type) => (
        <button
          key={type}
          className={activeFilter === type ? 'active' : ''}
          onClick={() => onFilterChange(type)}
        >
          {type}
        </button>
      ))}
    </div>
  );
}

export default ResourceFilter;
