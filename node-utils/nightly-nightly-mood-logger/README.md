Nightly Mood Logger
===================

A tiny, whimsical command‑line utility that lets you record how you feel each day and then peek at a simple summary of your emotional landscape.

Features
--------
* Add a mood entry for today (e.g., happy, sad, excited, meh)
* Store entries in a JSON file under your home directory (`~/.moodlog.json`)
* View a count of how many times each mood has been logged
* Zero‑dependency, pure Node.js (requires Node 14+)

Installation
------------
```sh
# Clone the utility (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-mood-logger
# Install (optional, only needed if you want to use it as a global command)
npm install -g .
```

Usage
-----
```sh
# Add a mood entry for today
node src/index.js add "happy"

# View a summary of all logged moods
node src/index.js stats
```

The utility will create (or update) a file at `~/.moodlog.json` that looks like:
```json
{"entries":[{"date":"2026-03-14","mood":"happy"}]}
```

Testing
-------
Run the bundled tests with:
```sh
node tests/test_index.js
```
All tests should pass without external network access.
