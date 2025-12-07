import React, { useState, useEffect } from 'react';

const DNA_TRAITS = {
  heads: ['Radiation Gecko', 'Toxic Frog', 'Mutant Rat', 'Cyborg Raccoon'],
  eyes: ['Glowing Green', 'Radioactive Red', 'Binary Vision', 'Thermal Infrared'],
  limbs: ['Tentacle Arms', 'Serrated Claws', 'Jet Propulsion', 'Exoskeleton Legs']
};

export default function MutantPetGenerator() {
  const [pet, setPet] = useState({});
  const [dnaCode, setDnaCode] = useState('');

  useEffect(() => {
    generatePet();
  }, []);

  const generatePet = () => {
    const newPet = {};
    Object.entries(DNA_TRAITS).forEach(([traitType, options]) => {
      newPet[traitType] = options[Math.floor(Math.random() * options.length)];
    });
    setPet(newPet);
    setDnaCode(btoa(JSON.stringify(newPet)));
  };

  return (
    <div className="mutant-pet">
      <h1>_MUTANT PET GENERATOR_</h1>
      <div className="dna-traits">
        {Object.entries(pet).map(([trait, value]) => (
          <div key={trait} className="trait">
            <strong>{trait.toUpperCase()}:</strong> {value}
          </div>
        ))}
      </div>
      <div className="controls">
        <button onClick={generatePet}>Generate New Mutant</button>
        <input
          type="text"
          value={dnaCode}
          readOnly
          placeholder="DNA Code"
        />
      </div>
    </div>
  );
}
