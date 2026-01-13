Nightly ANSI Bargraph CLI
==========================

A tiny TypeScript utility that turns a list of numbers into a colourful horizontal bar chart rendered with ANSI block characters. Perfect for quick visualisations in terminalâonly environments â the kind of postâapocalypse data analysis you do on a battered laptop.

Features
--------
* Scales bars to a configurable width (default 40 characters)
* Optional ANSI colour cycling (red, green, blue)
* Reads numbers from a file or STDIN, separated by spaces, commas or newlines
* Exposes a pure function `renderBarChart` for programmatic use

Installation
------------
1. Ensure you have Node.js (>=14) and npm installed.
2. Install ts-node globally (or use npx):
   npm install -g ts-node
3. Clone the repository and navigate to this utility's folder.
   git clone <repoâurl>
   cd utils/nightly-ansi-bargraph-cli
4. Install any needed dependencies (none beyond the Node standard library).

Usage
-----
From a file (or pipe):
   cat numbers.txt | ts-node src/cli.ts --color

Direct file argument:
   ts-node src/cli.ts data.txt

Programmatic use (import the library):
   import { renderBarChart } from "./src/graph";
   console.log(renderBarChart([4, 2, 7]));

Options
-------
--color   Enable ANSI colour cycling for the bars.

Testing
-------
Run the bundled test suite with ts-node:
   npm test

The tests are deterministic and do not require external resources.

License
-------
MIT
