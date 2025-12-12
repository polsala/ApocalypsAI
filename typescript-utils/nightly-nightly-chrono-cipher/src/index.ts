//!/usr/bin/env node

/**
 * Nightly Chrono Cipher - Time-based encryption CLI
 * Encrypts messages that can only be decrypted at specific future timestamps
 */

interface ChronoMessage {
  version: string;
  startTime: string;
  endTime: string;
  encryptedData: string;
}

/**
 * Simple XOR cipher for demonstration purposes
 * In production, use proper cryptographic libraries
 */
function xorCipher(text: string, key: string): string {
  const keyBytes = key.split('').map(c => c.charCodeAt(0));
  const textBytes = text.split('').map(c => c.charCodeAt(0));
  
  const result = textBytes.map((byte, i) => {
    const keyByte = keyBytes[i % keyBytes.length];
    return byte ^ keyByte;
  });
  
  return String.fromCharCode(...result);
}

/**
 * Generate a time-based key from a timestamp
 */
function generateTimeKey(timestamp: Date): string {
  const timeStr = timestamp.getTime().toString();
  // Create a simple key by repeating and truncating
  const baseKey = `chrono-${timeStr}-key`;
  return baseKey.repeat(Math.ceil(32 / baseKey.length)).slice(0, 32);
}

/**
 * Encrypt a message for a specific time window
 */
function encryptMessage(
  message: string,
  startTime: Date,
  endTime: Date
): string {
  // Validate time window
  if (startTime > endTime) {
    throw new Error('Start time must be before end time');
  }
  
  if (new Date() > startTime) {
    throw new Error('Start time must be in the future');
  }
  
  // Generate encryption key from start time
  const key = generateTimeKey(startTime);
  
  // Encrypt the message
  const encryptedData = xorCipher(message, key);
  
  // Create the chrono message structure
  const chronoMessage: ChronoMessage = {
    version: '1.0',
    startTime: startTime.toISOString(),
    endTime: endTime.toISOString(),
    encryptedData
  };
  
  // Encode as base64
  const jsonStr = JSON.stringify(chronoMessage);
  return Buffer.from(jsonStr, 'utf8').toString('base64');
}

/**
 * Decrypt a chrono-encrypted message
 */
function decryptMessage(encodedMessage: string): string {
  // Decode from base64
  const jsonStr = Buffer.from(encodedMessage, 'base64').toString('utf8');
  const chronoMessage: ChronoMessage = JSON.parse(jsonStr);
  
  // Validate message structure
  if (!chronoMessage.version || !chronoMessage.startTime || !chronoMessage.endTime || !chronoMessage.encryptedData) {
    throw new Error('Invalid encrypted message format');
  }
  
  const now = new Date();
  const startTime = new Date(chronoMessage.startTime);
  const endTime = new Date(chronoMessage.endTime);
  
  // Check if we're in the valid time window
  if (now < startTime) {
    throw new Error(`Message cannot be decrypted yet. Valid from ${startTime.toISOString()}`);
  }
  
  if (now > endTime) {
    throw new Error(`Message decryption window has expired. Was valid until ${endTime.toISOString()}`);
  }
  
  // Generate decryption key from start time
  const key = generateTimeKey(startTime);
  
  // Decrypt the message
  return xorCipher(chronoMessage.encryptedData, key);
}

/**
 * Parse command line arguments
 */
function parseArgs(): { command: string; options: any } {
  const args = process.argv.slice(2);
  const command = args[0];
  const options: any = {};
  
  for (let i = 1; i < args.length; i += 2) {
    const key = args[i]?.replace(/^--/, '');
    const value = args[i + 1];
    
    if (key && value) {
      options[key] = value;
    }
  }
  
  return { command, options };
}

/**
 * Display help information
 */
function showHelp(): void {
  console.log(`
Nightly Chrono Cipher - Time-based encryption CLI

Usage:
  npx nightly-chrono-cipher <command> [options]

Commands:
  encrypt   Encrypt a message for a specific time
  decrypt   Decrypt a time-locked message
  help      Show this help message

Options:
  --message <text>           The message to encrypt/decrypt
  --time <timestamp>         Exact time for decryption (ISO 8601)
  --start <timestamp>        Start of decryption window (ISO 8601)
  --end <timestamp>          End of decryption window (ISO 8601)
  --help                     Show help

Examples:
  npx nightly-chrono-cipher encrypt --message "Secret" --time "2024-12-25T15:30:00"
  npx nightly-chrono-cipher encrypt --message "Window" --start "2024-12-25T09:00:00" --end "2024-12-25T17:00:00"
  npx nightly-chrono-cipher decrypt --message "<base64_encoded_message>"
`);
}

/**
 * Main CLI function
 */
function main(): void {
  const { command, options } = parseArgs();
  
  // Show help if requested or no command
  if (options.help || !command) {
    showHelp();
    return;
  }
  
  try {
    switch (command) {
      case 'encrypt': {
        const message = options.message;
        const time = options.time;
        const start = options.start;
        const end = options.end;
        
        if (!message) {
          throw new Error('Message is required for encryption');
        }
        
        let startTime: Date;
        let endTime: Date;
        
        if (time) {
          startTime = new Date(time);
          endTime = new Date(time);
        } else if (start && end) {
          startTime = new Date(start);
          endTime = new Date(end);
        } else {
          throw new Error('Either --time or both --start and --end are required');
        }
        
        const encrypted = encryptMessage(message, startTime, endTime);
        console.log('Encrypted message:');
        console.log(encrypted);
        break;
      }
      
      case 'decrypt': {
        const message = options.message;
        
        if (!message) {
          throw new Error('Message is required for decryption');
        }
        
        const decrypted = decryptMessage(message);
        console.log('Decrypted message:');
        console.log(decrypted);
        break;
      }
      
      case 'help':
        showHelp();
        break;
      
      default:
        throw new Error(`Unknown command: ${command}`);
    }
  } catch (error) {
    console.error('Error:', error instanceof Error ? error.message : String(error));
    process.exit(1);
  }
}

// Run the CLI if this file is executed directly
if (require.main === module) {
  main();
}

// Export functions for testing
export { encryptMessage, decryptMessage, xorCipher, generateTimeKey };
export type { ChronoMessage };
