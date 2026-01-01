import React from 'react';
import ReactDOM from 'react-dom/client';
import QuantumEntanglementSimulator from './main';
import './styles.css';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <QuantumEntanglementSimulator />
  </React.StrictMode>
);

// Hot module replacement for development
if (module.hot) {
  module.hot.accept();
}
