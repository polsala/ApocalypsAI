const { sendMessage } = require('./main');

const args = process.argv.slice(2);

if (args.length < 2) {
    console.error('Usage: node src/send.js <recipient_id> <your_message>');
    process.exit(1);
}

const recipientId = args[0];
const message = args.slice(1).join(' ');

sendMessage(recipientId, message);
