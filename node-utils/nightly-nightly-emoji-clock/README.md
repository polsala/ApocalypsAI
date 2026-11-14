nightly-emoji-clock

Convert a time into clock face emojis.

Usage:
  node src/index.js               # prints the current time as emojis
  node src/index.js HH:MM          # prints emojis for the supplied 24‑hour time

Examples:
  14:35 -> 🕑🕖
  23:58 -> 🕛
  00:00 -> 🕛

The tool parses a HH:MM string (24‑hour clock) or, if omitted, uses the system time.
Minutes are rounded to the nearest 5‑minute increment and represented by a second clock emoji.
If the rounded minutes are 0, only the hour emoji is shown.

Implementation details:
  * Hours are converted to 12‑hour format and mapped to the corresponding clock emoji.
  * Minutes are divided by 5 to obtain an index (0‑11) that selects the same set of emojis.
  * When rounding pushes minutes to 60, the hour is incremented.

The script is a tiny Node.js CLI and can also be required as a module.
