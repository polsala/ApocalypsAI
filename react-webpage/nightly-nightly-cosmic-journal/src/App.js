import React, { useState, useEffect } from 'react';
import './App.css';

const cosmicWisdom = [
  "The stars are not wanted unless they shine.",
  "Look up at the stars and not down at your feet.",
  "The universe is a symphony of interconnectedness.",
  "Every atom of your being is as old as the universe.",
  "We are made of star-stuff.",
  "The cosmos is within us. We are made of star-stuff. We are a way for the universe to know itself.",
  "The greatest glory in living lies not in never falling, but in rising every time we fall.",
  "The universe is under no obligation to make sense to you."
];

function App() {
  const [dreams, setDreams] = useState([]);
  const [thoughts, setThoughts] = useState([]);
  const [currentThought, setCurrentThought] = useState('');
  const [currentDream, setCurrentDream] = useState({ title: '', description: '' });
  const [dailyWisdom, setDailyWisdom] = useState('');

  useEffect(() => {
    const today = new Date();
    const dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / 1000 / 60 / 60 / 24);
    setDailyWisdom(cosmicWisdom[dayOfYear % cosmicWisdom.length]);
  }, []);

  const handleThoughtChange = (event) => {
    setCurrentThought(event.target.value);
  };

  const addThought = () => {
    if (currentThought.trim()) {
      setThoughts([...thoughts, { id: Date.now(), text: currentThought }]);
      setCurrentThought('');
    }
  };

  const handleDreamChange = (event) => {
    const { name, value } = event.target;
    setCurrentDream({ ...currentDream, [name]: value });
  };

  const addDream = () => {
    if (currentDream.title.trim() && currentDream.description.trim()) {
      setDreams([...dreams, { ...currentDream, id: Date.now() }]);
      setCurrentDream({ title: '', description: '' });
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Cosmic Journal</h1>
        <p>Your personal space for dreams and thoughts among the stars.</p>
      </header>
      <main>
        <section className="cosmic-inspiration">
          <h2>Daily Cosmic Wisdom</h2>
          <p>"{dailyWisdom}"</p>
        </section>

        <section className="thought-nebula">
          <h2>Thought Nebula</h2>
          <textarea
            placeholder="Capture a fleeting thought..."
            value={currentThought}
            onChange={handleThoughtChange}
          />
          <button onClick={addThought}>Add Thought</button>
          <ul>
            {thoughts.map(thought => (
              <li key={thought.id}>{thought.text}</li>
            ))}
          </ul>
        </section>

        <section className="dream-weaver">
          <h2>Dream Weaver</h2>
          <input
            type="text"
            name="title"
            placeholder="Dream Title"
            value={currentDream.title}
            onChange={handleDreamChange}
          />
          <textarea
            name="description"
            placeholder="Describe your dream..."
            value={currentDream.description}
            onChange={handleDreamChange}
          />
          <button onClick={addDream}>Log Dream</button>
          <ul>
            {dreams.map(dream => (
              <li key={dream.id}>
                <strong>{dream.title}:</strong> {dream.description}
              </li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
}

export default App;
