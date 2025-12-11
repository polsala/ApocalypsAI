const greetings = [
  "Greetings, fellow stardust!",
  "Salutations from the cosmic expanse!",
  "Hello, traveler of the nebulae!",
  "A pleasant solar cycle to you!",
  "Ahoy, from the void!"
];

const celestialObjects = [
  "the latest nebula bloom",
  "a particularly shiny asteroid",
  "the dance of binary stars",
  "a rogue comet's tail",
  "the quiet hum of a distant galaxy"
];

const interjections = [
  "Have you seen",
  "Did you notice",
  "I was just pondering",
  "My sensors detected",
  "It's quite remarkable"
];

const themes = [
  "My warp drive is feeling a bit sluggish today. Perhaps a cosmic coffee?",
  "Beware the gravitational pull of existential dread, but enjoy the view!",
  "I think I saw a space whale migrating through the Kuiper Belt.",
  "The silence out here is deafening, yet strangely comforting.",
  "Is it just me, or is that black hole looking particularly hungry today?",
  "I'm trying to teach my pet quasar new tricks.",
  "The quantum foam is particularly bubbly this cycle."
];

function getRandomElement(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function generateCosmicChatter() {
  // With a 50% chance, generate a more structured greeting, otherwise a freeform theme.
  if (Math.random() < 0.5) {
    const greeting = getRandomElement(greetings);
    const interjection = getRandomElement(interjections);
    const celestial = getRandomElement(celestialObjects);
    return `${greeting} ${interjection} ${celestial}?`;
  } else {
    return getRandomElement(themes);
  }
}

console.log(generateCosmicChatter());
