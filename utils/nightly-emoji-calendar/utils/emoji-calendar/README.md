# Emoji Calendar

**emoji-calendar** is a tiny, self‑contained Python utility that prints a month calendar with a cute emoji for each weekday.

## Why?
- Quickly glance at a month and see the vibe of each day (e.g., 🎉 for Fridays).
- No external services – works completely offline.
- Perfect for terminal lovers who enjoy a dash of whimsy.

## Installation
```bash
# From the repository root
cd utils/emoji-calendar
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (no extra deps, file may be empty)
```

## Usage
```bash
python -m src.calendar <month> <year>
```
Example:
```bash
python -m src.calendar 3 2023
```
Will output something like:
```
      March 2023      
Mo Tu We Th Fr Sa Su
               1🌱 2🌱 3🌱 4🌱 5☕
 6🌞 7🚀 8🌱 9📚10🎉11🛌12☕
13🌞14🚀15🌱16📚17🎉18🛌19☕
20🌞21🚀22🌱23📚24🎉25🛌26☕
27🌞28🚀29🌱30📚31🎉   
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
All tests are deterministic and offline.
