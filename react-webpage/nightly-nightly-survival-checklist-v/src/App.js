import React from 'react';
import Checklist from './Checklist';

const checklistItems = [
  { id: 1, text: 'Find a safe shelter' },
  { id: 2, text: 'Stock up on water' },
  { id: 3, text: 'Secure a source of food' },
  { id: 4, text: 'Gather medical supplies' },
  { id: 5, text: 'Plan an escape route' }
];

function App() {
  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif', backgroundColor: '#222', color: '#eee' }}>
      <h1>Survival Checklist</h1>
      <Checklist items={checklistItems} />
    </div>
  );
}

export default App;
