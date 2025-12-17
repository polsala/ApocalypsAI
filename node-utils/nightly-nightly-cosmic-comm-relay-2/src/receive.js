const { receiveMessages } = require('./main');

const args = process.argv.slice(2);

if (args.length < 1) {
    console.error('Usage: node src/receive.js <your_id>');
    process.exit(1);
}

const myId = args[0];

receiveMessages(myId);
