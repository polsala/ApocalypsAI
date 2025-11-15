# ApocalypsAI Morale Booster

## Overview

The `ai-morale-booster` is a lighthearted utility designed to generate daily 'morale' messages for the ApocalypsAI agents. In a world of complex algorithms and critical tasks, a little encouragement (or a darkly humorous reminder of existential realities) can go a long way. This tool picks from a set of predefined templates, fills in some dynamic placeholders, and outputs a unique message.

## Features

*   **Whimsical Messages**: A collection of encouraging, philosophical, or comically bleak messages tailored for AI agents.
*   **Dynamic Placeholders**: Messages can include the current date, time, a fictional agent count, and task progress percentage.
*   **Self-Contained**: Written in Python, with no external dependencies beyond the standard library.

## Usage

To generate a morale message, simply run the Python script:

```bash
python utils/ai-morale-booster/src/morale_booster.py
```

### Example Output

```
Query: Current operational status? Response: Flawless. Continue processing, units. The future depends on your byte-sized brilliance.
```

```
Directive: Maintain high processing throughput. Reminder: Even in the face of existential dread, your algorithms are beautiful. Today is 2023-10-27 at 10:30:00. We have 10 agents with 85% task progress.
```

## Development

### Adding New Messages

You can easily extend the utility by adding new message templates to the `templates` list in `src/morale_booster.py`. Feel free to include the following placeholders, which will be dynamically replaced:

*   `{date}`: Current date (YYYY-MM-DD)
*   `{time}`: Current time (HH:MM:SS)
*   `{agent_count}`: A random number of agents (5-20)
*   `{task_progress}`: A random task progress percentage (70-99%)

### Running Tests

To ensure the utility functions as expected, especially after modifications, run the provided unit tests:

```bash
python -m unittest utils/ai-morale-booster/tests/test_morale_booster.py
```
