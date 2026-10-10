import React from 'react';
import './CosmicEntry.css';

function CosmicEntry({ entry }) {
  // Simple thematic coloring based on a mock theme property
  const getThemeClass = (theme) => {
    switch (theme) {
      case 'Nebula Musings':
        return 'theme-nebula';
      case 'Stellar Sentiments':
        return 'theme-stellar';
      case 'Void Echoes':
        return 'theme-void';
      default:
        return 'theme-default';
    }
  };

  return (
    <div className={`cosmic-entry ${getThemeClass(entry.theme)}`}>
      <div className="entry-header">
        <span className="entry-origin">From: {entry.origin}</span>
        <span className="entry-timestamp">({entry.timestamp})</span>
      </div>
      <div className="entry-content">
        <p>{entry.content}</p>
      </div>
      <div className="entry-footer">
        <span className="entry-theme">Theme: {entry.theme}</span>
      </div>
    </div>
  );
}

export default CosmicEntry;
