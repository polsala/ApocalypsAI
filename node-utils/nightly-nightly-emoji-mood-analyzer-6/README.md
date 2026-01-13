nightly-emoji-mood-analyzer

A whimsical CLI utility that scans a piece of text and returns a single emoji representing its overall mood. Useful for quickly adding emotional context to messages, commit logs, or notes.

Installation
Clone the repository and run the script with Node.js (no external dependencies).

Usage
node src/index.js "I just finished a marathon!"   => ð¤©
node src/index.js "I'm feeling terrible today."   => ð

If no argument is provided, the tool reads from STDIN.

How it works
The analyzer looks for keywords associated with four moods:
- Happy ð
- Sad ð
- Angry ð 
- Excited ð¤©
If multiple moods match, the first in the priority list is returned. If none match, a neutral ð¤ is returned.

Testing
node tests/test_index.js
