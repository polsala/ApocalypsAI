import React, { useState } from 'react';
import AuraDisplay from './AuraDisplay';
import { analyzeSentiment } from './sentimentAnalyzer';

function App() {
  const [text, setText] = useState('');
  const [sentiment, setSentiment] = useState(0); // -1: negative, 0: neutral, 1: positive

  const handleAnalyze = () => {
    const score = analyzeSentiment(text);
    setSentiment(score);
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Nightly Aura Reader</h1>
      <p style={styles.subtitle}>Unveil the emotional essence of your text.</p>
      <textarea
        style={styles.textarea}
        placeholder="Enter text here... (e.g., 'The temporal anomaly stabilized, all systems nominal.')"
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows="5"
      />
      <button style={styles.button} onClick={handleAnalyze}>
        Read Aura
      </button>
      <div style={styles.auraContainer}>
        <AuraDisplay sentiment={sentiment} />
      </div>
      <p style={styles.footer}>A Nightly Integrator creation for the ApocalypsAI community.</p>
    </div>
  );
}

const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    backgroundColor: '#282c34',
    color: 'white',
    padding: '20px',
    boxSizing: 'border-box'
  },
  title: {
    fontSize: '2.5em',
    marginBottom: '10px',
    color: '#61dafb'
  },
  subtitle: {
    fontSize: '1.2em',
    marginBottom: '30px',
    textAlign: 'center',
    maxWidth: '600px'
  },
  textarea: {
    width: '80%',
    maxWidth: '600px',
    padding: '15px',
    margin: '20px 0',
    borderRadius: '8px',
    border: '1px solid #61dafb',
    backgroundColor: '#3a3f47',
    color: 'white',
    fontSize: '1em',
    resize: 'vertical'
  },
  button: {
    padding: '12px 25px',
    fontSize: '1.1em',
    backgroundColor: '#61dafb',
    color: '#282c34',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'background-color 0.3s ease',
    '&:hover': {
      backgroundColor: '#21a1f1'
    }
  },
  auraContainer: {
    marginTop: '40px',
    width: '200px',
    height: '200px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    border: '2px dashed #61dafb',
    borderRadius: '50%',
    padding: '10px'
  },
  footer: {
    marginTop: '50px',
    fontSize: '0.8em',
    color: '#aaa'
  }
};

export default App;
