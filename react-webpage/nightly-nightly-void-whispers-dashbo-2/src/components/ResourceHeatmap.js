import React from 'react';

const ResourceHeatmap = () => {
  const zones = [
    { name: 'Zone A', water: 80, food: 60, tech: 40 },
    { name: 'Zone B', water: 30, food: 90, tech: 70 },
    { name: 'Zone C', water: 60, food: 40, tech: 90 },
  ];

  return (
    <div>
      <h2>Resource Heatmap</h2>
      <table>
        <thead>
          <tr>
            <th>Zone</th>
            <th>Water</th>
            <th>Food</th>
            <th>Tech</th>
          </tr>
        </thead>
        <tbody>
          {zones.map((zone, idx) => (
            <tr key={idx}>
              <td>{zone.name}</td>
              <td style={{ backgroundColor: `rgba(0, 0, 255, ${zone.water / 100})` }}>{zone.water}%</td>
              <td style={{ backgroundColor: `rgba(0, 255, 0, ${zone.food / 100})` }}>{zone.food}%</td>
              <td style={{ backgroundColor: `rgba(255, 0, 0, ${zone.tech / 100})` }}>{zone.tech}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ResourceHeatmap;
