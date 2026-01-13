import React from 'react';

type Supply = {
  name: string;
  quantity: number;
};

type Props = {
  supplies: Supply[];
  onUpdate: (index: number, delta: number) => void;
};

const SupplyList: React.FC<Props> = ({ supplies, onUpdate }) => {
  if (supplies.length === 0) {
    return <p>No supplies yet.</p>;
  }
  return (
    <ul>
      {supplies.map((s, i) => (
        <li key={i}>
          {s.name}: {s.quantity}{' '}
          <button onClick={() => onUpdate(i, -1)}>-</button>
          <button onClick={() => onUpdate(i, 1)}>+</button>
        </li>
      ))}
    </ul>
  );
};

export default SupplyList;
