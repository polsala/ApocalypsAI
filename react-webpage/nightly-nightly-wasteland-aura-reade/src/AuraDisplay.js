import React from 'react';

const AuraDisplay = ({ auraType, auraColor }) => {
  if (!auraType) {
    return null;
  }

  return (
    <div style={{
      marginTop: '30px',
      padding: '25px',
      borderRadius: '10px',
      backgroundColor: auraColor,
      color: '#FFFFFF',
      textAlign: 'center',
      fontSize: '1.8em',
      fontWeight: 'bold',
      boxShadow: '0 4px 15px rgba(0, 0, 0, 0.3)',
      transition: 'background-color 0.5s ease-in-out, transform 0.2s ease-out',
      transform: 'scale(1)',
      width: '80%',
      maxWidth: '500px'
    }}>
      Detected Aura: {auraType}
    </div>
  );
};

export default AuraDisplay;
