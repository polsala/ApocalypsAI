import React from 'react';
import { getEmojiForDate } from './emojiMapper';

function EmojiCalendar() {
  const today = new Date();
  const month = today.getMonth();
  const year = today.getFullYear();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const days = [];
  for (let d = 1; d <= daysInMonth; d++) {
    const date = new Date(year, month, d);
    days.push(
      <div key={d} className="day">
        <span>{d}</span> <span>{getEmojiForDate(date)}</span>
      </div>
    );
  }
  return (
    <div className="emoji-calendar">
      <h2>{today.toLocaleString('default', { month: 'long' })} {year}</h2>
      <div className="days">{days}</div>
    </div>
  );
}

export default EmojiCalendar;
