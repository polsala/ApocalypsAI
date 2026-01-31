# nightly-chaos-monkey-scheduler

A Node.js CLI utility that injects playful chaos into your system by scheduling random disruptions. Perfect for testing resilience in development or staging environments.

## Features
- Schedule random service restarts, network delays, or resource hogs
- Whimsical chaos types: `banana-peel`, `sneaky-cat`, `power-outage`
- Dry-run mode for previewing chaos

## Usage

```bash
npx nightly-chaos-monkey-scheduler --chaos banana-peel --interval 30s --dry-run
```

## Options

- `--chaos <type>`: Type of chaos to inject
- `--interval <time>`: How often to trigger chaos (e.g. 10s, 1m)
- `--dry-run`: Preview without executing

## Examples

```bash
npx nightly-chaos-monkey-scheduler --chaos sneaky-cat --interval 1m
```
