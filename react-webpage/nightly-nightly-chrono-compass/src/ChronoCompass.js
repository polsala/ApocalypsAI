import React from 'react';
import './ChronoCompass.css';

const CHARGE_COLORS = {
  Positive: '#4CAF50', // Green
  Neutral: '#9E9E9E',  // Grey
  Negative: '#F44336'  // Red
};

function ChronoCompass({ tasks }) {
  const totalDuration = tasks.reduce((sum, task) => sum + task.duration, 0);
  const radius = 100;
  const strokeWidth = 30;
  const circumference = 2 * Math.PI * radius;

  if (tasks.length === 0) {
    return (
      <div className="chrono-compass-container">
        <svg width="250" height="250" viewBox="0 0 250 250">
          <circle
            cx="125" cy="125" r={radius}
            fill="none" stroke="#555" strokeWidth={strokeWidth}
          />
          <text x="125" y="125" textAnchor="middle" fill="#f0f0f0" fontSize="14">
            Add tasks to see your compass!
          </text>
        </svg>
      </div>
    );
  }

  let currentOffset = 0;

  return (
    <div className="chrono-compass-container">
      <svg width="250" height="250" viewBox="0 0 250 250">
        {tasks.map((task, index) => {
          const percentage = task.duration / totalDuration;
          const strokeDasharray = circumference * percentage;
          const strokeDashoffset = circumference - currentOffset;
          currentOffset += strokeDasharray;

          return (
            <circle
              key={task.id}
              cx="125" cy="125" r={radius}
              fill="none"
              stroke={CHARGE_COLORS[task.charge] || CHARGE_COLORS.Neutral}
              strokeWidth={strokeWidth}
              strokeDasharray={`${strokeDasharray} ${circumference - strokeDasharray}`}
              strokeDashoffset={strokeDashoffset}
              transform="rotate(-90 125 125)" /* Start from top */
              className="compass-segment"
            >
              <title>{task.name}: {task.duration} min ({task.charge})</title>
            </circle>
          );
        })}
      </svg>
      <p className="total-duration">Total Temporal Energy: {totalDuration} minutes</p>
    </div>
  );
}

export default ChronoCompass;
