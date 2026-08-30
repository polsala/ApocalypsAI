import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // Global styles if any, though App.css is used for component-specific
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
