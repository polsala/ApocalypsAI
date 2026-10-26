#!/usr/bin/env node
import { main } from './cli';

// Execute the main CLI function with arguments, excluding 'node' and the script path.
main(process.argv.slice(2));
