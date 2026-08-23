#!/usr/bin/env node

import { voidEchoTypeChecker } from './index';
import { registerDefaultSchemas } from './schemas';

// Register default schemas for the CLI instance
registerDefaultSchemas(voidEchoTypeChecker);

function runCli() {
  const args = process.argv.slice(2);

  if (args.length < 3 || args[0] !== 'validate') {
    console.log('Usage: nightly-void-echo-type-checker validate <schema-name> <message-type> <message-content>');
    console.log('  <schema-name>: Name of the registered schema (e.g., simple-status, structured-log, anomaly-report)');
    console.log('  <message-type>: "string" or "json"');
    console.log('  <message-content>: The message to validate. If "json", provide a JSON string.');
    process.exit(1);
  }

  const schemaName = args[1];
  const messageType = args[2];
  let messageContent: string | object = args.slice(3).join(' '); // Join remaining args for message

  if (messageType === 'json') {
    try {
      messageContent = JSON.parse(messageContent as string);
    } catch (e) {
      console.error('Error: Invalid JSON message content provided.');
      process.exit(1);
    }
  } else if (messageType !== 'string') {
    console.error('Error: Invalid message type. Must be "string" or "json".');
    process.exit(1);
  }

  const result = voidEchoTypeChecker.validate(schemaName, messageContent);

  if (result.isValid) {
    console.log(`✅ Message is valid against schema "${schemaName}".`);
    process.exit(0);
  } else {
    console.error(`❌ Message is INVALID against schema "${schemaName}".`);
    if (result.errors) {
      result.errors.forEach(err => console.error(`   - ${err}`));
    }
    process.exit(1);
  }
}

runCli();
