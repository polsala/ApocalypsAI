import React from 'react';

const MoodRing = ({ moodColor }) => {
  return (
    <div
      style={{
        width: '150px',
        height: '150px',
        borderRadius: '50%',
        backgroundColor: moodColor,
        border: '5px solid #333',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontSize: '1.2em',
        fontWeight: 'bold',
        color: '#fff',
        textShadow: '1px 1px 2px rgba(0,0,0,0.5)',
        transition: 'background-color 0.5s ease-in-out',
        margin: '30px auto',
      }}
      aria-label="Mood Ring"
    >
      {/* Optional: Display current mood text inside */}
    </div>
  );
};

export default MoodRing;
