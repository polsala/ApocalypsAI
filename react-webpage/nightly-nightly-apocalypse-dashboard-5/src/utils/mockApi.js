export const fetchResources = () => {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve({
        cannedGoods: Math.floor(Math.random() * 1000) + 100,
        cleanWater: Math.floor(Math.random() * 500) + 50,
        ammo: Math.floor(Math.random() * 200) + 20,
        medicalSupplies: Math.floor(Math.random() * 300) + 30
      });
    }, 500); // Mock network latency
  });
};

export const fetchSurvivalOdds = () => {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(Math.floor(Math.random() * 70) + 15); // Between 15% and 85%
    }, 500);
  });
};

export const fetchThreatLevel = () => {
  return new Promise(resolve => {
    setTimeout(() => {
      const levels = ['low', 'medium', 'high'];
      resolve(levels[Math.floor(Math.random() * levels.length)]);
    }, 500);
  });
};

export const fetchAlerts = () => {
  return new Promise(resolve => {
    setTimeout(() => {
      const messages = [
        "The squirrels are organizing. Stay vigilant.",
        "A rogue tumbleweed has been spotted. Evacuate sector 7.",
        "Your pet rock seems unusually concerned. Probably nothing.",
        "The whispers from the void are just static today. A good sign?",
        "Remember to hydrate. Even in the apocalypse."
      ];
      resolve(messages[Math.floor(Math.random() * messages.length)]);
    }, 700);
  });
};
