import React from 'react';
import './TearCard.css';

function TearCard({ tear }) {
  const handleDragStart = (e) => {
    e.dataTransfer.setData('tearId', tear.id);
  };

  return (
    <div
      className={`tear-card severity-${tear.severity.toLowerCase()}`}
      draggable="true"
      onDragStart={handleDragStart}
      data-testid={`tear-card-${tear.id}`}
    >
      <h3>{tear.name}</h3>
      <p>ID: {tear.id}</p>
      <p>Severity: <strong>{tear.severity}</strong></p>
    </div>
  );
}

export default TearCard;
