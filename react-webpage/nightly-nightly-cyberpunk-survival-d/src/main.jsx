import React, { useState } from 'react';
import './styles/cyberpunk.css';

const SurvivalDashboard = () => {
  const [resources, setResources] = useState({ water: 100, food: 50 });
  const [threatLevel, setThreat] = useState(30);
  const [aiMood, setAiMood] = useState('neutral');

  const handleScavenge = () => {
    setResources(prev => ({
      water: Math.min(100, prev.water + 10),
      food: Math.min(50, prev.food + 5)
    }));
    setThreat(prev => Math.max(0, prev + 15));
    setAiMood('excited');
  };

  return (
    <div className="cyberpunk-container">
      <h1>生存态势板 🧠</h1>
      <div className="threat-meter">
        <meter min="0" max="100" value={threatLevel} /> {threatLevel}% 威胁等级
      </div>
      <div className="resource-grid">
        <div>💧 水: {resources.water}</div>
        <div>🍎 食物: {resources.food}</div>
      </div>
      <button onClick={handleScavenge}>
        出发搜寻物资
      </button>
      <div className={`ai-companion ${aiMood}`}>AI: {aiMood === 'excited' ? '🎉 发现新资源!' : '😐 监控中...'}</div>
    </div>
  );
};

export default SurvivalDashboard;
