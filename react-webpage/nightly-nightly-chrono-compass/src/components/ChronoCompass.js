import React from 'react';

const ChronoCompass = ({ anomalies }) => {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'Critical': return '#e94560';
      case 'Moderate': return '#ff7b00';
      case 'Minor': return '#ffd700';
      default: return '#e0e0e0';
    }
  };

  return (
    <div style={styles.compassContainer}>
      <div style={styles.compassHeader}>
        <span role="img" aria-label="compass" style={styles.compassIcon}>🧭</span>
        <h2 style={styles.compassTitle}>Temporal Anomaly Log</h2>
      </div>
      {anomalies.length === 0 ? (
        <p>No temporal anomalies detected. All clear... for now.</p>
      ) : (
        <div style={styles.anomalyList}>
          {anomalies.map(anomaly => (
            <div key={anomaly.id} style={{
              ...styles.anomalyCard,
              borderColor: getSeverityColor(anomaly.severity)
            }}>
              <div style={styles.anomalyHeader}>
                <span style={{ ...styles.anomalySeverity, color: getSeverityColor(anomaly.severity) }}>
                  {anomaly.severity}
                </span>
                <span style={styles.anomalyTimestamp}>
                  {new Date(anomaly.timestamp).toLocaleString()}
                </span>
              </div>
              <h3 style={styles.anomalyType}>{anomaly.type}</h3>
              <p style={styles.anomalyDescription}>{anomaly.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const styles = {
  compassContainer: {
    backgroundColor: '#0f3460',
    borderRadius: '8px',
    padding: '20px',
    margin: '0 auto',
    maxWidth: '800px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)'
  },
  compassHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: '20px'
  },
  compassIcon: {
    fontSize: '2em',
    marginRight: '10px'
  },
  compassTitle: {
    color: '#a0a0a0',
    margin: 0
  },
  anomalyList: {
    display: 'grid',
    gap: '15px'
  },
  anomalyCard: {
    backgroundColor: '#1a1a2e',
    borderLeft: '5px solid',
    padding: '15px',
    borderRadius: '5px',
    textAlign: 'left'
  },
  anomalyHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '5px'
  },
  anomalySeverity: {
    fontWeight: 'bold'
  },
  anomalyTimestamp: {
    fontSize: '0.8em',
    color: '#a0a0a0'
  },
  anomalyType: {
    color: '#e0e0e0',
    margin: '5px 0'
  },
  anomalyDescription: {
    fontSize: '0.9em',
    color: '#c0c0c0'
  }
};

export default ChronoCompass;
