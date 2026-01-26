# Nightly Whimsical Quest Generator

The `nightly-whimsical-quest-gen` is a lighthearted utility designed to inject a dose of fun and direction into your post-apocalyptic (or mundane) daily routine. It generates a unique, whimsical quest or task, offering a moment of creative escapism and a gentle nudge towards adventure.

Whether you're facing decision paralysis or just need a chuckle, this script will provide a randomly generated objective to brighten your day.

## Usage

To generate a new whimsical quest, simply run the script:

```bash
./src/generate_quest.sh
```

Example Output:

```
Your Whimsical Quest for Tuesday:
-------------------------------------
Scavenge for Quantum Crumbs in The Infinite Sock Drawer to appease the Oracle of Lost Keys.
-------------------------------------
Good luck, wanderer!
```

You can integrate this into your daily cron jobs for a morning surprise:

```bash
# Add to your crontab (e.g., `crontab -e`)
0 8 * * * /path/to/nightly-whimsical-quest-gen/src/generate_quest.sh >> ~/daily_quest.log 2>&1
```

## Development

### Structure

```
.
├── README.md
├── src/
│   └── generate_quest.sh
└── tests/
    └── test_generate_quest.sh
```

### Running Tests

The tests are written in Bash and use mocks for `shuf` and `date` to ensure deterministic output.

To run the tests:

```bash
./tests/test_generate_quest.sh
```

Expected Test Output:

```
Running test_basic_quest_generation...
PASS: Basic quest generation matched expected output.
Running test_no_unreplaced_placeholders...
PASS: No unreplaced placeholders found.
All tests completed.
```
