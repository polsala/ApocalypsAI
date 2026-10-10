import React, { useState, useEffect } from 'react';

const App = () => {
  const [tasks, setTasks] = useState(() => {
    // Load tasks from local storage on initial render
    const savedTasks = localStorage.getItem('chronoChoreographerTasks');
    return savedTasks ? JSON.parse(savedTasks) : [];
  });
  const [newTaskName, setNewTaskName] = useState('');
  const [newTaskDuration, setNewTaskDuration] = useState('');

  // Save tasks to local storage whenever they change
  useEffect(() => {
    localStorage.setItem('chronoChoreographerTasks', JSON.stringify(tasks));
  }, [tasks]);

  const handleAddTask = (e) => {
    e.preventDefault();
    if (newTaskName.trim() === '' || isNaN(parseInt(newTaskDuration))) {
      alert('Please enter a valid task name and duration (in minutes).');
      return;
    }
    const duration = parseInt(newTaskDuration);
    setTasks([...tasks, { id: Date.now(), name: newTaskName.trim(), duration: duration }]);
    setNewTaskName('');
    setNewTaskDuration('');
  };

  const handleRemoveTask = (id) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  const handleMoveTask = (id, direction) => {
    const index = tasks.findIndex(task => task.id === id);
    if (index === -1) return;

    const newTasks = [...tasks];
    if (direction === 'up' && index > 0) {
      [newTasks[index - 1], newTasks[index]] = [newTasks[index], newTasks[index - 1]];
    } else if (direction === 'down' && index < newTasks.length - 1) {
      [newTasks[index + 1], newTasks[index]] = [newTasks[index], newTasks[index + 1]];
    }
    setTasks(newTasks);
  };

  const totalDuration = tasks.reduce((sum, task) => sum + task.duration, 0);

  return (
    <div className="app-container">
      <h1>Nightly Chrono-Choreographer 💃</h1>
      <p>Choreograph your daily tasks into a temporal dance sequence!</p>

      <form onSubmit={handleAddTask} className="task-form">
        <input
          type="text"
          placeholder="Task Name (e.g., Scavenge for rations)"
          value={newTaskName}
          onChange={(e) => setNewTaskName(e.target.value)}
          aria-label="New task name"
        />
        <input
          type="number"
          placeholder="Duration (minutes)"
          value={newTaskDuration}
          onChange={(e) => setNewTaskDuration(e.target.value)}
          min="1"
          aria-label="New task duration in minutes"
        />
        <button type="submit">Add Task</button>
      </form>

      <div className="task-list-container">
        <h2>Your Choreography:</h2>
        {tasks.length === 0 ? (
          <p>No tasks added yet. Start choreographing!</p>
        ) : (
          <ul className="task-list">
            {tasks.map((task, index) => (
              <li key={task.id} className="task-item">
                <span>{task.name} ({task.duration} min)</span>
                <div className="task-controls">
                  <button onClick={() => handleMoveTask(task.id, 'up')} disabled={index === 0} aria-label="Move task up">⬆️</button>
                  <button onClick={() => handleMoveTask(task.id, 'down')} disabled={index === tasks.length - 1} aria-label="Move task down">⬇️</button>
                  <button onClick={() => handleRemoveTask(task.id)} aria-label="Remove task">❌</button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="choreography-display">
        <h2>Temporal Dance Floor:</h2>
        {tasks.length === 0 ? (
          <p>The dance floor awaits your moves!</p>
        ) : (
          <div className="dance-floor">
            {tasks.map(task => (
              <div
                key={task.id}
                className="dance-move"
                style={{ width: `${(task.duration / totalDuration) * 100}%` }}
                title={`${task.name} (${task.duration} min)`}
              >
                <span className="dance-move-label">{task.name}</span>
              </div>
            ))}
          </div>
        )}
        {totalDuration > 0 && (
          <p className="total-duration">Total Choreography Time: {totalDuration} minutes</p>
        )}
      </div>
    </div>
  );
};

export default App;
