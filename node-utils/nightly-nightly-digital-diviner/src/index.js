const os = require('os');

function getCpuProphecy(normalizedLoad) {
  if (normalizedLoad > 0.8) {
    return "The processing core hums with an urgent, frantic energy. The Oracle of Overload whispers: 'Seek respite, lest the circuits melt into digital slag!'";
  } else if (normalizedLoad >= 0.3) {
    return "The computational gears turn with a steady, purposeful rhythm. The Oracle of Efficiency nods: 'Your efforts are well-paced, survivor. Maintain this balance.'";
  } else {
    return "A profound stillness settles upon the processing plains. The Oracle of Potential declares: 'The digital canvas is blank. What grand design will you manifest next?'";
  }
}

function getMemoryVision(memoryUsageRatio) {
  if (memoryUsageRatio > 0.8) {
    return "The memory banks groan under the weight of accumulated data. The Oracle of Retention warns: 'Unburden your mind, clear the caches, or risk the collapse of thought!'";
  } else if (memoryUsageRatio >= 0.3) {
    return "Memory flows like a well-tended spring. The Oracle of Clarity smiles: 'Your digital mind is sharp and ready. Proceed with purpose.'";
  } else {
    return "The memory void stretches, vast and inviting. The Oracle of Expansion beckons: 'Embrace new knowledge, for there is ample space for growth!'";
  }
}

function divine() {
  const cpuCount = os.cpus().length;
  const loadAvg = os.loadavg()[0]; // 1-minute load average
  const normalizedLoad = loadAvg / cpuCount;

  const totalMem = os.totalmem();
  const freeMem = os.freemem();
  const usedMem = totalMem - freeMem;
  const memoryUsageRatio = usedMem / totalMem;

  console.log('🌌 The Nightly Digital Diviner speaks! 🌌\n');
  console.log(`CPU Prophecy: ${getCpuProphecy(normalizedLoad)}`);
  console.log(`Memory Vision: ${getMemoryVision(memoryUsageRatio)}`);
}

// Only run if executed directly
if (require.main === module) {
  divine();
}

module.exports = { getCpuProphecy, getMemoryVision, divine };
