import React, { useState, useEffect } from "react";

const mockResources = [
  { name: "Food", amount: 70, capacity: 100 },
  { name: "Water", amount: 30, capacity: 100 },
  { name: "Medicine", amount: 15, capacity: 50 },
  { name: "Fuel", amount: 5, capacity: 20 }
];

function getColor(percentage) {
  if (percentage > 66) return "#4caf50"; // green
  if (percentage > 33) return "#ff9800"; // orange
  return "#f44336"; // red
}

export default function App() {
  const [resources, setResources] = useState([]);

  useEffect(() => {
    // Simulate async fetch
    const fetchData = () => {
      // Mock rationale: simulate network latency
      setTimeout(() => {
        setResources(mockResources);
      }, 100);
    };
    fetchData();
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Community Resource Dashboard</h1>
      {resources.map((r) => {
        const percent = Math.round((r.amount / r.capacity) * 100);
        return (
          <div key={r.name} style={{ marginBottom: "15px" }}>
            <div>{r.name}: {r.amount}/{r.capacity} ({percent}%)</div>
            <div style={{
              background: "#ddd",
              width: "100%",
              height: "20px",
              borderRadius: "4px",
              overflow: "hidden"
            }}>
              <div style={{
                width: `${percent}%`,
                height: "100%",
                background: getColor(percent)
              }} />
            </div>
          </div>
        );
      })}
    </div>
  );
}
