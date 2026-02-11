#!/usr/bin/env node
const yargs = require('yargs');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const path = require('path');

const BOTTLES_DIR = path.join(process.cwd(), 'bottles');

// Ensure the bottles directory exists
if (!fs.existsSync(BOTTLES_DIR)) {
  fs.mkdirSync(BOTTLES_DIR, { recursive: true });
}

const bottleMessage = (message) => {
  const id = uuidv4();
  const timestamp = new Date().toISOString();
  const encodedMessage = Buffer.from(message).toString('base64');

  const bottle = {
    id,
    timestamp,
    encodedMessage,
    originalLength: message.length,
    encoding: 'base64',
  };

  const filename = path.join(BOTTLES_DIR, `bottle-${id}.json`);
  fs.writeFileSync(filename, JSON.stringify(bottle, null, 2), 'utf8');

  console.log(`Message bottled! ID: ${id}`);
  console.log(`File: ${filename}`);
  return { id, filename }; // For testing
};

const uncorkMessage = (bottleIdOrPath) => {
  let filename;
  if (fs.existsSync(bottleIdOrPath) && bottleIdOrPath.endsWith('.json')) {
    filename = bottleIdOrPath;
  } else {
    filename = path.join(BOTTLES_DIR, `bottle-${bottleIdOrPath}.json`);
  }

  if (!fs.existsSync(filename)) {
    console.error(`Error: Bottle '${bottleIdOrPath}' not found.`);
    process.exit(1);
  }

  const bottleContent = fs.readFileSync(filename, 'utf8');
  const bottle = JSON.parse(bottleContent);

  const decodedMessage = Buffer.from(bottle.encodedMessage, 'base64').toString('utf8');

  console.log('--- Uncorked Message ---');
  console.log(`ID: ${bottle.id}`);
  console.log(`Timestamp: ${bottle.timestamp}`);
  console.log(`Original Length: ${bottle.originalLength}`);
  console.log(`Encoding: ${bottle.encoding}`);
  console.log('------------------------');
  console.log(decodedMessage);
  console.log('------------------------');
  return { id: bottle.id, message: decodedMessage }; // For testing
};

yargs
  .command(
    'bottle <message>',
    'Encodes and saves a message into a digital bottle.',
    (yargs) => {
      yargs.positional('message', {
        description: 'The message to bottle.',
        type: 'string',
      });
    },
    (argv) => {
      bottleMessage(argv.message);
    }
  )
  .command(
    'uncork <bottleIdOrPath>',
    'Retrieves and decodes a message from a digital bottle.',
    (yargs) => {
      yargs.positional('bottleIdOrPath', {
        description: 'The ID of the bottle or the full path to the bottle file.',
        type: 'string',
      });
    },
    (argv) => {
      uncorkMessage(argv.bottleIdOrPath);
    }
  )
  .demandCommand(1, 'You need to specify a command.')
  .help()
  .argv;

// Export for testing
module.exports = { bottleMessage, uncorkMessage, BOTTLES_DIR };
