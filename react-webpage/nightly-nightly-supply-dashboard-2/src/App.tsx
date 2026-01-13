import React, { useState } from "react";

interface Item {
  name: string;
  weight: number; // kg per unit
  quantity: number;
  value: number; // credits per unit
}

const App: React.FC = () => {
  const [items, setItems] = useState<Item[]>([]);
  const [form, setForm] = useState<Partial<Item>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: name === "name" ? value : Number(value),
    }));
  };

  const addItem = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.name || form.weight == null || form.quantity == null || form.value == null) {
      return;
    }
    setItems((prev) => [...prev, form as Item]);
    setForm({});
  };

  const totalWeight = items.reduce((sum, i) => sum + i.weight * i.quantity, 0);
  const totalValue = items.reduce((sum, i) => sum + i.value * i.quantity, 0);

  return (
    <div style={{ padding: "1rem", fontFamily: "sans-serif" }}>
      <h1>Supply Dashboard</h1>
      <form onSubmit={addItem} style={{ marginBottom: "1rem" }}>
        <input
          name="name"
          placeholder="Item name"
          value={form.name ?? ""}
          onChange={handleChange}
          required
        />
        <input
          name="weight"
          type="number"
          placeholder="Weight (kg)"
          value={form.weight ?? ""}
          onChange={handleChange}
          required
        />
        <input
          name="quantity"
          type="number"
          placeholder="Quantity"
          value={form.quantity ?? ""}
          onChange={handleChange}
          required
        />
        <input
          name="value"
          type="number"
          placeholder="Value (credits)"
          value={form.value ?? ""}
          onChange={handleChange}
          required
        />
        <button type="submit">Add</button>
      </form>

      {items.length > 0 && (
        <table border={1} cellPadding={4}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Weight (kg)</th>
              <th>Qty</th>
              <th>Value (c)</th>
            </tr>
          </thead>
          <tbody>
            {items.map((it, idx) => (
              <tr key={idx}>
                <td>{it.name}</td>
                <td>{it.weight}</td>
                <td>{it.quantity}</td>
                <td>{it.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <h2>Totals</h2>
      <p>Total weight: {totalWeight} kg</p>
      <p>Total value: {totalValue} credits</p>
    </div>
  );
};

export default App;

