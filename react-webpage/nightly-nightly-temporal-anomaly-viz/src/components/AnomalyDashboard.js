import React, { useEffect, useState } from 'react';
import AnomalyCard from './AnomalyCard';
import mockAnomalies from '../data/mockAnomalies'; // # Mock rationale: Using mock data for deterministic, offline demonstration and testing.

const AnomalyDashboard = () => {
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Simulate fetching data from an API
    const fetchAnomalies = () => {
      return new Promise((resolve) => {
        setTimeout(() => {
          // In a real app, this would be a fetch() call
          resolve(mockAnomalies);
        }, 500); // Simulate network delay
      });
    };

    fetchAnomalies()
      .then(data => {
        setAnomalies(data);
      })
      .catch(err => {
        setError('Failed to load anomalies.');
        console.error(err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading temporal anomalies...</p>;
  }

  if (error) {
    return <p style={{ color: 'red' }}>Error: {error}</p>;
  }

  return (
    <div className="anomaly-dashboard">
      {anomalies.length === 0 ? (
        <p>No temporal anomalies detected. All clear!</p>
      ) : (
        anomalies.map(anomaly => (
          <AnomalyCard key={anomaly.id} anomaly={anomaly} />
        ))
      )}
    </div>
  );
};

export default AnomalyDashboard;
