import React, { useState, useEffect, useCallback } from 'react';
import SkillNode from './SkillNode';
import skillsData from './data/skills';
import './SkillTree.css';

function SkillTree() {
  const [learnedSkills, setLearnedSkills] = useState({}); // { skillId: true }

  // Function to check if a skill is available to learn
  const isSkillAvailable = useCallback((skillId) => {
    const skill = skillsData.find(s => s.id === skillId);
    if (!skill) return false;
    if (learnedSkills[skillId]) return false; // Already learned

    // Check prerequisites
    return skill.prerequisites.every(prereqId => learnedSkills[prereqId]);
  }, [learnedSkills]);

  // Function to handle learning a skill
  const learnSkill = useCallback((skillId) => {
    if (isSkillAvailable(skillId)) {
      setLearnedSkills(prev => ({ ...prev, [skillId]: true }));
    } else if (learnedSkills[skillId]) {
      // Optionally allow unlearning, but for this simple version, we'll just ignore
      console.log(`Skill ${skillId} already learned.`);
    } else {
      console.log(`Cannot learn ${skillId}. Prerequisites not met.`);
    }
  }, [isSkillAvailable, learnedSkills]);

  // Group skills by branch and tier for display
  const groupedSkills = skillsData.reduce((acc, skill) => {
    if (!acc[skill.branch]) {
      acc[skill.branch] = {};
    }
    if (!acc[skill.branch][skill.tier]) {
      acc[skill.branch][skill.tier] = [];
    }
    acc[skill.branch][skill.tier].push(skill);
    return acc;
  }, {});

  const branches = Object.keys(groupedSkills);

  return (
    <div className="skill-tree-container">
      <h1>Survival Skill Tree</h1>
      <p className="instruction-text">Click on available skills to learn them.</p>

      {branches.map(branchName => (
        <div key={branchName} className="skill-branch">
          <h2>{branchName}</h2>
          {Object.keys(groupedSkills[branchName]).sort((a, b) => a - b).map(tier => (
            <div key={`${branchName}-tier-${tier}`} className="skill-tier-row">
              <h3>Tier {tier}</h3>
              <div className="skill-nodes-wrapper">
                {groupedSkills[branchName][tier].map(skill => (
                  <SkillNode
                    key={skill.id}
                    skill={skill}
                    isLearned={!!learnedSkills[skill.id]}
                    isAvailable={isSkillAvailable(skill.id)}
                    onClick={learnSkill}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export default SkillTree;
