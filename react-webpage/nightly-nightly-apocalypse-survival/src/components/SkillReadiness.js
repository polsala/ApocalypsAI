import React from 'react';

const skills = [
  { name: 'Fire Starting', readiness: 85 },
  { name: 'Scavenging', readiness: 70 },
  { name: 'First Aid', readiness: 60 },
  { name: 'Camouflage', readiness: 50 }
];

function SkillReadiness() {
  return (
    <div className="skill-readiness">
      <h2>Survival Skills</h2>
      <ul>
        {skills.map((skill, index) => (
          <li key={index}>
            {skill.name}: {skill.readiness}%
            <progress value={skill.readiness} max="100"></progress>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SkillReadiness;
