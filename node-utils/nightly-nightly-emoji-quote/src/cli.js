#!/usr/bin/env node
const { getQuoteWithEmoji } = require('./index');

(async () => {
  try {
    const message = await getQuoteWithEmoji();
    console.log(message);
  } catch (err) {
    console.error('Error fetching quote:', err.message);
    process.exit(1);
  }
})();
