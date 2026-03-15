#!/usr/bin/env node
import { stdin } from 'node:process';

function rot13(str) {
  return str.replace(/[a-zA-Z]/g, c => {
    const base = c <= 'Z' ? 65 : 97;
    return String.fromCharCode(((c.charCodeAt(0) - base + 13) % 26) + base);
  });
}

function readStdin(callback) {
  let data = '';
  stdin.setEncoding('utf8');
  stdin.on('data', chunk => data += chunk);
  stdin.on('end', () => callback(data));
  stdin.resume();
}

function main() {
  const arg = process.argv[2];
  if (arg) {
    console.log(rot13(arg));
  } else {
    readStdin(input => {
      console.log(rot13(input.trim()));
    });
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
