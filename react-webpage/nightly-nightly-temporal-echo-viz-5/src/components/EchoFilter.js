import React from 'react';

function EchoFilter({ filters, onFilterChange, echoTypes }) {
  const handleTypeChange = (event) => {
    onFilterChange('type', event.target.value);
  };

  const handleMinIntensityChange = (event) => {
    onFilterChange('minIntensity', event.target.value === '' ? '' : parseInt(event.target.value, 10));
  };

  return (
    <div className="filters">
      <label htmlFor="echoType">Filter by Type:</label>
      <select id="echoType" value={filters.type} onChange={handleTypeChange}>
        <option value="">All Types</option>
        {echoTypes.map((type) => (
          <option key={type} value={type}>
            {type}
          </option>
        ))}
      </select>

      <label htmlFor="minIntensity">Min Intensity:</label>
      <input
        id="minIntensity"
        type="number"
        min="1"
        max="10"
        value={filters.minIntensity}
        onChange={handleMinIntensityChange}
        placeholder="1-10"
      />
    </div>
  );
}

export default EchoFilter;
