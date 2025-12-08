import React from 'react';
import MutantGenerator from './MutantGenerator';

function App() {
  return (
    <div className="App">
      <header>
        <h1>🧬 Mutant Menagerie Generator</h1>
        <p>Create your post-apocalyptic animal companions</p>
      </header>
      <main>
        <MutantGenerator />
      </main>
      <footer>
        <p>Export your creations to share with the wasteland community!</p>
      </footer>
    </div>
  );
}

export default App;
