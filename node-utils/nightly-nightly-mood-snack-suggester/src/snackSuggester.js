const snackData = {
  grumpy: {
    name: "Irradiated Twinkie",
    description: "A classic for a reason. Its eternal shelf-life mirrors your eternal grumpiness. Best served with a side of existential dread."
  },
  energetic: {
    name: "Mutant Berry Blend",
    description: "Harvested from the glowing wilds, these berries provide a questionable but potent burst of energy. May cause temporary bioluminescence."
  },
  contemplative: {
    name: "Dusty Can of Beans (vintage 2042)",
    description: "Perfect for quiet reflection by the flickering barrel fire. Each bean a tiny universe of thought. Best consumed slowly, one bean at a time."
  },
  hopeful: {
    name: "Foraged Mushroom Surprise",
    description: "A rare find! Hopefully, it's the edible kind. A gamble, much like hope itself. Chew thoroughly."
  },
  anxious: {
    name: "Pre-War Emergency Rations Bar",
    description: "Dense, flavorless, and reassuringly bland. It reminds you that even in chaos, some things remain predictably unexciting. Good for calming frayed nerves."
  },
  bored: {
    name: "Mystery Meat Jerky",
    description: "The ultimate boredom cure: trying to guess what animal it once was. A culinary adventure for the truly uninspired."
  }
};

function getSnackSuggestion(mood) {
  const normalizedMood = mood.toLowerCase();
  return snackData[normalizedMood] || {
    name: "Dehydrated Nutrient Paste",
    description: "When your mood is beyond classification, or simply 'meh', this universal sustenance will do. It's... food."
  };
}

module.exports = { getSnackSuggestion };
