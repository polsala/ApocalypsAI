nightly-leetify

A tiny TypeScript CLI that converts ordinary text into leet‑speak.

Install:
npm install -g ts-node typescript

Usage:
npx ts-node src/main.ts "Your text here"
or pipe via stdin:
echo "Hello" | npx ts-node src/main.ts

Options:
-l, --level <number>   Transformation intensity (1-3). Higher levels replace more characters.

Example:
npx ts-node src/main.ts -l 2 "Apocalypse"
Output: 4p0c4lyp53
