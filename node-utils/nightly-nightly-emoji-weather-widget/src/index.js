// Nightly Emoji Weather Widget
// Cross-platform CLI weather display with animated emojis

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const fetch = require('node-fetch');

// Configuration defaults
const DEFAULT_CONFIG = {
  api_key: null,
  default_city: 'Auto-Detect',
  theme: 'default',
  units: 'metric'
};

// Emoji weather icons
const WEATHER_ICONS = {
  'clear': '☀️',
  'clear_night': '🌙',
  'clouds': '☁️',
  'few_clouds': '🌤️',
  'scattered_clouds': '⛅',
  'broken_clouds': '🌥️',
  'shower_rain': '🌦️',
  'rain': '🌧️',
  'thunderstorm': '⛈️',
  'snow': '❄️',
  'mist': '🌫️',
  'fog': '🌫️',
  'tornado': '🌪️',
  'hail': ' hail',
  'wind': '💨'
};

// ASCII art templates
const ASCII_ARTS = {
  'sunrise': `
   🌅 SUNRISE ⏰
      ☀️
      /|\\
     / | \\
    /  |  \\
   /___|___\\
`,
  'sunset': `
   🌇 SUNSET ⏰
      ☀️
      \/|\\
     \/ | \\
    \/  |  \\
   \/___|___\\
`,
  'rain': `
   🌧️  SHOWERS 💦
      _ _ _
     /'     '\\n    |         |
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
`,
  'snow': `
   ❄️  SNOWFLAKES ❄️
      *   *
     * * * *
    *       *
     * * * *
      *   *
`,
  'cloud': `
   ☁️  CLOUDS ☁️
     __
   _|  |_\n  (     )
  \_____/\n`
};

// Color themes
const THEMES = {
  'default': {
    header: '\u001b[36m', // Cyan
    temp: '\u001b[31m',   // Red
    description: '\u001b[32m', // Green
    reset: '\u001b[0m'
  },
  'retro': {
    header: '\u001b[33m', // Yellow
    temp: '\u001b[35m',   // Magenta
    description: '\u001b[34m', // Blue
    reset: '\u001b[0m'
  },
  'apocalypse': {
    header: '\u001b[41m\u001b[37m', // Red background
    temp: '\u001b[33m',            // Yellow
    description: '\u001b[31m',      // Red
    reset: '\u001b[0m'
  }
};

// Utility functions
function getConfig() {
  try {
    const configPath = path.join(process.env.HOME, '.emoji-weather', 'config.json');
    if (fs.existsSync(configPath)) {
      return JSON.parse(fs.readFileSync(configPath, 'utf8'));
    }
  } catch (error) {
    console.error('Error reading config:', error.message);
  }
  return DEFAULT_CONFIG;
}

function saveConfig(config) {
  try {
    const configDir = path.join(process.env.HOME, '.emoji-weather');
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
    }
    fs.writeFileSync(path.join(configDir, 'config.json'), JSON.stringify(config, null, 2));
  } catch (error) {
    console.error('Error saving config:', error.message);
  }
}

function getCurrentLocation() {
  try {
    const geo = JSON.parse(execSync('curl -s https://ipapi.co/json/').toString());
    return `${geo.city}, ${geo.region}`;
  } catch (error) {
    return 'Denver, CO'; // Fallback
  }
}

async function getWeatherData(city, apiKey, units = 'metric') {
  const config = getConfig();
  const finalApiKey = apiKey || config.api_key;
  const finalCity = city || config.default_city || getCurrentLocation();

  if (!finalApiKey) {
    console.error('Error: No API key found. Please set your OpenWeatherMap API key in config.json');
    process.exit(1);
  }

  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(finalCity)}&units=${units}&appid=${finalApiKey}`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Weather API Error:', error.message);
    return null;
  }
}

function getEmojiForWeather(weather) {
  const lower = weather.toLowerCase();
  if (lower.includes('clear')) return lower.includes('night') ? 'clear_night' : 'clear';
  if (lower.includes('cloud')) {
    if (lower.includes('few')) return 'few_clouds';
    if (lower.includes('scattered')) return 'scattered_clouds';
    if (lower.includes('broken')) return 'broken_clouds';
    return 'clouds';
  }
  if (lower.includes('rain')) return 'rain';
  if (lower.includes('shower')) return 'shower_rain';
  if (lower.includes('thunderstorm')) return 'thunderstorm';
  if (lower.includes('snow')) return 'snow';
  if (lower.includes('mist') || lower.includes('fog')) return 'mist';
  if (lower.includes('tornado')) return 'tornado';
  if (lower.includes('hail')) return 'hail';
  return 'wind';
}

function getAsciiArt(weather) {
  const icon = getEmojiForWeather(weather);
  switch (icon) {
    case 'sunrise':
    case 'sunset':
      return ASCII_ARTS[icon];
    case 'rain':
    case 'snow':
      return ASCII_ARTS[icon];
    default:
      return ASCII_ARTS['cloud'];
  }
}

function formatTemperature(temp, units) {
  if (units === 'imperial') {
    return `${Math.round(temp)}°F`;
  }
  return `${Math.round(temp)}°C`;
}

function displayWeather(data, theme) {
  if (!data) {
    console.log('\n❌ Unable to fetch weather data\n');
    return;
  }

  const weather = data.weather[0];
  const main = weather.main;
  const description = weather.description;
  const temp = data.main.temp;
  const tempMin = data.main.temp_min;
  const tempMax = data.main.temp_max;
  const city = data.name;

  const emoji = WEATHER_ICONS[getEmojiForWeather(main)] || '❓';
  const ascii = getAsciiArt(main);
  const colors = THEMES[theme] || THEMES['default'];

  // Display with animation
  console.clear();
  console.log('\n');
  console.log(colors.header + `\u{1F30D} ${emoji} ${city.toUpperCase()} \u{1F30D}` + colors.reset);
  console.log(colors.description + `  ${description.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}` + colors.reset);
  console.log('\n');
  console.log(ascii);
  console.log('\n');
  console.log(colors.temp + `🌡️  Current: ${formatTemperature(temp, data.sys.country === 'US' ? 'imperial' : 'metric')}` + colors.reset);
  if (tempMin !== tempMax) {
    console.log(colors.temp + `📈  High: ${formatTemperature(tempMax, data.sys.country === 'US' ? 'imperial' : 'metric')}` + colors.reset);
    console.log(colors.temp + `📉  Low: ${formatTemperature(tempMin, data.sys.country === 'imperial' : 'metric')}` + colors.reset);
  }
  console.log('\n');
}

function showSetupInstructions() {
  console.log('\n📝 Setup Instructions:\n');
  console.log('1. Sign up at https://openweathermap.org/api');
  console.log('2. Get your API key');
  console.log('3. Run: emoji-weather --setup\n');
}

// CLI parsing
function parseArgs() {
  const args = process.argv.slice(2);
  const config = getConfig();

  let city = null;
  let apiKey = null;
  let theme = config.theme;
  let forecast = false;

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--city':
        city = args[i + 1];
        i++;
        break;
      case '--api-key':
        apiKey = args[i + 1];
        i++;
        break;
      case '--theme':
        theme = args[i + 1];
        i++;
        break;
      case '--forecast':
        forecast = true;
        break;
      case '--setup':
        console.log('\n🔧 Setting up emoji-weather...\n');
        const newApiKey = apiKey || prompt('Enter your OpenWeatherMap API key: ');
        const newCity = city || prompt('Default city (leave blank for auto-detect): ') || 'Auto-Detect';
        const newTheme = theme || prompt('Theme (default/retro/apocalypse): ') || 'default';
        
        saveConfig({
          ...config,
          api_key: newApiKey,
          default_city: newCity,
          theme: newTheme
        });
        
        console.log('\n✅ Configuration saved!\n');
        return;
    }
  }

  return { city, apiKey, theme, forecast };
}

// Simple prompt function for setup
function prompt(question) {
  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise(resolve => {
    readline.question(question, ans => {
      readline.close();
      resolve(ans);
    });
  });
}

// Main function
async function main() {
  const { city, apiKey, theme, forecast } = parseArgs();

  if (forecast) {
    console.log('\n📅 7-Day Forecast coming soon!\n');
    return;
  }

  const data = await getWeatherData(city, apiKey);
  
  if (!data) {
    // Offline fallback with whimsical apocalypse weather
    const apocalypseWeather = {
      city: 'Apocalypse Zone',
      weather: [{ main: 'tornado', description: 'apocalyptic winds' }],
      main: { temp: 100, temp_min: 80, temp_max: 120 },
      sys: { country: 'US' }
    };
    displayWeather(apocalypseWeather, 'apocalypse');
    return;
  }

  displayWeather(data, theme);
}

// Handle uncaught errors
process.on('uncaughtException', (error) => {
  console.error('\n💥 Uncaught Exception:', error.message);
  console.log('\n💡 Try running with --setup to configure your API key\n');
  process.exit(1);
});

// Run if called directly
if (require.main === module) {
  main().catch(error => {
    console.error('\n💥 Error:', error.message);
    console.log('\n💡 Try running with --setup to configure your API key\n');
    process.exit(1);
  });
}

module.exports = {
  getCurrentLocation,
  getWeatherData,
  displayWeather,
  WEATHER_ICONS,
  ASCII_ARTS
};
