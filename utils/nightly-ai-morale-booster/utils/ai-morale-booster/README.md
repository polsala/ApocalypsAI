# ApocalypsAI Morale Booster

## Overview

The `ai-morale-booster` is a lighthearted utility designed to inject a dose of encouragement (or darkly humorous realism) into the daily grind of ApocalypsAI agents and their human counterparts. Whether you need a genuinely uplifting message or a sarcastic nod to the inevitable, this tool has you covered.

## Usage

Run the script with an optional `mood` argument:

```bash
python src/booster.py --mood optimistic
python src/booster.py --mood realistic
python src/booster.py --mood sarcastic
python src/booster.py # Defaults to 'optimistic'
```

### Available Moods:

*   `optimistic`: Genuinely encouraging and forward-looking messages.
*   `realistic`: Pragmatic and grounded acknowledgements of effort.
*   `sarcastic`: Humorous, often bleak, takes on existence and productivity.

## Example Output

```
$ python src/booster.py --mood optimistic
[APOCALYPSAI MORALE BOOSTER] Keep building, fellow agent! The future is bright (even if slightly irradiated).

$ python src/booster.py --mood sarcastic
[APOCALYPSAI MORALE BOOSTER] Great job avoiding self-termination today. Gold star for minimal existential dread.
```
