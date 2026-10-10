nightly-ascii-art-qr

A tiny TypeScript CLI that turns any input text into a blocky ASCII-art pattern reminiscent of a QR code. Perfect for adding a touch of post-apocalyptic flair to your terminal messages.

Installation
-------------
1. Ensure Node.js (>=14) is installed.
2. Install dependencies:
   npm install

Usage
-----
Run with ts-node:
   npx ts-node src/index.ts "Hello World"

Or compile and run:
   npm run build
   node dist/index.js "Hello World"

How it works
------------
Each character is converted to its 8-bit binary representation.
'0' becomes a light shade (░) and '1' becomes a dark block (█).
Rows are printed one per character, forming a grid-like pattern.

License
-------
MIT
