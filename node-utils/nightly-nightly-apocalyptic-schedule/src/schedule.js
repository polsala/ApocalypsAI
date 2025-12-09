const tasks = [
  'Barricade the Wi-Fi router',
  'Scavenge for GitHub stars',
  'Radiation coffee brewing',
  'Server chicken coop maintenance',
  'Code cave meditation',
  'Debug the nuclear reactor',
  'Patch the firewall with duct tape',
  'Recalibrate the doomsday clock',
  'Salvage RAM from zombies',
  'Rebuild the internet in a shoebox'
];

function generateSchedule() {
  const times = [];
  const hours = Array.from({length: 12}, (_, i) => `${i + 8}:00 AM`);

  // Create calendar ASCII art with random X
  const calendar = Array(7).fill('');
  for (let i = 0; i < 7; i++) {
    calendar[i] = Array(7).fill(' ').map((_, j) => {
      return i === 0 && j === Math.floor(Math.random() * 7) ? 'X' : ' '; 
    }).join('[]');
  }

  // Generate time-blocked tasks
  for (const time of hours) {
    const taskIndex = Math.floor(Math.random() * tasks.length);
    times.push({
      time,
      task: tasks[taskIndex]
    });
  }

  return {
    asciiArt: calendar.join('\n'),
    times
  };
}

module.exports = { generateSchedule };
