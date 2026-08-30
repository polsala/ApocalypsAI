import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [entries, setEntries] = useState([]);
  const [title, setTitle] = useState('');
  const [date, setDate] = useState('');
  const [content, setContent] = useState('');

  useEffect(() => {
    // Load entries from localStorage on initial render
    const savedEntries = localStorage.getItem('cosmicJournalEntries');
    if (savedEntries) {
      setEntries(JSON.parse(savedEntries));
    }
  }, []);

  useEffect(() => {
    // Save entries to localStorage whenever they change
    localStorage.setItem('cosmicJournalEntries', JSON.stringify(entries));
  }, [entries]);

  const handleAddEntry = (e) => {
    e.preventDefault();
    if (!title || !date || !content) {
      alert('Please fill in all fields!');
      return;
    }
    const newEntry = {
      id: Date.now(),
      title,
      date,
      content,
    };
    setEntries([...entries, newEntry]);
    // Clear form
    setTitle('');
    setDate('');
    setContent('');
  };

  const generateWordCloud = (allContent) => {
    const words = allContent.toLowerCase().match(/\b\w{3,}\b/g) || [];
    const wordCounts = words.reduce((acc, word) => {
      acc[word] = (acc[word] || 0) + 1;
      return acc;
    }, {});

    const sortedWords = Object.entries(wordCounts).sort(([, a], [, b]) => b - a);
    return sortedWords.slice(0, 20); // Top 20 words
  };

  const wordCloudData = generateWordCloud(entries.map(e => e.content).join(' '));

  return (
    <div className="App">
      <header className="App-header">
        <h1>✨ Cosmic Journal Visualizer ✨</h1>
      </header>
      <main>
        <section className="entry-form">
          <h2>Add a New Cosmic Thought</h2>
          <form onSubmit={handleAddEntry}>
            <input
              type="text"
              placeholder="Title (e.g., A Starry Revelation)"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
            <textarea
              placeholder="Your cosmic musings..."
              rows="5"
              value={content}
              onChange={(e) => setContent(e.target.value)}
            ></textarea>
            <button type="submit">Record Entry</button>
          </form>
        </section>

        <section className="visualizations">
          <h2>Your Cosmic Constellation</h2>
          <div className="timeline">
            <h3>Timeline of Thoughts</h3>
            {entries.length === 0 ? (
              <p>Your cosmic journey is just beginning...</p>
            ) : (
              <ul>
                {entries.sort((a, b) => new Date(a.date) - new Date(b.date)).map(entry => (
                  <li key={entry.id}>
                    <strong>{entry.title}</strong> ({entry.date})
                    <p>{entry.content}</p>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="word-cloud">
            <h3>Word Nebula</h3>
            {wordCloudData.length === 0 ? (
              <p>No words yet to form a nebula.</p>
            ) : (
              <div className="word-cloud-container">
                {wordCloudData.map(([word, count]) => (
                  <span
                    key={word}
                    style={{ fontSize: `${12 + count * 2}px`, margin: '5px', display: 'inline-block' }}
                  >
                    {word}
                  </span>
                ))}
              </div>
            )}
          </div>
        </section>
      </main>
      <footer>
        <p>May your thoughts be as vast as the universe.</p>
      </footer>
    </div>
  );
}

export default App;
