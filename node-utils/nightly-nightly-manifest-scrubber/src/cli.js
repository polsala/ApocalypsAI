#!/usr/bin/env node

const { scrubFileContent } = require('./index');
const { Command } = require('commander');
const program = new Command();

program
    .name('nightly-manifest-scrubber')
    .description('A Node.js CLI tool to clean configuration files by removing comments, empty lines, and optionally redacting sensitive patterns.')
    .version('1.0.0');

program
    .argument('<file>', 'Path to the input file to scrub.')
    .option('-o, --output <file>', 'Path to the output file. If not provided, prints to stdout.')
    .option('-c, --no-comments', 'Do not remove lines starting with # or //. By default, comments are removed.')
    .option('-e, --no-empty-lines', 'Do not remove empty lines. By default, empty lines are removed.')
    .option('-r, --redact <patterns...>', 'Space-separated list of regex patterns to redact. Example: "API_KEY=.*" "PASSWORD=.*"')
    .option('-p, --placeholder <text>', 'Placeholder text for redacted content. Default: [REDACTED]', '[REDACTED]')
    .action((file, options) => {
        try {
            const scrubOptions = {
                removeComments: !options.noComments,
                removeEmptyLines: !options.noEmptyLines,
                redactPatterns: options.redact || [],
                redactionPlaceholder: options.placeholder,
                outputFile: options.output
            };
            const scrubbedContent = scrubFileContent(file, scrubOptions);
            if (!options.output) {
                console.log(scrubbedContent);
            } else {
                console.log(`Successfully scrubbed '${file}' to '${options.output}'.`);
            }
        } catch (error) {
            console.error(`Error: ${error.message}`);
            process.exit(1);
        }
    });

program.parse(process.argv);
