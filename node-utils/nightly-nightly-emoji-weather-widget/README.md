# Nightly Emoji Weather Widget

A fun, cross-platform CLI weather widget that displays current conditions and forecasts using animated emojis, ASCII art, and playful descriptions. Perfect for adding personality to your terminal workflow!

## Features
- Real-time weather data from OpenWeatherMap API
- Emoji-based weather icons (☀️🌧️❄️💨)
- Animated sunrise/sunset sequences
- Customizable color themes
- Support for multiple locations
- Offline fallback with whimsical "apocalypse" weather

## Installation
```bash
npm install -g nightly-emoji-weather-widget
```

## Usage
```bash
# Show current weather for your location
emoji-weather

# Show forecast for a specific city
emoji-weather --city="New York"

# Show 7-day forecast
emoji-weather --forecast

# Custom theme
emoji-weather --theme="retro"
```

## Configuration
Create `~/.emoji-weather/config.json`:
```json
{
  "api_key": "YOUR_OPENWEATHERMAP_API_KEY",
  "default_city": "Denver, CO",
  "theme": "default",
  "units": "metric"
}
```

## API Key Setup
1. Sign up at https://openweathermap.org/api
2. Add your API key to the config file
3. Run `emoji-weather` to test

## Examples
### Clear Sky
```
🌤️  SUNRISE ⏰
      ☀️
      /|\
     / | \
    /  |  \
   /___|___\

Denver, CO - Sunny
High: 78°F | Low: 55°F
"
### Rain
```
🌧️  SHOWERS 💦
     _ _ _
    /'     '\
   |         |
   |         |
   |         |
   |         |
   |         |
   |         |
   |         |
   |         |
   |         |
   |         |
   |         |
   |         |
   \         /
    \______/
"

## Development
```bash
npm install
npm test
```

## License
MIT
