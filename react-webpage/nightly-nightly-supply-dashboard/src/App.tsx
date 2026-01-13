import React, { useState } from 'react';
import SupplyList from './components/SupplyList';

type Supply = {
  name: string;
  quantity: number;
};

const App: React.FC = () => {
  const [supplies, setSupplies] = useState<Supply[]>([]);
  const [newName, setNewName] = useState('');
  const [newQty, setNewQty] = useState(1);

  const addSupply = () => {
    if (!newName.trim()) return;
    setSupplies([...supplies, { name: newName.trim(), quantity: newQty }]);
    setNewName('');
    setNewQty(1);
  };

  const updateQuantity = (index: number, delta: number) => {
    const updated = supplies.map((s, i) =>
      i === index ? { ...s, quantity: Math.max(s.quantity + delta, 0) } : s
    );
    setSupplies(updated);
  };

  return (
    <div style={{ padding: '1rem', fontFamily: 'sans-serif' }}>
      <h1>Supply Dashboard</h1>
      <div>
        <input
          placeholder="Item name"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <input
          type="number"
          min={1}
          value={newQty}
          onChange={(e) => setNewQty(parseInt(e.target.value, 10) || 1)}
          style={{ width: '4rem', marginLeft: '0.5rem' }}
        />
        <button onClick={addSupply} style={{ marginLeft: '0.5rem' }}>
          Add
        </button>
      </div>
      <SupplyList supplies={supplies} onUpdate={updateQuantity} />
    </div>
  );
};

export default App;
