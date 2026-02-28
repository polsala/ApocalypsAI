import React, { useState } from 'react';

const quotes = [
  "When the world ends, make sure your coffee is still hot.",
  "Even in the wasteland, a good pun can save the day.",
  "Scavenging is just extreme couponing.",
  "Never trust a mutant with a smile.",
  "Remember: radiation makes for great nightlights."
];

function getRandomQuote() {
  return quotes[Math.floor(Math.random() * quotes.length)];
}

function App() {
  const [quote, setQuote] = useState(getRandomQuote());

  const handleNew = () => {
    setQuote(getRandomQuote());
  };

  return (
    <div style={{fontFamily: 'Arial, sans-serif', padding: '2rem'}}>
      <h1>Survival Quote Generator</h1>
      <p data-testid="quote">{quote}</p>
      <button onClick={handleNew}>New Quote</button>
    </div>
  );
}

export default App;
