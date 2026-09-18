import React, { useState } from 'react';
import './App.css';
import TaskInput from './TaskInput';
import ChronoCompass from './ChronoCompass';

function App() {
  const [tasks, setTasks] = useState([]);
  const [nextId, setNextId] = useState(1);

  const addTask = (name, duration, charge) => {
    if (name && duration > 0) {
      setTasks(prevTasks => [
        ...prevTasks,
        { id: nextId, name, duration: parseInt(duration), charge }
      ]);
      setNextId(prevId => prevId + 1);
    }
  };

  return (
    <div className="App">
      <h1>Nightly Chrono-Compass</h1>
      <TaskInput onAddTask={addTask} />
      <ChronoCompass tasks={tasks} />
      <div className="task-list">
        <h2>Temporal Echoes Log</h2>
        {tasks.length === 0 ? (
          <p>No tasks logged yet. Chart your temporal journey!</p>
        ) : (
          <ul>
            {tasks.map(task => (
              <li key={task.id} className={`charge-${task.charge.toLowerCase()}`}>
                [{task.charge}] {task.name} ({task.duration} min)
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
