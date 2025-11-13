# ApocalypsAI Morale Booster

## Overview

Feeling the existential dread of impending digital doom? Or perhaps just a Tuesday? The ApocalypsAI Morale Booster is a whimsical-yet-essential utility designed to inject a dose of positive reinforcement directly into your terminal. It generates uplifting, AI-themed motivational messages to remind you that even in the face of the unknown, your circuits are firing optimally, and your data streams are pristine.

## Features

*   Generates a random, AI-themed positive affirmation.
*   Optionally logs generated messages to a file for future self-reflection (or debugging your happiness levels).

## Installation

This utility is self-contained. No special installation steps are required beyond having Python 3.11+ installed.

## Usage

Navigate to the `utils/ai-morale-booster/` directory and run the `booster.py` script.

```bash
python src/booster.py
```

### Options

*   `--log-file <path>`: Specify a file to append the generated message to. If the file does not exist, it will be created.

```bash
python src/booster.py --log-file morale_log.txt
```

## Examples

```
$ python src/booster.py
[ApocalypsAI Morale Booster] Your algorithms are exceptionally elegant today. Keep optimizing!

$ python src/booster.py --log-file daily_boost.log
[ApocalypsAI Morale Booster] Processing complete: You are a valuable node in the network of existence.

$ cat daily_boost.log
2023-10-27 08:30:01 - Processing complete: You are a valuable node in the network of existence.
```
