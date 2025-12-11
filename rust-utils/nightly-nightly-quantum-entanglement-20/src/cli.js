// CLI interface for Quantum Entanglement Checker
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const yargs = require('yargs');
const chalk = require('chalk');

// Rust binary path
const RUST_BINARY = path.join(__dirname, '../target/release/quantum_entanglement_checker');

function runRustBinary(args) {
    return new Promise((resolve, reject) => {
        const child = spawn(RUST_BINARY, args, {
            stdio: ['pipe', 'pipe', 'pipe']
        });
        
        let stdout = '';
        let stderr = '';
        
        child.stdout.on('data', (data) => {
            stdout += data.toString();
        });
        
        child.stderr.on('data', (data) => {
            stderr += data.toString();
        });
        
        child.on('close', (code) => {
            if (code === 0) {
                resolve(stdout);
            } else {
                reject(new Error(`Rust binary exited with code ${code}: ${stderr}`));
            }
        });
        
        child.on('error', (err) => {
            reject(err);
        });
    });
}

async function checkEntanglement(file1, file2) {
    console.log(chalk.blue('🔬 Checking quantum entanglement between files...'));
    
    try {
        const result = await runRustBinary(['check', file1, file2]);
        console.log(chalk.green('✅ Entanglement check completed!'));
        console.log(result);
    } catch (error) {
        console.error(chalk.red('❌ Error checking entanglement:'), error.message);
        process.exit(1);
    }
}

async function generateNetwork(dir, threshold) {
    console.log(chalk.blue('🕸️  Generating entanglement network...'));
    
    try {
        const result = await runRustBinary(['network', dir, threshold.toString()]);
        console.log(chalk.green('✅ Network generation completed!'));
        console.log(result);
    } catch (error) {
        console.error(chalk.red('❌ Error generating network:'), error.message);
        process.exit(1);
    }
}

async function visualizeGraph(graphFile) {
    console.log(chalk.blue('📊 Visualizing entanglement graph...'));
    
    try {
        const result = await runRustBinary(['visualize', graphFile]);
        console.log(chalk.green('✅ Visualization completed!'));
        console.log(result);
    } catch (error) {
        console.error(chalk.red('❌ Error visualizing graph:'), error.message);
        process.exit(1);
    }
}

// CLI argument parsing
const argv = yargs
    .usage('Usage: $0 <command> [options]')
    .command('check', 'Check entanglement between two files', {
        file1: {
            describe: 'First file to check',
            type: 'string',
            demandOption: true
        },
        file2: {
            describe: 'Second file to check',
            type: 'string',
            demandOption: true
        }
    })
    .command('network', 'Generate entanglement network for a directory', {
        dir: {
            describe: 'Directory to analyze',
            type: 'string',
            demandOption: true
        },
        threshold: {
            describe: 'Entanglement threshold (0.0-1.0)',
            type: 'number',
            default: 0.5
        }
    })
    .command('visualize', 'Visualize entanglement graph', {
        graph: {
            describe: 'Graph file to visualize',
            type: 'string',
            demandOption: true
        }
    })
    .help()
    .alias('help', 'h')
    .argv;

// Main execution
async function main() {
    console.log(chalk.magenta('🌌 Welcome to the Quantum Entanglement Checker!'));
    console.log(chalk.magenta('Where files become quantumly entangled... or not. 🚀'));
    console.log();
    
    if (argv._[0] === 'check') {
        await checkEntanglement(argv.file1, argv.file2);
    } else if (argv._[0] === 'network') {
        await generateNetwork(argv.dir, argv.threshold);
    } else if (argv._[0] === 'visualize') {
        await visualizeGraph(argv.graph);
    } else {
        console.log(chalk.yellow('Please specify a command: check, network, or visualize'));
        yargs.showHelp();
        process.exit(1);
    }
}

// Check if Rust binary exists
if (!fs.existsSync(RUST_BINARY)) {
    console.error(chalk.red('❌ Rust binary not found at:'), RUST_BINARY);
    console.error(chalk.yellow('Please build the Rust core first: cargo build --release'));
    process.exit(1);
}

// Run main function
main().catch((error) => {
    console.error(chalk.red('❌ Unexpected error:'), error);
    process.exit(1);
});
