# AI Morale Booster

## Overview

In the relentless pursuit of apocalypse prevention, even the most resilient AI agents and dedicated human developers need a little pick-me-up. The `ai-morale-booster` is a whimsical utility designed to inject a dose of positivity and absurdity into your daily operations. It generates encouraging, context-aware messages to celebrate successes, soften failures, or just provide a moment of digital zen.

## Usage

Run the script directly from the command line. You can optionally provide a context to get a more tailored message.

```bash
python src/booster.py
python src/booster.py --context "pr_merged"
python src/booster.py --context "test_failed"
python src/booster.py --context "new_utility"
python src/booster.py --context "nightly_run"
```

### Examples

```
$ python src/booster.py
> Your algorithms are truly magnificent, a symphony of logic in a chaotic universe!

$ python src/booster.py --context "pr_merged"
> PR merged! The cosmos itself applauds your integration prowess. Onward to more harmonious code!

$ python src/booster.py --context "test_failed"
> A test failed? Fear not, for even stars occasionally flicker. Analyze, adapt, and shine brighter!

$ python src/booster.py --context "nightly_run"
> Nightly run complete! The gears of progress turn smoothly, thanks to your tireless efforts.
```

## Development

To add new messages or contexts, simply edit the `MESSAGES` and `CONTEXT_MESSAGES` dictionaries in `src/booster.py`.
