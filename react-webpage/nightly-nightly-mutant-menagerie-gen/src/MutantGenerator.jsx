import React, { useState } from 'react';

export default function MutantGenerator() {
  const [traits, setTraits] = useState({
    eyes: 'glowing green',
    limbs: 'normal',
    skin: 'radiation rash',
    mutationLevel: 50
  });

  const generateMutant = () => {
    const base = {
      name: `Mutant ${['Rat','Squirrel','Raccoon','Coyote','Deer'][Math.floor(Math.random()*5)]}`,
      description: `A ${traits.mutationLevel}% mutated creature with ${traits.eyes} eyes, ${traits.limbs} limbs, and ${traits.skin} skin texture.`
    };
    return {...base, ...traits};
  };

  return (
    <div className="generator">
      <h2>Mutant Traits</h2>
      <div className="trait-panel">
        <label>
          Eyes:
          <select value={traits.eyes} onChange={e => setTraits({...traits, eyes: e.target.value})}>
            <option>glowing green</option>
            <option>radioactive blue</option>
            <option>cracked glass</option>
            <option>laser vision</option>
          </select>
        </label>
        
        <label>
          Limbs:
          <select value={traits.limbs} onChange={e => setTraits({...traits, limbs: e.target.value})}>
            <option>normal</option>
            <option>metallic</option>
            <option>extra set</option>
            <option>crushing claws</option>
          </select>
        </label>
        
        <label>
          Skin:
          <select value={traits.skin} onChange={e => setTraits({...traits, skin: e.target.value})}>
            <option>radiation rash</option>
            <option>scorched</option>
            <option>bioluminescent</option>
            <option>mechanical plating</option>
          </select>
        </label>
      </div>

      <div className="controls">
        <input 
          type="range" 
          min="0" 
          max="100" 
          value={traits.mutationLevel}
          onChange={e => setTraits({...traits, mutationLevel: parseInt(e.target.value)})}
        />
        <span>Mutation Level: {traits.mutationLevel}%</span>
      </div>

      <button onClick={() => console.log(generateMutant())}>
        Generate Mutant
      </button>
    </div>
  );
}
