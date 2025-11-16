# Nightly Solar Noon Finder

## Purpose
In a world where digital navigation might fail, knowing the precise moment of solar noon is a crucial survival skill. This utility calculates when the sun will reach its highest point in the sky for a given location and date, allowing you to reliably determine true North or South.

## How it Works
The `Nightly Solar Noon Finder` uses astronomical formulas to compute the Equation of Time and adjust for your longitude. The result is the exact UTC time of solar noon, which is then converted to your local time based on an optional timezone offset.

At solar noon:
*   In the Northern Hemisphere, the sun is due South. True North is directly behind you.
*   In the Southern Hemisphere, the sun is due North. True South is directly behind you.

## Usage
Run the Python script from your terminal:

```bash
python src/solar_noon.py --date YYYY-MM-DD --lat <latitude> --lon <longitude> [--tz <timezone_offset_hours>]
```

### Arguments:
*   `--date`: The date for which to calculate solar noon, in `YYYY-MM-DD` format.
*   `--lat`: The latitude of your location (e.g., `34.0522` for Los Angeles).
*   `--lon`: The longitude of your location (e.g., `-118.2437` for Los Angeles; West is negative, East is positive).
*   `--tz`: (Optional) Your timezone offset from UTC in hours (e.g., `-7` for PDT, `+2` for CET). Defaults to `0` (UTC).

### Examples:

**1. Los Angeles, USA (PDT, UTC-7) on June 20, 2024:**
```bash
python src/solar_noon.py --date 2024-06-20 --lat 34.0522 --lon -118.2437 --tz -7
```

**2. Sydney, Australia (AEDT, UTC+11) on December 21, 2024:**
```bash
python src/solar_noon.py --date 2024-12-21 --lat -33.8688 --lon 151.2093 --tz 11
```

## Installation
This utility is self-contained and requires Python 3.6+ (tested with 3.11). No external dependencies are needed beyond the standard library.

```bash
cd utils/nightly-solar-noon-finder
python src/solar_noon.py --help
```
