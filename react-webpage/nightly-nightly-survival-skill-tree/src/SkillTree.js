import React from 'react';
import SkillNode from './SkillNode';
import './SkillTree.css';

function SkillTree({ skills, onToggleSkill }) {
  return (
    <div className="skill-tree-container">
      {skills.map(skill => (
        <SkillNode
          key={skill.id}
          skill={skill}
          onToggle={onToggleSkill}
          isUnlocked={skill.unlocked}
          isUnlockable={skill.isUnlockable} // Passed from App.js
        />
      ))}
    </div>
  );
}

export default SkillTree;
