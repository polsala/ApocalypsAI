import React from 'react';
import ReactDOM from 'react-dom/client';

const data = [
  { date: '2023-10-01', triage: 5 },
  { date: '2023-10-02', triage: 3 },
  { date: '2023-10-03', triage: 8 },
  { date: '2023-10-04', triage: 2 },
  { date: '2023-10-05', triage: 6 }
];

function App() {
  return (
    <div>
      <h1>Issue Triage Heatmap</h1>
      <table border="1">
        <thead>
          <tr>
            <th>Date</th>
            <th>Triage Count</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx}>
              <td>{row.date}</td>
              <td>{row.triage}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
