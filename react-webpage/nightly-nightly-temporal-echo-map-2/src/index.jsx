import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css'; // Basic global styles, often from create-react-app

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
