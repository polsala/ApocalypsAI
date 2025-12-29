import React, { useState } from 'react';
import BingoBoard from './BingoBoard.jsx';
import { generateBoard } from './utils.js';

export default function App() {
  const [board, setBoard] = useState(generateBoard());
  return <BingoBoard board={board} />;
}
