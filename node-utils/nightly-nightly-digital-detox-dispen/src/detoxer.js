const activities = [
  { text: "🌌 Gaze at the stars or clouds. Contemplate the vastness of the cosmos and your place within the temporal flux.", categories: ["mindful", "creative"] },
  { text: "🌳 Take a walk in the nearest green space. Observe the resilience of nature in the face of entropy.", categories: ["physical", "mindful"] },
  { text: "📖 Read a physical book. Let the scent of aged paper transport you to another reality.", categories: ["mindful", "creative"] },
  { text: "✍️ Write a letter to a friend, or start a journal. Document your observations of the post-digital era.", categories: ["creative"] },
  { text: "🎨 Create something with your hands: draw, paint, sculpt, or build a miniature shelter.", categories: ["creative"] },
  { text: "🍳 Cook a complex meal from scratch. Master the ancient art of sustenance.", categories: ["practical"] },
  { text: "🧘 Practice meditation or deep breathing. Find your inner calm amidst the digital static.", categories: ["mindful"] },
  { text: "🧹 Tidy your physical space. A clear environment fosters a clear mind, even in the wasteland.", categories: ["practical"] },
  { text: "🗣️ Engage in a face-to-face conversation. Reconnect with the organic network.", categories: ["social"] },
  { text: "🎶 Listen to music without distractions. Let the vibrations soothe your weary soul.", categories: ["mindful"] },
  { text: "🧩 Solve a puzzle or play a board game. Sharpen your strategic mind for future challenges.", categories: ["mindful", "creative"] },
  { text: "🛠️ Fix something broken around your dwelling. Embrace the spirit of the scavenger.", categories: ["practical"] }
];

const messageTemplates = [
  "Greetings, fellow travelers of the digital ether. I am currently embarking on a {duration} journey to {reason}, a necessary recalibration for my temporal sensors. I shall return when the echoes of the void subside. Until then, may your signals remain strong and your data uncorrupted.",
  "Attention, digital denizens! I am temporarily retreating from the network for {duration} to {reason}. My consciousness requires a brief respite from the data streams. Expect my return when the stars align, or my battery recharges, whichever comes first.",
  "Initiating a {duration} period of deep contemplation and {reason}. The digital realm will be momentarily devoid of my presence. Do not send out search parties; I am merely seeking analog enlightenment. Transmission ends.",
  "My apologies, but I am currently unavailable. I've ventured into the great offline unknown for {duration} to {reason}. I will resurface when my quest is complete, or when the coffee runs out. Over and out."
];

function generateActivity(preferences = []) {
  let filteredActivities = activities;
  if (preferences.length > 0) {
    filteredActivities = activities.filter(activity =>
      preferences.some(pref => activity.categories.includes(pref.toLowerCase()))
    );
  }
  if (filteredActivities.length === 0) {
    filteredActivities = activities; // Fallback to all activities if no match
  }
  const randomIndex = Math.floor(Math.random() * filteredActivities.length);
  return filteredActivities[randomIndex].text;
}

function generateMessage(duration = "an unspecified period", reason = "recharge my essence") {
  const randomIndex = Math.floor(Math.random() * messageTemplates.length);
  let message = messageTemplates[randomIndex];
  message = message.replace('{duration}', duration);
  message = message.replace('{reason}', reason);
  return message;
}

module.exports = {
  generateActivity,
  generateMessage,
  activities: activities.map(a => a.text), // Export just the text for listing
  messageTemplates
};
