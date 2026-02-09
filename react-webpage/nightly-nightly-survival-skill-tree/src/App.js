import React, { useState, useEffect } from 'react';
import SkillTree from './SkillTree';
import './App.css';

const initialSkillsData = [
  { id: 'scavenging', name: 'Scavenging Basics', description: 'Learn to find useful items in abandoned places.', prerequisites: [], unlocked: false, level: 0 },
  { id: 'urban-foraging', name: 'Urban Foraging', description: 'Identify edible plants and discarded food in city ruins.', prerequisites: ['scavenging'], unlocked: false, level: 1 },
  { id: 'wilderness-survival', name: 'Wilderness Survival', description: 'Basic outdoor survival skills: shelter, fire, water.', prerequisites: [], unlocked: false, level: 0 },
  { id: 'basic-first-aid', name: 'Basic First Aid', description: 'Treat minor injuries and stabilize wounds.', prerequisites: [], unlocked: false, level: 0 },
  { id: 'advanced-first-aid', name: 'Advanced First Aid', description: 'Handle severe trauma and medical emergencies.', prerequisites: ['basic-first-aid'], unlocked: false, level: 1 },
  { id: 'makeshift-crafting', name: 'Makeshift Crafting', description: 'Turn junk into useful tools and repairs.', prerequisites: ['scavenging'], unlocked: false, level: 1 },
  { id: 'radio-repair', name: 'Radio Repair', description: 'Fix broken radios to communicate across the wasteland.', prerequisites: ['makeshift-crafting'], unlocked: false, level: 2 },
  { id: 'wasteland-diplomacy', name: 'Wasteland Diplomacy', description: 'Negotiate with other survivors and factions.', prerequisites: [], unlocked: false, level: 0 },
  { id: 'bartering-basics', name: 'Bartering Basics', description: 'Master the art of trade in a resource-scarce world.', prerequisites: ['wasteland-diplomacy'], unlocked: false, level: 1 },
];

function App() {
  const [skills, setSkills] = useState(() => {
    // # Mock rationale: Using localStorage for persistence, but for tests, it's mocked or ignored.
    const savedSkills = localStorage.getItem('survivalSkills');
    return savedSkills ? JSON.parse(savedSkills) : initialSkillsData;
  });

  useEffect(() => {
    // # Mock rationale: Using localStorage for persistence, but for tests, it's mocked or ignored.
    localStorage.setItem('survivalSkills', JSON.stringify(skills));
  }, [skills]);

  const getSkillById = (id) => skills.find(s => s.id === id);

  const arePrerequisitesMet = (skill) => {
    if (!skill.prerequisites || skill.prerequisites.length === 0) {
      return true;
    }
    return skill.prerequisites.every(prereqId => getSkillById(prereqId)?.unlocked);
  };

  const toggleSkill = (id) => {
    setSkills(prevSkills => {
      return prevSkills.map(skill => {
        if (skill.id === id) {
          const canUnlock = arePrerequisitesMet(skill);
          if (skill.unlocked) {
            // If skill is unlocked, allow locking it (un-mastering)
            return { ...skill, unlocked: false };
          } else if (canUnlock) {
            // If skill is locked and prerequisites are met, allow unlocking
            return { ...skill, unlocked: true };
          }
        }
        return skill;
      });
    });
  };

  // Calculate unlockable status for each skill for UI feedback
  const skillsWithUnlockableStatus = skills.map(skill => ({
    ...skill,
    isUnlockable: !skill.unlocked && arePrerequisitesMet(skill),
  }));

  return (
    <div className="app-container">
      <h1>ApocalypsAI Survival Skill Tree</h1>
      <SkillTree skills={skillsWithUnlockableStatus} onToggleSkill={toggleSkill} />
    </div>
  );
}

export default App;
