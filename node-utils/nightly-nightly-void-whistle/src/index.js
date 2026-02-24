"use strict";
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

function playSound(soundName) {
  const soundPath = path.join(__dirname, '..', 'sounds', `${soundName}.wav`);
  if (!fs.existsSync(soundPath)) {
    console.error(`Sound not found: ${soundName}`);
    return;
  }

  let player;
  if (process.platform === 'darwin') {
    player = spawn('afplay', [soundPath]);
  } else if (process.platform === 'win32') {
    player = spawn('powershell', ['-c', `New-Object Media.SoundPlayer "${soundPath}"; $player.PlaySync()`], { shell: true });
  } else {
    player = spawn('aplay', [soundPath]);
  }

  player.on('error', () => {
    console.warn('Could not play sound. Install aplay (Linux), afplay (macOS), or use PowerShell (Windows).');
  });
}

function main() {
  const args = process.argv.slice(2);
  let sound = 'chime';
  let commandIndex = 0;

  // Parse --sound option
  if (args[0] === '--sound' && args[1]) {
    sound = args[1];
    commandIndex = 2;
  } else if (args[0]?.startsWith('--sound=')) {
    sound = args[0].split('=')[1];
    commandIndex = 1;
  }

  const commandToRun = args.slice(commandIndex);

  if (commandToRun.length === 0) {
    console.log('Usage: void-whistle [--sound <name>] -- <command>');
    process.exit(1);
  }

  const proc = spawn(commandToRun[0], commandToRun.slice(1), { stdio: 'inherit' });

  proc.on('close', (code) => {
    playSound(sound);
    process.exit(code);
  });
}

if (require.main === module) {
  main();
}
