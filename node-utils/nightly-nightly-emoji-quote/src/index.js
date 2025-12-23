const https = require('https');

const EMOJIS = ['😀','😃','😄','😁','😆','😅','😂','🤣','😊','😇','🙂','🙃','😉','😌','😍','🥰','😘','😗','😙','😚','😋','😛','😜','🤪','🤨','🧐','🤓','😎','🤩','🥳','😏','😒','😞','😔','😟','😕','🙁','☹️','😣','😖','😫','😩','🥺','😢','😭','😤','😠','😡','🤬','🤯','😳','🥵','🥶','😱','😨','😰','😥','😓','🤗','🤔','🤭','🤫','🤥','😶','😐','😑','😬','🙄','😯','😦','😧','😮','😲','🥱','😴','🤤','😪','😵','🤐','🥴','🤢','🤮','🤧','😷','🤒','🤕','🤑','🤠','😈','👿','👹','👺','🤡','💩','👻','💀','☠️','👽','🤖','🎃','😺','😸','😹','😻','😼','😽','🙀','😿','😾'];
function getRandomEmoji() {
  return EMOJIS[Math.floor(Math.random() * EMOJIS.length)];
}

function fetchQuote(fetchFn) {
  if (fetchFn) {
    return fetchFn();
  }
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.quotable.io',
      path: '/random',
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    };
    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.content);
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

async function getQuoteWithEmoji(fetchFn) {
  const quote = await fetchQuote(fetchFn);
  const emoji = getRandomEmoji();
  return `${emoji} ${quote}`;
}

module.exports = { getQuoteWithEmoji, fetchQuote, getRandomEmoji };
