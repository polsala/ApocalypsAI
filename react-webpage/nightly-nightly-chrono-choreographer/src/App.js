import React, { useState, useEffect } from 'react';
import TaskCalendar from './TaskCalendar';
import './App.css';

const DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

function App() {
  const [tasks, setTasks] = useState(() => {
    // # Mock rationale: localStorage is mocked in tests to ensure deterministic, offline execution.
    const savedTasks = localStorage.getItem('chronoTasks');
    return savedTasks ? JSON.parse(savedTasks) : [];
  });
  const [newTaskName, setNewTaskName] = useState('');

  useEffect(() => {
    // # Mock rationale: localStorage is mocked in tests to ensure deterministic, offline execution.
    localStorage.setItem('chronoTasks', JSON.stringify(tasks));
  }, [tasks]);

  const addTask = () => {
    if (newTaskName.trim() === '') return;
    const newTask = {
      id: Date.now(),
      name: newTaskName.trim(),
      day: null, // null means unassigned
      completed: false,
    };
    setTasks([...tasks, newTask]);
    setNewTaskName('');
  };

  const assignTaskToDay = (taskId, day) => {
    setTasks(tasks.map(task =>
      task.id === taskId ? { ...task, day: day } : task
    ));
  };

  const toggleTaskCompletion = (taskId) => {
    setTasks(tasks.map(task =>
      task.id === taskId ? { ...task, completed: !task.completed } : task
    ));
  };

  const clearCompletedTasks = () => {
    setTasks(tasks.filter(task => !task.completed));
  };

  const unassignedTasks = tasks.filter(task => task.day === null);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Chrono-Choreographer</h1>
        <p>Organize your apocalyptic endeavors!</p>
      </header>

      <div className="task-input-section">
        <input
          type="text"
          value={newTaskName}
          onChange={(e) => setNewTaskName(e.target.value)}
          placeholder="Enter a new task (e.g., 'Fortify temporal rift')"
          onKeyPress={(e) => { if (e.key === 'Enter') addTask(); }}
        />
        <button onClick={addTask}>Add Task</button>
      </div>

      <div className="unassigned-tasks-section">
        <h2>Unassigned Tasks</h2>
        <div className="unassigned-tasks-list">
          {unassignedTasks.length === 0 && <p>No unassigned tasks. Time to get busy!</p>}
          {unassignedTasks.map(task => (
            <div key={task.id} className="task-item unassigned">
              <span>{task.name}</span>
              <select
                onChange={(e) => assignTaskToDay(task.id, e.target.value)}
                value=""
              >
                <option value="" disabled>Assign to Day</option>
                {DAYS_OF_WEEK.map(day => (
                  <option key={day} value={day}>{day}</option>
                ))}
              </select>
            </div>
          ))}
        </div>
      </div>

      <TaskCalendar
        tasks={tasks}
        daysOfWeek={DAYS_OF_WEEK}
        toggleTaskCompletion={toggleTaskCompletion}
      />

      <div className="footer-actions">
        <button onClick={clearCompletedTasks}>Clear Completed</button>
      </div>
    </div>
  );
}

export default App;
