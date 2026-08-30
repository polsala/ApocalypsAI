import React, { useState, useEffect } from 'react';
import './App.css';

const apocalypseThemes = [
  'Cosmic Horror', 'Robot Uprising', 'Zombie Apocalypse', 'Environmental Collapse',
  'Alien Invasion', 'Magical Cataclysm', 'Sentient AI Takeover', 'Mutant Overgrowth',
  'Digital Singularity', 'Post-Apocalyptic Wasteland'
];

const artStyles = [
  'Surrealism', 'Cyberpunk', 'Gothic', 'Art Nouveau', 'Impressionism',
  'Abstract Expressionism', 'Baroque', 'Minimalist', 'Steampunk', 'Dystopian Realism'
];

const subjects = [
  'A lone survivor', 'A mutated creature', 'A sentient machine', 'A celestial event',
  'A hidden sanctuary', 'A forgotten artifact', 'A mutated flora', 'A defiant rebel',
  'A digital ghost', 'A desolate cityscape'
];

function App() {
  const [theme, setTheme] = useState(apocalypseThemes[0]);
  const [style, setStyle] = useState(artStyles[0]);
  const [subject, setSubject] = useState(subjects[0]);
  const [customSubject, setCustomSubject] = useState('');
  const [additionalDetails, setAdditionalDetails] = useState('');
  const [generatedPrompt, setGeneratedPrompt] = useState('');
  const [savedPrompts, setSavedPrompts] = useState([]);

  useEffect(() => {
    // Load saved prompts from localStorage on initial render
    const storedPrompts = localStorage.getItem('apocalypseArtPrompts');
    if (storedPrompts) {
      setSavedPrompts(JSON.parse(storedPrompts));
    }
  }, []);

  const getRandomElement = (arr) => arr[Math.floor(Math.random() * arr.length)];

  const generateArtPrompt = () => {
    let prompt = `A ${style} depiction of ${subject}`; 
    if (customSubject) {
      prompt = `A ${style} depiction of ${customSubject}`;
    }
    if (additionalDetails) {
      prompt += `, with ${additionalDetails}`;
    }
    prompt += ` in the context of a ${theme} apocalypse.`;
    setGeneratedPrompt(prompt);
  };

  const surpriseMe = () => {
    setTheme(getRandomElement(apocalypseThemes));
    setStyle(getRandomElement(artStyles));
    setSubject(getRandomElement(subjects));
    setCustomSubject('');
    setAdditionalDetails('');
    generateArtPrompt();
  };

  const savePrompt = () => {
    if (generatedPrompt && !savedPrompts.includes(generatedPrompt)) {
      const newSavedPrompts = [...savedPrompts, generatedPrompt];
      setSavedPrompts(newSavedPrompts);
      localStorage.setItem('apocalypseArtPrompts', JSON.stringify(newSavedPrompts));
    }
  };

  const deleteSavedPrompt = (promptToDelete) => {
    const updatedPrompts = savedPrompts.filter(prompt => prompt !== promptToDelete);
    setSavedPrompts(updatedPrompts);
    localStorage.setItem('apocalypseArtPrompts', JSON.stringify(updatedPrompts));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Apocalypse Art Generator</h1>
        <p>Craft your next masterpiece from the ashes of imagination!</p>
      </header>
      <main>
        <div className="controls">
          <div className="control-group">
            <label htmlFor="theme">Apocalypse Theme:</label>
            <select id="theme" value={theme} onChange={(e) => setTheme(e.target.value)}>
              {apocalypseThemes.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div className="control-group">
            <label htmlFor="style">Art Style:</label>
            <select id="style" value={style} onChange={(e) => setStyle(e.target.value)}>
              {artStyles.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div className="control-group">
            <label htmlFor="subject">Base Subject:</label>
            <select id="subject" value={subject} onChange={(e) => setSubject(e.target.value)}>
              {subjects.map(sub => <option key={sub} value={sub}>{sub}</option>)}
            </select>
          </div>
          <div className="control-group">
            <label htmlFor="customSubject">Custom Subject (Optional):</label>
            <input type="text" id="customSubject" value={customSubject} onChange={(e) => setCustomSubject(e.target.value)} placeholder="e.g., a sentient toaster" />
          </div>
          <div className="control-group">
            <label htmlFor="additionalDetails">Additional Details (Optional):</label>
            <input type="text" id="additionalDetails" value={additionalDetails} onChange={(e) => setAdditionalDetails(e.target.value)} placeholder="e.g., glowing eyes, raining ash" />
          </div>
        </div>
        <div className="actions">
          <button onClick={generateArtPrompt}>Generate Prompt</button>
          <button onClick={surpriseMe}>Surprise Me!</button>
          {generatedPrompt && <button onClick={savePrompt}>Save Prompt</button>}
        </div>
        {generatedPrompt && (
          <div className="generated-prompt">
            <h2>Your Prompt:</h2>
            <p>{generatedPrompt}</p>
          </div>
        )}
        <div className="saved-prompts">
          <h2>Saved Prompts</h2>
          {savedPrompts.length === 0 ? (
            <p>No prompts saved yet.</p>
          ) : (
            <ul>
              {savedPrompts.map((prompt, index) => (
                <li key={index}>
                  {prompt}
                  <button onClick={() => deleteSavedPrompt(prompt)}>X</button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
