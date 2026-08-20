import React from 'react';
import './SkillNode.css';

function SkillNode({ skill, onToggle, isUnlocked, isUnlockable }) {
  const nodeClass = `skill-node ${isUnlocked ? 'unlocked' : 'locked'} ${isUnlockable ? 'unlockable' : ''}`;

  return (
    <div className={nodeClass} style={{ marginLeft: `${skill.level * 20}px` }}>
      <div className="skill-header">
        <h3 className="skill-name">{skill.name}</h3>
        <button
          onClick={() => onToggle(skill.id)}
          disabled={!isUnlockable && !isUnlocked} // Can't unlock if not unlockable, can't lock if not unlocked
          className={`skill-toggle-button ${isUnlocked ? 'unlocked-btn' : (isUnlockable ? 'unlockable-btn' : 'locked-btn')}`}
        >
          {isUnlocked ? 'Mastered!' : (isUnlockable ? 'Unlock' : 'Locked')}
        </button>
      </div>
      <p className="skill-description">{skill.description}</p>
      {skill.prerequisites.length > 0 && !isUnlocked && (
        <p className="skill-prerequisites">Requires: {skill.prerequisites.map(p => p.replace(/-/g, ' ')).join(', ')}</p>
      )}
    </div>
  );
}

export default SkillNode;
