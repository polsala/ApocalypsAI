function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
}

const conditions = [
  "Acid rain",
  "Radioactive dust storm",
  "Scorching sun",
  "Glowing fog",
  "Electromagnetic turbulence",
  "Silent snowfall of ash"
];

function getForecast(location) {
  const h = hashString(location);
  const condition = conditions[h % conditions.length];
  const temperature = (h % 80) - 30;
  return `${condition} with a temperature of ${temperature}Â°C`;
}

function App() {
  const [location, setLocation] = React.useState('Radiated Ruins');
  const [forecast, setForecast] = React.useState('');
  const locations = [
    'Radiated Ruins',
    'Dusty Wasteland',
    'Frozen Bunker',
    'Neon Oasis',
    'Cinder City'
  ];
  const generate = () => {
    setForecast(getForecast(location));
  };
  return React.createElement('div', {style: {fontFamily: 'sans-serif', padding: '20px'}},
    React.createElement('h1', null, 'Apocalypse Weather Dashboard'),
    React.createElement('select', {
      value: location,
      onChange: e => setLocation(e.target.value)
    },
      locations.map(loc => React.createElement('option', {key: loc, value: loc}, loc))
    ),
    React.createElement('button', {onClick: generate, style: {marginLeft: '10px'}}, 'Generate'),
    forecast && React.createElement('p', {style: {marginTop: '20px'}}, forecast)
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
