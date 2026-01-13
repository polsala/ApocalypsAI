import React, { useState, useEffect } from "react";

function App() {
  const [items, setItems] = useState(() => {
    const saved = localStorage.getItem("checklist");
    return saved ? JSON.parse(saved) : [
      { id: 1, text: "Water filter", done: false },
      { id: 2, text: "First aid kit", done: false },
      { id: 3, text: "Solar charger", done: false }
    ];
  });

  useEffect(() => {
    localStorage.setItem("checklist", JSON.stringify(items));
  }, [items]);

  const toggleItem = id => {
    setItems(items.map(item => item.id === id ? { ...item, done: !item.done } : item));
  };

  const addItem = text => {
    const newItem = { id: Date.now(), text, done: false };
    setItems([...items, newItem]);
  };

  const completed = items.filter(i => i.done).length;
  const progress = items.length ? Math.round((completed / items.length) * 100) : 0;

  const [newText, setNewText] = useState("");

  const handleAdd = e => {
    e.preventDefault();
    if (newText.trim()) {
      addItem(newText.trim());
      setNewText("");
    }
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", padding: "1rem", maxWidth: "600px", margin: "auto" }}>
      <h1>Apocalypse Survival Checklist</h1>
      <div style={{ background: "#eee", borderRadius: "4px", overflow: "hidden", marginBottom: "1rem" }}>
        <div style={{ width: `${progress}%`, background: "#4caf50", height: "20px" }} />
      </div>
      <p>{completed} of {items.length} items completed ({progress}%)</p>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {items.map(item => (
          <li key={item.id} style={{ marginBottom: "0.5rem" }}>
            <label>
              <input type="checkbox" checked={item.done} onChange={() => toggleItem(item.id)} />
              <span style={{ textDecoration: item.done ? "line-through" : "none", marginLeft: "0.5rem" }}>{item.text}</span>
            </label>
          </li>
        ))}
      </ul>
      <form onSubmit={handleAdd}>
        <input value={newText} onChange={e => setNewText(e.target.value)} placeholder="New item" />
        <button type="submit">Add</button>
      </form>
    </div>
  );
}

export default App;
