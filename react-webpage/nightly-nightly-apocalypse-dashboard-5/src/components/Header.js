import React from 'react';
import './Header.css';

function Header({ title }) {
  return (
    <header className="dashboard-header">
      <h1>{title}</h1>
      <div className="apocalypse-icon">🌌</div>
    </header>
  );
}

export default Header;
