import React from 'react';

const ShelterIntegrityChart = () => {
  // Mock data for shelter integrity
  const data = [90, 85, 80, 78, 75];

  return (
    <div className="shelter-chart">
      <h2>Shelter Integrity Over Time</h2>
      <div style={{ display: 'flex', alignItems: 'flex-end', height: '100px' }}>
        {data.map((value, index) => (
          <div
            key={index}
            style={{
              width: '30px',
              height: `${value}px`,
              backgroundColor: 'green',
              margin: '0 5px',
              border: '1px solid black'
            }}
          ></div>
        ))}
      </div>
    </div>
  );
};

export default ShelterIntegrityChart;
