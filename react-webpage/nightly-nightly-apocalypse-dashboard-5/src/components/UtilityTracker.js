import React from 'react';
import './UtilityTracker.css';

function UtilityTracker({ data }) {
  return (
    <div className="utility-tracker-table">
      {data.length === 0 ? (
        <p>No utilities generated yet...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Utility Name</th>
              <th>Classifier</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.map(item => (
              <tr key={item.id} className={`status-${item.status.toLowerCase().replace(' ', '-')}`}>
                <td>{item.name}</td>
                <td>{item.classifier}</td>
                <td>{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default UtilityTracker;
