import React from 'react';
import './SkillNode.css';

function SkillNode({ skill, isLearned, isAvailable, onClick }) {
  const nodeClass = `skill-node ${isLearned ? 'learned' : ''} ${isAvailable ? 'available' : ''}`;

  return (
    <div
      className={nodeClass}
      onClick={() => onClick(skill.id)}
      title={skill.description}
      data-testid={`skill-node-${skill.id}`}
    >
      <h3>{skill.name}</h3>
      <p className="skill-tier">Tier: {skill.tier}</p>
      {skill.prerequisites.length > 0 && (
        <p className="skill-prereqs">Prereqs: {skill.prerequisites.join(', ')}</p>
      )}
    </div>
  );
}

export default SkillNode;
