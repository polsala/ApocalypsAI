import React, { useState } from 'react';
import './App.css';

function App() {
  const [food, setFood] = useState(100);
  const [water, setWater] = useState(150);
  const [meds, setMeds] = useState(20);
  const [survivors, setSurvivors] = useState(10);
  const [allocationResults, setAllocationResults] = useState(null);

  const calculateAllocation = () => {
    if (survivors <= 0) {
      setAllocationResults({ error: "Number of survivors must be greater than 0." });
      return;
    }

    // Whimsical daily needs per survivor
    const foodPerSurvivor = 2; // rations
    const waterPerSurvivor = 3; // units
    const medsPerSurvivor = 0.5; // kits (rounded up)

    const requiredFood = survivors * foodPerSurvivor;
    const requiredWater = survivors * waterPerSurvivor;
    const requiredMeds = Math.ceil(survivors * medsPerSurvivor);

    const allocatedFood = Math.min(food, requiredFood);
    const allocatedWater = Math.min(water, requiredWater);
    const allocatedMeds = Math.min(meds, requiredMeds);

    const remainingFood = food - allocatedFood;
    const remainingWater = water - allocatedWater;
    const remainingMeds = meds - allocatedMeds;

    // Morale calculation
    let morale = "High";
    let moraleEmoji = "😊";
    let unmetNeedsCount = 0;
    if (allocatedFood < requiredFood) unmetNeedsCount++;
    if (allocatedWater < requiredWater) unmetNeedsCount++;
    if (allocatedMeds < requiredMeds) unmetNeedsCount++;

    if (unmetNeedsCount === 1) {
      morale = "Medium";
      moraleEmoji = "😐";
    } else if (unmetNeedsCount >= 2) {
      morale = "Low";
      moraleEmoji = "😟";
    }

    // Scavenging Success Chance (whimsical, based on morale)
    let scavengingChance = "Uncertain";
    if (morale === "High") {
      scavengingChance = "High (80% chance of finding something useful!)";
    } else if (morale === "Medium") {
      scavengingChance = "Moderate (50% chance, but beware of raiders!)";
    } else {
      scavengingChance = "Low (20% chance, better stay put or risk it all!)";
    }

    setAllocationResults({
      allocatedFood,
      allocatedWater,
      allocatedMeds,
      remainingFood,
      remainingWater,
      remainingMeds,
      morale,
      moraleEmoji,
      scavengingChance,
      requiredFood,
      requiredWater,
      requiredMeds
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Resource Allocator</h1>
        <p>For a thriving post-apocalyptic community!</p>
      </header>
      <div className="container">
        <div className="input-section">
          <h2>Current Inventory</h2>
          <div className="input-group">
            <label>Food Rations:</label>
            <input
              type="number"
              value={food}
              onChange={(e) => setFood(Math.max(0, parseInt(e.target.value) || 0))}
            />
          </div>
          <div className="input-group">
            <label>Water Units:</label>
            <input
              type="number"
              value={water}
              onChange={(e) => setWater(Math.max(0, parseInt(e.target.value) || 0))}
            />
          </div>
          <div className="input-group">
            <label>Medical Kits:</label>
            <input
              type="number"
              value={meds}
              onChange={(e) => setMeds(Math.max(0, parseInt(e.target.value) || 0))}
            />
          </div>
          <div className="input-group">
            <label>Number of Survivors:</label>
            <input
              type="number"
              value={survivors}
              onChange={(e) => setSurvivors(Math.max(1, parseInt(e.target.value) || 1))}
            />
          </div>
          <button onClick={calculateAllocation}>Calculate Allocation</button>
        </div>

        {allocationResults && (
          <div className="results-section">
            <h2>Allocation Report</h2>
            {allocationResults.error ? (
              <p className="error-message">{allocationResults.error}</p>
            ) : (
              <>
                <div className="allocation-summary">
                  <h3>Daily Needs & Allocation:</h3>
                  <p>Food: {allocationResults.allocatedFood} / {allocationResults.requiredFood} rations allocated</p>
                  <p>Water: {allocationResults.allocatedWater} / {allocationResults.requiredWater} units allocated</p>
                  <p>Medical Kits: {allocationResults.allocatedMeds} / {allocationResults.requiredMeds} kits allocated</p>
                </div>
                <div className="remaining-summary">
                  <h3>Remaining Inventory:</h3>
                  <p>Food: {allocationResults.remainingFood} rations</p>
                  <p>Water: {allocationResults.remainingWater} units</p>
                  <p>Medical Kits: {allocationResults.remainingMeds} kits</p>
                </div>
                <div className="morale-section">
                  <h3>Community Morale: <span className="morale-emoji">{allocationResults.moraleEmoji}</span> {allocationResults.morale}</h3>
                </div>
                <div className="scavenging-section">
                  <h3>Next Scavenging Success Chance:</h3>
                  <p>{allocationResults.scavengingChance}</p>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
