# nightly-bash-uptime-emoji

**Purpose**: A tiny Bash utility that reads the system uptime and prints a friendly message together with an emoji that hints at the time‑of‑day range the system has been up for.

## Features
- Works without any external dependencies.
- Accepts an optional *uptime string* (the output of `uptime -p`).  This makes the script easy to test.
- If no argument is supplied, the script calls `uptime -p` itself.
- Maps the total uptime to one of four emojis:
  - **🌅** – less than 6 hours (sunrise)
  - **☀️** – 6 – 12 hours (mid‑day)
  - **🌇** – 12 – 18 hours (sunset)
  - **🌙** – 18 hours or more (night)

## Installation
```bash
# Clone the repository (or copy the folder) and make the script executable
chmod +x src/main.sh
```

## Usage
```bash
# Let the script query the real system uptime
./src/main.sh

# Or feed a mocked uptime string (useful for testing or demos)
./src/main.sh "up 2 hours, 15 minutes"
```

## Example Output
```
System has been up for 2 hours 15 minutes. 🌅
```

## Testing
Run the bundled test suite:
```bash
cd tests && ./test_main.sh
```
All tests should pass.
