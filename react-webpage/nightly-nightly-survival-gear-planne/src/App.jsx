import React, { useState } from "react";

const GEAR = [
  { id: 1, name: "Water Bottle", weight: 2 },
  { id: 2, name: "Canned Food (x3)", weight: 3 },
  { id: 3, name: "First Aid Kit", weight: 1.5 },
  { id: 4, name: "Multi‑tool", weight: 0.5 },
  { id: 5, name: "Tent", weight: 5 },
  { id: 6, name: "Sleeping Bag", weight: 4 }
];

export default function App() {
  const [selected, setSelected] = useState([]);

  const toggle = (id) => {
    setSelected((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  const totalWeight = selected.reduce((sum, id) => {
    const item = GEAR.find((g) => g.id === id);
    return sum + (item ? item.weight : 0);
  }, 0);

  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "1rem" }}>
      <h1>Survival Gear Planner</h1>
      <ul>
        {GEAR.map((item) => (
          <li key={item.id}>
            <label>
              <input
                type="checkbox"
                checked={selected.includes(item.id)}
                onChange={() => toggle(item.id)}
              />
              {item.name} – {item.weight} kg
            </label>
          </li>
        ))}
      </ul>
      <h2>Total Weight: {totalWeight.toFixed(2)} kg</h2>
    </div>
  );
}
