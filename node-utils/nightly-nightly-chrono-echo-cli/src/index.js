#!/usr/bin/env node

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// Helper for argument parsing
const getArg = (flag) => {
    const index = process.argv.indexOf(flag);
    return index > -1 && process.argv.length > index + 1 ? process.argv[index + 1] : null;
};

const hasArg = (flag) => process.argv.includes(flag);

const command = getArg('--command');
const echoFile = getArg('--file') || 'chrono-echo.json';
const mode = hasArg('--capture') ? 'capture' : (hasArg('--replay') ? 'replay' : null);
const delayMs = parseInt(getArg('--delay') || '0', 10);
const distortionType = getArg('--distort'); // 'shift', 'ghost'

const distortOutput = (output, type) => {
    if (!type) return output;

    if (type === 'shift') {
        return output.split('').map(char => {
            if (Math.random() < 0.05 && char.match(/[a-zA-Z0-9]/)) { // 5% chance to shift alphanumeric chars
                const offset = Math.random() < 0.5 ? 1 : -1;
                return String.fromCharCode(char.charCodeAt(0) + offset);
            }
            return char;
        }).join('');
    } else if (type === 'ghost') {
        const ghostMessage = "\n[...a faint echo of the past whispers...]\n";
        return output + ghostMessage;
    }
    return output;
};

const capture = async (cmd, args, file) => {
    console.log(`Capturing command: ${cmd} ${args.join(' ')} to ${file}`);
    let stdout = '';
    let stderr = '';
    let exitCode = 0;

    try {
        const child = spawn(cmd, args, { shell: true });

        child.stdout.on('data', (data) => {
            stdout += data.toString();
            process.stdout.write(data); // Also print to console during capture
        });

        child.stderr.on('data', (data) => {
            stderr += data.toString();
            process.stderr.write(data); // Also print to console during capture
        });

        await new Promise((resolve, reject) => {
            child.on('close', (code) => {
                exitCode = code;
                resolve();
            });
            child.on('error', (err) => {
                console.error(`Failed to start subprocess: ${err}`);
                reject(err);
            });
        });

        const echoData = {
            command: `${cmd} ${args.join(' ')}`,
            timestamp: new Date().toISOString(),
            stdout,
            stderr,
            exitCode,
        };
        fs.writeFileSync(file, JSON.stringify(echoData, null, 2));
        console.log(`\nCapture complete. Echo saved to ${file}`);
    } catch (error) {
        console.error(`Error during capture: ${error.message}`);
        process.exit(1);
    }
};

const replay = async (file, delay, distortion) => {
    console.log(`Replaying echo from ${file} with delay ${delay}ms and distortion '${distortion || "none"}'`);
    try {
        const echoData = JSON.parse(fs.readFileSync(file, 'utf8'));

        const replayOutput = (output, stream) => {
            if (output) {
                const distorted = distortOutput(output, distortion);
                stream.write(distorted);
            }
        };

        await new Promise(resolve => setTimeout(resolve, delay));
        replayOutput(echoData.stdout, process.stdout);

        await new Promise(resolve => setTimeout(resolve, delay)); // Separate delay for stderr
        replayOutput(echoData.stderr, process.stderr);

        console.log(`\nReplay complete. Original exit code: ${echoData.exitCode}`);
        process.exit(echoData.exitCode);

    } catch (error) {
        console.error(`Error during replay: ${error.message}`);
        process.exit(1);
    }
};

const run = async () => {
    if (!mode) {
        console.log("Usage: nightly-chrono-echo-cli --capture --command \"<your command>\" [--file <echo_file.json>]");
        console.log("       nightly-chrono-echo-cli --replay [--file <echo_file.json>] [--delay <ms>] [--distort <shift|ghost>]");
        process.exit(1);
    }

    if (mode === 'capture') {
        if (!command) {
            console.error("Error: --command is required for capture mode.");
            process.exit(1);
        }
        const cmdParts = command.split(' ');
        const cmd = cmdParts[0];
        const args = cmdParts.slice(1);
        await capture(cmd, args, echoFile);
    } else if (mode === 'replay') {
        await replay(echoFile, delayMs, distortionType);
    }
};

run();
