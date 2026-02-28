import React from 'react';
import './InputForm.css';

function InputForm({ inputText, setInputText, keywordsInput, setKeywordsInput }) {
  return (
    <div className="input-form-container">
      <div className="input-group">
        <label htmlFor="text-input">Text to Analyze:</label>
        <textarea
          id="text-input"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Paste your text here..."
          rows="10"
        ></textarea>
      </div>
      <div className="input-group">
        <label htmlFor="keywords-input">Keywords (comma-separated):</label>
        <input
          id="keywords-input"
          type="text"
          value={keywordsInput}
          onChange={(e) => setKeywordsInput(e.target.value)}
          placeholder="e.g., temporal, rift, anomaly"
        />
      </div>
    </div>
  );
}

export default InputForm;
