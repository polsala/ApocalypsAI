import React from 'react';
import TaskItem from './TaskItem';
import './App.css'; // For shared styles

function TaskCalendar({ tasks, daysOfWeek, toggleTaskCompletion }) {
  return (
    <div className="task-calendar">
      {daysOfWeek.map(day => (
        <div key={day} className="calendar-day">
          <h3>{day}</h3>
          <div className="day-tasks">
            {tasks
              .filter(task => task.day === day)
              .map(task => (
                <TaskItem
                  key={task.id}
                  task={task}
                  onToggleComplete={toggleTaskCompletion}
                />
              ))}
            {tasks.filter(task => task.day === day).length === 0 && (
              <p className="no-tasks">No tasks for {day}.</p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

export default TaskCalendar;
