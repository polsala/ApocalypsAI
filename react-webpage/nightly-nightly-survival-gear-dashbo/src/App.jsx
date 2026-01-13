import React, { useState } from "react";
import { computeTotalWeight } from "./utils";

function App() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");
  const [weight, setWeight] = useState("");
  const [durability, setDurability] = useState("");

  const addItem = () => {
    if (!name) return;
    const newItem = {
      name,
      weight: parseFloat(weight) || 0,
      durability: parseInt(durability) || 0,
    };
    setItems([...items, newItem]);
    setName("");
    setWeight("");
    setDurability("");
  };

  const totalWeight = computeTotalWeight(items);

  return (
    <div style={{ padding: "1rem", fontFamily: "sans-serif" }}>
      <h1>Survival Gear Dashboard</h1>
      <div>
        <input
          placeholder="Item name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          placeholder="Weight (kg)"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
          type="number"
          step="0.1"
        />
        <input
          placeholder="Durability"
          value={durability}
          onChange={(e) => setDurability(e.target.value)}
          type="number"
        />
        <button onClick={addItem}>Add Item</button>
      </div>
      <h2>Items</h2>
      <ul>
        {items.map((it, idx) => (
          <li key={idx}>
            {it.name} â {it.weight}kg â durability {it.durability}
          </li>
        ))}
      </ul>
      <h3>Total Weight: {totalWeight} kg</h3>
    </div>
  );
}

export default App;
