import React from 'react';

const Affirmations = ({ affirmation }) => {
  return (
    <p
      style={{
        marginTop: '20px',
        fontSize: '1.1em',
        fontStyle: 'italic',
        color: '#555',
        textAlign: 'center',
        maxWidth: '400px',
        margin: '20px auto 0 auto',
      }}
      aria-live="polite"
    >
      {affirmation}
    </p>
  );
};

export default Affirmations;
