# Wasteland Weather Oracle

## Description

In the desolate future, knowing the weather isn't just about comfort; it's about survival. The Wasteland Weather Oracle is a whimsical-yet-useful command-line utility designed for the discerning survivor. It fetches current weather data for a specified location and translates it into a grim, post-apocalyptic forecast, complete with warnings about radiation storms, acid rain, or opportunistic raiders.

Plan your scavenging runs, decide whether to fortify your shelter, or simply brace for the next environmental hazard with this essential tool.

## Usage

To get a forecast, run the script with either a location name or geographical coordinates:

```bash
python src/weather_oracle.py --location "New York"
# Or with coordinates:
python src/weather_oracle.py --lat 40.7128 --lon -74.0060
```

### Examples

**Example 1: Clear Skies**

```
$ python src/weather_oracle.py --location "Los Angeles"

--- Wasteland Weather Report for Los Angeles ---
Conditions: Scorching sun. Clear skies, but watch for raiders and mutated wildlife.
Wind: A gentle, eerie breeze.
```

**Example 2: Acid Rain Advisory**

```
$ python src/weather_oracle.py --location "London"

--- Wasteland Weather Report for London ---
Conditions: Chilly winds. Heavy acid downpour, seek immediate shelter!
Wind: Gusty winds, secure your scavenged goods.
```

**Example 3: Toxic Fog**

```
$ python src/weather_oracle.py --lat 34.0522 --lon -118.2437

--- Wasteland Weather Report for Los Angeles ---
Conditions: Mild, but don't get complacent. Toxic fog/dust/ash cloud rolling in, don your respirators!
Wind: A gentle, eerie breeze.
```

## Installation

This utility is self-contained and requires Python 3.6+.

1.  Navigate to the `utils/wasteland-weather-oracle/` directory.
2.  Run the script directly as shown in the Usage section.
