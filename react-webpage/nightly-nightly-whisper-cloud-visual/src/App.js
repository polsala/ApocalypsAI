import React, { useState, useCallback } from 'react';
import './App.css';

const stopWords = new Set([
  'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
  'to', 'of', 'in', 'on', 'at', 'for', 'with', 'as', 'by', 'from', 'up', 'down', 'out', 'off',
  'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
  'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
  'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
  'just', 'don', 'should', 'now', 'about', 'into', 'through', 'during', 'before', 'after',
  'above', 'below', 'between', 'among', 'across', 'along', 'around', 'behind', 'below',
  'beneath', 'beside', 'between', 'beyond', 'during', 'except', 'for', 'from', 'inside',
  'into', 'near', 'off', 'on', 'onto', 'out', 'outside', 'over', 'past', 'round', 'since',
  'through', 'to', 'under', 'until', 'up', 'upon', 'with', 'within', 'without', 'i', 'me',
  'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
  'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',
  'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
  'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
  'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'would', 'should', 'could',
  'ought', 'i\'m', 'you\'re', 'he\'s', 'she\'s', 'it\'s', 'we\'re', 'they\'re', 'i\'ve',
  'you\'ve', 'we\'ve', 'they\'ve', 'i\'d', 'you\'d', 'he\'d', 'she\'d', 'we\'d', 'they\'d',
  'i\'ll', 'you\'ll', 'he\'ll', 'she\'ll', 'we\'ll', 'they\'ll', 'isn\'t', 'aren\'t', 'wasn\'t',
  'weren\'t', 'hasn\'t', 'haven\'t', 'hadn\'t', 'doesn\'t', 'don\'t', 'didn\'t', 'won\'t',
  'wouldn\'t', 'shan\'t', 'shouldn\'t', 'can\'t', 'cannot', 'couldn\'t', 'mustn\'t', 'let\'s',
  'that\'s', 'who\'s', 'what\'s', 'here\'s', 'there\'s', 'when\'s', 'where\'s', 'why\'s',
  'how\'s', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn',
  'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn',
  'weren', 'won', 'wouldn'
]);

function App() {
  const [inputText, setInputText] = useState('');
  const [wordFrequencies, setWordFrequencies] = useState([]);

  const processText = useCallback(() => {
    if (!inputText.trim()) {
      setWordFrequencies([]);
      return;
    }

    const cleanedText = inputText
      .toLowerCase()
      .replace(/[.,/#!$%^&*;:{}=\-_`~()]/g, '') // Remove punctuation
      .replace(/\s\s+/g, ' ') // Replace multiple spaces with single space
      .trim();

    const words = cleanedText.split(' ').filter(word => word.length > 2 && !stopWords.has(word));

    const frequencies = {};
    words.forEach(word => {
      frequencies[word] = (frequencies[word] || 0) + 1;
    });

    const sortedFrequencies = Object.entries(frequencies)
      .sort(([, countA], [, countB]) => countB - countA)
      .slice(0, 50); // Limit to top 50 words for display

    setWordFrequencies(sortedFrequencies);
  }, [inputText]);

  const getMaxFrequency = () => {
    if (wordFrequencies.length === 0) return 1;
    return wordFrequencies[0][1];
  };

  return (
    <div className="App">
      <h1>Nightly Whisper Cloud Visualizer</h1>
      <textarea
        placeholder="Paste your wasteland whispers, survivor logs, or cryptic prophecies here..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      ></textarea>
      <button onClick={processText}>Generate Whispers</button>

      <div className="word-cloud">
        {wordFrequencies.length === 0 ? (
          <p>No whispers yet. Type something above!</p>
        ) : (
          wordFrequencies.map(([word, count]) => (
            <span
              key={word}
              style={{
                fontSize: `${1 + (count / getMaxFrequency()) * 2}em`, // Scale font size
                opacity: `${0.5 + (count / getMaxFrequency()) * 0.5}` // Scale opacity
              }}
              title={`${word}: ${count} times`}
            >
              {word}
            </span>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
