import React, { useState, useEffect, useMemo } from 'react';
import { Bar, Gauge } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const classifiers = [
  'python-utils', 'rust-utils', 'bash-utils', 'react-webpage',
  'github-actions', 'devops-tools', 'docker-tools', 'cli-apps',
  'web-apis', 'js-utils', 'node-utils', 'typescript-utils',
  'data-scripts', 'test-suite-tools', 'monitoring-scripts',
  'infra-automation', 'go-utils', 'java-utils', 'cpp-utils',
  'ansible-playbooks', 'terraform-modules', 'k8s-resources',
  'ci-cd-pipelines', 'database-scripts', 'ml-notebooks', 'api-clients'
];

const weatherTypes = ['Sunny', 'Cloudy', 'Rainy', 'Stormy', 'Foggy', 'Windy'];
const moraleMessages = [
  'Keep calm and code on!',
  'The wasteland needs your brilliance!',
  'Your contributions are stellar!',
  'Stay whimsical and carry on!',
  'You are a beacon of hope!',
  'Your creativity is contagious!'
];
const compliments = [
  'You have the survival instincts of a seasoned wasteland wanderer!',
  'Your code is as clean as a freshly wiped terminal!',
  'You debug with the precision of a temporal surgeon!',
  'Your ideas are as innovative as a post-apocalyptic gadget!',
  'You orchestrate chaos with the grace of a maestro!',
  'Your enthusiasm is as infectious as a meme in the void!'
];

const ApocDashboard = () => {
  const [weather, setWeather] = useState('Sunny');
  const [morale, setMorale] = useState(75);
  const [resources, setResources] = useState({ water: 80, food: 60, ammo: 40, power: 90 });
  const [compliment, setCompliment] = useState(compliments[0]);
  const [nextAnomaly, setNextAnomaly] = useState('');

  // Utility distribution data (mock)
  const utilityData = useMemo(() => {
    const counts = classifiers.map(() => Math.floor(Math.random() * 50) + 5);
    return counts;
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate weather changes
      const newWeather = weatherTypes[Math.floor(Math.random() * weatherTypes.length)];
      setWeather(newWeather);

      // Simulate morale changes
      setMorale((prev) => {
        const change = Math.floor(Math.random() * 20) - 10;
        return Math.max(0, Math.min(100, prev + change));
      });

      // Simulate resource changes
      setResources((prev) => ({
        water: Math.max(0, Math.min(100, prev.water + Math.floor(Math.random() * 10) - 5)),
        food: Math.max(0, Math.min(100, prev.food + Math.floor(Math.random() * 10) - 5)),
        ammo: Math.max(0, Math.min(100, prev.ammo + Math.floor(Math.random() * 10) - 5)),
        power: Math.max(0, Math.min(100, prev.power + Math.floor(Math.random() * 10) - 5)),
      }));

      // Random compliment
      setCompliment(compliments[Math.floor(Math.random() * compliments.length)]);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const updateAnomaly = () => {
      const now = new Date();
      const nextHour = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours() + 1, 0, 0, 0);
      const diff = nextHour - now;
      const minutes = Math.floor(diff / 60000);
      const seconds = Math.floor((diff % 60000) / 1000);
      setNextAnomaly(`${minutes}:${seconds < 10 ? '0' : ''}${seconds}`);
    };
    updateAnomaly();
    const interval = setInterval(updateAnomaly, 1000);
    return () => clearInterval(interval);
  }, []);

  const barData = {
    labels: classifiers,
    datasets: [
      {
        label: 'Utilities Count',
        data: utilityData,
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };

  const barOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Utility Distribution by Classifier' },
    },
    scales: {
      y: { beginAtZero: true },
    },
  };

  const moraleData = {
    labels: ['Morale'],
    datasets: [
      {
        data: [morale, 100 - morale],
        backgroundColor: ['rgba(75, 192, 192, 0.8)', 'rgba(200, 200, 200, 0.3)'],
        borderWidth: 0,
      },
    ],
  };

  const moraleOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: { display: true, text: `Morale Meter: ${morale}%` },
    },
    circumference: 180,
    rotation: 270,
  };

  const weatherIcon = (type) => {
    switch (type) {
      case 'Sunny': return '☀️';
      case 'Cloudy': return '☁️';
      case 'Rainy': return '🌧️';
      case 'Stormy': return '⛈️';
      case 'Foggy': return '🌫️';
      case 'Windy': return '🌬️';
      default: return '🌈';
    }
  };

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '20px', background: '#0f172a', color: '#e2e8f0' }}>
      <h1 style={{ textAlign: 'center', color: '#93c5fd' }}>ApocalypsAI Nightly Dashboard</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
        <div style={{ background: '#111827', padding: '15px', borderRadius: '8px' }}>
          <h2 style={{ color: '#fca5a5' }}>Wasteland Weather</h2>
          <div style={{ fontSize: '3em', textAlign: 'center' }}>{weatherIcon(weather)}</div>
          <p style={{ textAlign: 'center', fontSize: '1.2em' }}>{weather}</p>
        </div>
        <div style={{ background: '#111827', padding: '15px', borderRadius: '8px' }}>
          <h2 style={{ color: '#fca5a5' }}>Morale Meter</h2>
          <Gauge data={moraleData} options={moraleOptions} />
          <p style={{ textAlign: 'center', color: '#a78bfa' }}>{moraleMessages[Math.floor(morale / 20)]}</p>
        </div>
        <div style={{ background: '#111827', padding: '15px', borderRadius: '8px' }}>
          <h2 style={{ color: '#fca5a5' }}>Temporal Rift Countdown</h2>
          <p style={{ fontSize: '2em', textAlign: 'center', color: '#22d3ee' }}>{nextAnomaly}</p>
          <p style={{ textAlign: 'center', color: '#94a3b8' }}>Until next anomaly</p>
        </div>
        <div style={{ background: '#111827', padding: '15px', borderRadius: '8px' }}>
          <h2 style={{ color: '#fca5a5' }}>Survival Resources</h2>
          {Object.entries(resources).map(([name, value]) => (
            <div key={name} style={{ marginBottom: '10px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ textTransform: 'capitalize' }}>{name}</span>
                <span>{value}%</span>
              </div>
              <div style={{ background: '#334155', height: '10px', borderRadius: '5px', overflow: 'hidden' }}>
                <div style={{ background: '#34d399', height: '100%', width: `${value}%`, transition: 'width 0.5s ease' }} />
              </div>
            </div>
          ))}
        </div>
        <div style={{ background: '#111827', padding: '15px', borderRadius: '8px' }}>
          <h2 style={{ color: '#fca5a5' }}>Compliment Corner</h2>
          <p style={{ fontStyle: 'italic', color: '#fde68a' }}>{compliment}</p>
        </div>
        <div style={{ background: '#111827', padding: '15px', borderRadius: '8px' }}>
          <h2 style={{ color: '#fca5a5' }}>Utility Distribution</h2>
          <Bar data={barData} options={barOptions} />
        </div>
      </div>
    </div>
  );
};

export default ApocDashboard;
