Nightly ISO8601 Duration Parser

A tiny utility that parses ISO 8601 duration strings (e.g., PT1H30M) into an object with hours, minutes, seconds and can format them into a readable sentence.

Installation

Copy the folder into your project and run `node src/index.js \"PT2H15M\"`.

Usage

Command line: `node src/index.js \"<duration>\"` prints formatted duration.

Programmatic usage:

const { parseISO8601Duration, formatDuration } = require("./src/index.js");
const obj = parseISO8601Duration("PT1H45M");
console.log(formatDuration(obj)); // 1 hour, 45 minutes
