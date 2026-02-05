const fs = require('fs');

function getEmoji(seed) {
  const emojis = ["🌟","🚀","🔥","💡","🎉","🛠️","🤖","🧩","⚡","🧪"];
  if (seed !== undefined) {
    const idx = parseInt(seed, 10) % emojis.length;
    return emojis[idx];
  }
  // pseudo‑random based on current time
  const idx = Math.floor(Math.random() * emojis.length);
  return emojis[idx];
}

function run() {
  const message = process.env['INPUT_MESSAGE'];
  if (!message) {
    console.error('::error::Input "message" is required');
    process.exit(1);
  }
  const seed = process.env['SEED'];
  const emoji = getEmoji(seed);
  const annotated = `${message} ${emoji}`;
  console.log(`::set-output name=annotated_message::${annotated}`);
  // also write to stdout for visibility
  console.log(annotated);
}

run();
