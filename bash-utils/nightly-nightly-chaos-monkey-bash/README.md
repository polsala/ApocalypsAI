# nightly-chaos-monkey-bash

A playful Bash utility that introduces random, harmless chaos into your terminal session. Perfect for testing how robust your scripts are under unexpected conditions.

## Features

- Randomly alters prompt appearance
- Occasionally echoes funny error-like messages
- Changes directory listing colors
- Safe and reversible

## Usage

```bash
source nightly-chaos-monkey-bash.sh
```

Once sourced, the chaos monkey will activate periodically during your session.

To disable:

```bash
chaos_monkey_disable
```

## Example

After sourcing, you might see things like:

- Your prompt turning into a random emoji
- Fake "disk space low" warnings
- Unexpected (but harmless) command output delays

All effects are purely visual or timing-based and never destructive.
