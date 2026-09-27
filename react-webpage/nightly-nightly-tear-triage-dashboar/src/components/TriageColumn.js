import React from 'react';
import TearCard from './TearCard';
import './TriageColumn.css';

function TriageColumn({ id, title, tears, onDropTear }) {
  const handleDragOver = (e) => {
    e.preventDefault(); // Necessary to allow dropping
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const tearId = e.dataTransfer.getData('tearId');
    onDropTear(tearId, id);
  };

  return (
    <div
      className="triage-column"
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      data-testid={`triage-column-${id}`}
    >
      <h2>{title}</h2>
      <div className="tear-cards-container">
        {tears.map(tear => (
          <TearCard key={tear.id} tear={tear} />
        ))}
      </div>
    </div>
  );
}

export default TriageColumn;
