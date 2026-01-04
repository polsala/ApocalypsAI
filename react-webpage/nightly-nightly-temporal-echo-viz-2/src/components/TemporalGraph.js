import React from 'react';
import './TemporalGraph.css'; // Styles for the graph

const TemporalGraph = ({ data }) => {
  if (!data || data.length === 0) {
    return <div className="temporal-graph-container">No temporal data available.</div>;
  }

  const width = 800;
  const height = 300;
  const padding = 40;

  const maxDistortion = Math.max(...data.map(d => d.distortion));
  const maxEcho = Math.max(...data.map(d => d.echoIntensity));
  const maxVal = Math.max(maxDistortion, maxEcho, 10); // Ensure min scale

  const xScale = (index) => padding + (index / (data.length - 1)) * (width - 2 * padding);
  const yScale = (value) => height - padding - (value / maxVal) * (height - 2 * padding);

  const distortionPath = data.map((d, i) => `${xScale(i)},${yScale(d.distortion)}`).join(' ');
  const echoPath = data.map((d, i) => `${xScale(i)},${yScale(d.echoIntensity)}`).join(' ');

  // Y-axis labels
  const yAxisLabels = [0, Math.round(maxVal / 2), Math.round(maxVal)];

  return (
    <div className="temporal-graph-container">
      <svg viewBox={`0 0 ${width} ${height}`} className="temporal-svg">
        {/* Grid lines */}
        <g className="grid">
          {yAxisLabels.map((label, i) => (
            <line
              key={`y-grid-${i}`}
              x1={padding}
              y1={yScale(label)}
              x2={width - padding}
              y2={yScale(label)}
              stroke="#4a4a6a"
              strokeDasharray="2,2"
            />
          ))}
          {data.map((_, i) => (
            <line
              key={`x-grid-${i}`}
              x1={xScale(i)}
              y1={padding}
              x2={xScale(i)}
              y2={height - padding}
              stroke="#4a4a6a"
              strokeDasharray="2,2"
            />
          ))}
        </g>

        {/* Y-axis labels */}
        <g className="y-axis-labels">
          {yAxisLabels.map((label, i) => (
            <text
              key={`y-label-${i}`}
              x={padding - 10}
              y={yScale(label) + 5}
              textAnchor="end"
              fill="#a0a0a0"
              fontSize="12"
            >
              {label}
            </text>
          ))}
        </g>

        {/* X-axis labels (time) */}
        <g className="x-axis-labels">
          {data.map((d, i) => (
            <text
              key={`x-label-${i}`}
              x={xScale(i)}
              y={height - padding + 20}
              textAnchor="middle"
              fill="#a0a0a0"
              fontSize="10"
              transform={`rotate(45 ${xScale(i)} ${height - padding + 20})`}
            >
              {d.time}
            </text>
          ))}
        </g>

        {/* Distortion Line */}
        <polyline
          fill="none"
          stroke="#ff0066" /* Critical red */
          strokeWidth="2"
          points={distortionPath}
        />
        {/* Echo Intensity Line */}
        <polyline
          fill="none"
          stroke="#ffcc00" /* Warning amber */
          strokeWidth="2"
          points={echoPath}
        />

        {/* Legend */}
        <g className="legend" transform={`translate(${width - padding - 120}, ${padding + 10})`}>
          <rect x="0" y="0" width="10" height="10" fill="#ff0066" />
          <text x="15" y="9" fill="#e0e0e0" fontSize="12">Distortion</text>
          <rect x="0" y="15" width="10" height="10" fill="#ffcc00" />
          <text x="15" y="24" fill="#e0e0e0" fontSize="12">Echo Intensity</text>
        </g>
      </svg>
    </div>
  );
};

export default TemporalGraph;
