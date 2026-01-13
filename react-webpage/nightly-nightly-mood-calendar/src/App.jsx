import React from 'react';

const EMOJIS = ['ð','ð','ð','ð¤©','ð','ð¤','ð¥³','ð´','ð¤','ð¤©'];

function getMoodEmoji(dateStr, startDateStr) {
  const date = new Date(dateStr);
  const start = new Date(startDateStr);
  const diff = Math.floor((date - start) / (1000 * 60 * 60 * 24));
  const index = ((diff % EMOJIS.length) + EMOJIS.length) % EMOJIS.length;
  return EMOJIS[index];
}

export default function MoodCalendar({ startDate, days }) {
  const rows = [];
  for (let i = 0; i < days; i++) {
    const currentDate = new Date(startDate);
    currentDate.setDate(currentDate.getDate() + i);
    const iso = currentDate.toISOString().split('T')[0];
    const emoji = getMoodEmoji(iso, startDate);
    rows.push(
      <div key={iso} style={{display:'inline-block',margin:'4px',fontSize:'24px'}}>
        {iso}: {emoji}
      </div>
    );
  }
  return <div>{rows}</div>;
}
