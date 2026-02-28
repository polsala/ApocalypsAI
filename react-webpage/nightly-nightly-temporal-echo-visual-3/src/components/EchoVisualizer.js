import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function EchoVisualizer({ data }) {
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#f0f0f0',
        },
      },
      title: {
        display: true,
        text: 'Keyword Temporal Echoes',
        color: '#61dafb',
        font: {
          size: 18,
        },
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += context.parsed.y;
            }
            return label;
          }
        }
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Text Slice',
          color: '#f0f0f0',
        },
        ticks: {
          color: '#f0f0f0',
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Echo Strength (Frequency)',
          color: '#f0f0f0',
        },
        ticks: {
          color: '#f0f0f0',
          beginAtZero: true,
          precision: 0,
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
    },
  };

  return (
    <div style={{ height: '400px', width: '100%' }}>
      <Line options={options} data={data} />
    </div>
  );
}

export default EchoVisualizer;
