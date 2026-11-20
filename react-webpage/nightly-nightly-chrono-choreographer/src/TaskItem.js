import React from 'react';
import './App.css'; // For shared styles

function TaskItem({ task, onToggleComplete }) {
  return (
    <div
      className={`task-item ${task.completed ? 'completed' : ''}`}
      onClick={() => onToggleComplete(task.id)}
    >
      <span>{task.name}</span>
      {task.completed && <span className="completion-mark">✓</span>}
    </div>
  );
}

export default TaskItem;
