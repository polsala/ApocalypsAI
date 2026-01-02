const defaultMessages = {
  change: [
    "The ancient runes of '{filename}' shimmer with new intent. A change is upon us!",
    "A whisper from the ether: '{filename}' has been touched by unseen hands. What magic unfolds?",
    "The Cauldron bubbles! '{filename}' has been stirred. Expect potent concoctions.",
    "A subtle tremor in the ley lines: '{filename}' has been re-aligned."
  ],
  add: [
    "From the void, '{filename}' manifests! A new artifact enters the realm.",
    "A fresh scroll, '{filename}', unrolls itself. What prophecies does it hold?",
    "Behold! '{filename}' emerges from the mists. The tapestry of creation expands.",
    "A new star, '{filename}', ignites in the cosmic firmament!"
  ],
  delete: [
    "Alas, '{filename}' has faded into legend. Its essence returns to the cosmic dust.",
    "The echoes of '{filename}' diminish. A chapter closes, a void remains.",
    "A sacrifice to the void: '{filename}' is no more. The path ahead is clearer.",
    "The veil thins: '{filename}' dissolves back into the ethereal."
  ]
};

function generateMessage(eventType, filename, customConfig) {
  const messages = customConfig && customConfig[eventType] ? customConfig[eventType] : defaultMessages[eventType];

  if (!messages || messages.length === 0) {
    return `A mysterious event occurred for '{filename}' (type: ${eventType}). The Cauldron is silent.`;
  }

  const randomIndex = Math.floor(Math.random() * messages.length);
  const template = messages[randomIndex];

  return template.replace('{filename}', filename);
}

module.exports = { generateMessage };
