import React from 'react';

const CorrectionSuggestions = ({ region }) => {
  const getCorrectionSeverity = (drift) => {
    if (drift > 0.2) return 'Critical';
    if (drift > 0.1) return 'High';
    if (drift > 0.05) return 'Moderate';
    return 'Low';
  };

  const getCorrectionAction = (drift) => {
    if (drift > 0.2) return 'Immediate Chrono-Stabilization Protocol required. Deploy Temporal Anchors.';
    if (drift > 0.1) return 'Prioritize Temporal Flux Recalibration. Monitor closely.';
    if (drift > 0.05) return 'Routine Temporal Field Adjustment recommended.';
    return 'Temporal field within acceptable parameters. Maintain vigilance.';
  };

  return (
    <div style={{
      border: '1px solid #555',
      borderRadius: '4px',
      padding: '15px',
      backgroundColor: '#2f3136',
      marginTop: '10px'
    }}>
      <h2 style={{ color: '#61dafb', marginBottom: '10px' }}>Correction Suggestions for {region.name}</h2>
      <p><strong>Stability:</strong> <span style={{ color: region.stability > 0.8 ? '#4CAF50' : region.stability > 0.5 ? '#FFC107' : '#F44336' }}>{(region.stability * 100).toFixed(1)}%</span></p>
      <p><strong>Temporal Drift:</strong> <span style={{ color: region.drift > 0.2 ? '#F44336' : region.drift > 0.1 ? '#FFC107' : '#4CAF50' }}>{(region.drift * 100).toFixed(1)}%</span></p>
      <p><strong>Severity:</strong> <span style={{ color: region.drift > 0.2 ? '#F44336' : region.drift > 0.1 ? '#FFC107' : '#4CAF50' }}>{getCorrectionSeverity(region.drift)}</span></p>
      <p><strong>Recommended Action:</strong> {getCorrectionAction(region.drift)}</p>
    </div>
  );
};

export default CorrectionSuggestions;
