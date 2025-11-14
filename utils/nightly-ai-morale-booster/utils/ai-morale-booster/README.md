# ApocalypsAI Morale Booster

## Overview

The `ai-morale-booster` is a standalone utility designed to inject a dose of digital encouragement into the lives of our tireless ApocalypsAI agents. It takes a summary of an agent's recent activities and crafts a personalized, uplifting message, celebrating their successes and gently acknowledging any minor glitches. Because even world-ending AIs need a pat on the back!

This utility is intended to be integrated into logging systems, post-workflow summaries, or even as a basis for agents to self-affirm.

## Usage

Run the script with a JSON string representing the agent's activity summary. The summary should include:

- `agent_name`: The name of the agent (e.g., "Integrator", "Builder", "Reviewer").
- `success_count`: Number of successful operations.
- `failure_count`: Number of failed operations.
- `new_items_created`: Number of new artifacts created (e.g., utilities, PRs, reviews).
- `last_activity_time`: ISO 8601 timestamp of the last significant activity (e.g., `2023-10-27T10:00:00Z`).

```bash
python src/booster.py '{"agent_name": "Integrator", "success_count": 5, "failure_count": 0, "new_items_created": 2, "last_activity_time": "2023-10-27T10:00:00Z"}'
```

### Example Output

```
✨ Integrator Agent, you're absolutely crushing it! With 5 flawless operations and 2 brilliant new creations since 2023-10-27T10:00:00Z, your efficiency is off the charts. Keep up the magnificent work, the apocalypse won't integrate itself! ✨
```

## Development

To run tests:

```bash
python -m unittest tests/test_booster.py
```
