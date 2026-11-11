const attireRules = {
  "Irradiated Haze": {
    "Scavenging": "Lead-lined poncho, gas mask (Type-A filter), sturdy boots, Geiger counter.",
    "Bunker Formal": "Cleaned hazmat suit, polished respirator, emergency rations pouch.",
    "Raid Prep": "Reinforced combat suit, radiation shield vest, tactical goggles.",
    "Trading Post Visit": "Light hazmat jacket (stylish!), filtered scarf, barter pouch.",
    "Stargazing (if visible)": "Thick, insulated suit, oxygen rebreather, telescope (radiation hardened)."
  },
  "Acid Rain": {
    "Scavenging": "Acid-proof slicker, full-face visor, rubber boots, acid-neutralizing spray.",
    "Bunker Formal": "Ceremonial acid-resistant cloak, waterproof formal wear, umbrella (reinforced).",
    "Raid Prep": "Heavy-duty acid-resistant armor, ballistic helmet with visor, plasma cutter.",
    "Trading Post Visit": "Waterproof trench coat, wide-brimmed hat, sealed satchel.",
    "Stargazing (if visible)": "Full environmental suit, portable shelter, acid-resistant binoculars."
  },
  "Dust Storm": {
    "Scavenging": "Dust-goggles, face wrap, light but durable clothing, water canteen.",
    "Bunker Formal": "Finely woven dust-cloak, ceremonial head wrap, sand-resistant shoes.",
    "Raid Prep": "Desert camo, sand-goggles, high-capacity water pack, survival knife.",
    "Trading Post Visit": "Loose-fitting robes, wide-brimmed hat, dust-proof bag.",
    "Stargazing (if visible)": "Clear-vision goggles, heavy blanket, wind-resistant shelter."
  },
  "Mutant Downpour": {
    "Scavenging": "Biohazard suit (Level 3), heavy-duty gloves, mutant repellent spray, tranquilizer rifle.",
    "Bunker Formal": "Formal bio-suit, ceremonial mutant-hide sash, polished boots.",
    "Raid Prep": "Exoskeleton armor, sonic deterrent, heavy plasma rifle, medkit.",
    "Trading Post Visit": "Discreet bio-suit, hooded cloak, concealed weapon.",
    "Stargazing (if visible)": "Reinforced observation dome, long-range scanner, tranquilizer darts."
  },
  "Clear but Cold Void": {
    "Scavenging": "Thermal layers, insulated jacket, thick gloves, headlamp, survival blanket.",
    "Bunker Formal": "Woolen formal wear, fur-lined coat, heated boots, hot beverage flask.",
    "Raid Prep": "Arctic combat gear, thermal vision goggles, portable heater, ice axe.",
    "Trading Post Visit": "Heavy cloak, warm hat, insulated boots, hot rock pouch.",
    "Stargazing (if visible)": "Heated observation suit, high-power telescope, thermos of 'void tea'."
  }
};

const weatherConditions = Object.keys(attireRules);
const moods = Object.keys(attireRules[weatherConditions[0]]); // Assuming all weather conditions have the same moods

module.exports = {
  attireRules,
  weatherConditions,
  moods
};
