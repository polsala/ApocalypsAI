# nightly-survival-bingo

A whimsical yet useful React web page that generates a 5x5 Survival Bingo board.  Each cell can be toggled to mark a task you’ve completed while surviving the apocalypse.

## Features
- Randomly generated board (deterministic for tests)
- Click‑to‑toggle cells
- Simple, self‑contained – no build step required

## Quick Start
1. **Clone the repo**
   ```bash
   git clone https://github.com/polsala/ApocalypsAI.git
   cd ApocalypsAI/utils/nightly-survival-bingo
   ```
2. **Open the page**
   ```bash
   # You can serve it with any static server, e.g. Python
   python -m http.server 8000
   ```
   Then navigate to `http://localhost:8000`.

## Running Tests
The tests are pure Node.js scripts and require no external dependencies.
```bash
node tests/test_generateBoard.js
```

## License
MIT
