const emojis = ["😀","🚀","🌟","🔥","💡","🎉","🧩","🛠️","📦","🤖"];function getRandomEmoji() {const idx = Math.floor(Math.random() * emojis.length);return emojis[idx];}module.exports = { getRandomEmoji };
