import { useState, useEffect } from 'react';
import './main.css';

const WHIMSICAL_MESSAGES = [
  "You're surviving like a pro! 🦖",
  "That's the way! Now go find some snacks! 🍞",
  "Task complete! Reward: 5 extra minutes of sleep 🛏️",
  "Survival points +1! Keep it up! ⚔️"
];

export default function TaskMate() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState('');
  const [currentMessage, setCurrentMessage] = useState('');

  useEffect(() => {
    if (tasks.filter(t => t.completed).length > 0) {
      setCurrentMessage(WHIMSICAL_MESSAGES[
        Math.floor(Math.random() * WHIMSICAL_MESSAGES.length)
      ]);
    }
  }, [tasks]);

  const addTask = () => {
    if (newTask.trim()) {
      setTasks([...tasks, {
        id: Date.now(),
        text: newTask,
        completed: false
      }]);
      setNewTask('');
    }
  };

  const toggleTask = (id) => {
    setTasks(tasks.map(task => 
      task.id === id ? { ...task, completed: !task.completed } : task
    ));
  };

  return (
    <div className="task-mate">
      <h1>🧟‍♂️ Task Mate</h1>
      <div className="input-group">
        <input
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          placeholder="Add survival task..."
          onKeyPress={(e) => e.key === 'Enter' && addTask()}
        />
        <button onClick={addTask}>➕</button>
      </div>
      <ul>
        {tasks.map(task => (
          <li key={task.id} className={task.completed ? 'completed' : ''}>
            <span onClick={() => toggleTask(task.id)}>
              {task.text}
            </span>
            {task.completed && <span className="checkmark">✅</span>}
          </li>
        ))}
      </ul>
      {currentMessage && <div className="message">{currentMessage}</div>}
    </div>
  );
}
