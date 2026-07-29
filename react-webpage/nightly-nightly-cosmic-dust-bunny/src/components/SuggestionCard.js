import React from 'react';

const SuggestionCard = ({ id, text, completed, onComplete }) => {
  const handleCompleteClick = () => {
    onComplete(id);
  };

  return (
    <div
      className="suggestion-card"
      style={{
        backgroundColor: completed ? '#4CAF50' : '#3a3f50',
        padding: '15px',
        margin: '10px 0',
        borderRadius: '5px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        boxShadow: '0 2px 5px rgba(0,0,0,0.3)',
        transition: 'background-color 0.3s ease'
      }}
    >
      <p style={{ margin: 0, textDecoration: completed ? 'line-through' : 'none', flexGrow: 1, textAlign: 'left' }}>
        {text}
      </p>
      {!completed && (
        <button
          onClick={handleCompleteClick}
          style={{
            backgroundColor: '#61dafb',
            color: '#282c34',
            border: 'none',
            padding: '8px 15px',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '0.9em',
            fontWeight: 'bold'
          }}
        >
          Complete
        </button>
      )}
    </div>
  );
};

export default SuggestionCard;
