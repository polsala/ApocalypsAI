const { getRandomEmoji } = require('./emoji');
const emoji = getRandomEmoji();
console.log(`::set-output name=emoji::${emoji}`);
