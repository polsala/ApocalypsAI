# nightly‑hash‑art‑cli

**What it does**

`nightly‑hash‑art‑cli` is a tiny TypeScript command‑line utility that takes an input string, computes its SHA‑256 hash, and renders the hash as whimsical ASCII art. Each hexadecimal digit is mapped to a unique Unicode block character, producing a compact, deterministic visual fingerprint.

**Why it’s useful**

* Quickly generate a visual identifier for passwords, tokens, or any piece of text without exposing the raw hash.
* Fun way to embed a “signature” in logs, README files, or terminal output.
* Fully deterministic – the same input always yields the same art, making it suitable for simple integrity checks.

**Installation**

```bash
# Clone the repository (or copy the utility folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-hash-art-cli

# Install dependencies (Node.js 18+ required)
npm install
```

**Build & Run**

```bash
# Compile TypeScript (optional – ts-node can run directly)
npm run build

# Run the CLI
node dist/main.js "your string here"
```

Or, using `ts-node` without a build step:

```bash
npx ts-node src/main.ts "your string here"
```

**Example**

```bash
$ npx ts-node src/main.ts test
▎■▏▇▊▁▏▂▏▏▅▋█▊▇▆▎▍▃■▉▍▍▁▋▆▆▍▊▁▂▆▍▄▌■▅■▂▌▃▌▁▌▏▃▃▋▊▂▆▊▇▋▂▆▌▁■▁▁▍▁▏
```

**API**

The core function is exported for programmatic use:

```ts
import { hashToArt } from "./main";

const art = hashToArt("some secret");
console.log(art);
```

**Testing**

Run the bundled tests with:

```bash
npm test
```

---

*Feel free to adapt the character map or extend the utility to support other hash algorithms!*
