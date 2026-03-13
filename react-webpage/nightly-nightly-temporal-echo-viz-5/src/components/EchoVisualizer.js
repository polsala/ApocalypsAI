import React, { useRef, useEffect, useState } from 'react';
import { format, min, max, addDays } from 'date-fns';

const EchoVisualizer = ({ events, echoes }) => {
  const svgRef = useRef();
  const [width, setWidth] = useState(0);
  const height = 150;
  const margin = { top: 20, right: 20, bottom: 30, left: 50 };

  // # Mock rationale: This component relies on DOM measurements for responsive width.
  // In a real test environment, we would mock the ref.current.clientWidth or use a testing library
  // that provides a virtual DOM with dimensions. For this self-contained utility, we assume
  // the browser environment provides correct dimensions.
  useEffect(() => {
    const updateWidth = () => {
      if (svgRef.current) {
        setWidth(svgRef.current.clientWidth - margin.left - margin.right);
      }
    };
    updateWidth();
    window.addEventListener('resize', updateWidth);
    return () => window.removeEventListener('resize', updateWidth);
  }, [margin.left, margin.right]);

  if (!events || events.length === 0 || width <= 0) {
    return <p style={{ textAlign: 'center' }}>No events to display or container not ready.</p>;
  }

  const allDates = events.map(e => e.date);
  const minDate = min(allDates);
  const maxDate = max(allDates);

  // Add some padding to the timeline
  const paddedMinDate = addDays(minDate, -1);
  const paddedMaxDate = addDays(maxDate, 1);

  // Scale for X-axis (time)
  const xScale = (date) => {
    return margin.left + (date.getTime() - paddedMinDate.getTime()) / (paddedMaxDate.getTime() - paddedMinDate.getTime()) * width;
  };

  // Unique event types for Y-axis positioning
  const eventTypes = [...new Set(events.map(e => e.event))].sort();
  const yScale = (eventType) => {
    return margin.top + (eventTypes.indexOf(eventType) + 0.5) * (height - margin.top - margin.bottom) / eventTypes.length;
  };

  return (
    <div ref={svgRef} style={{ width: '100%', height: `${height}px`, overflowX: 'auto', border: '1px solid #555', borderRadius: '4px' }}>
      <svg width="100%" height={height}>
        {/* X-axis line */}
        <line x1={margin.left} y1={height - margin.bottom} x2={width + margin.left} y2={height - margin.bottom} stroke="#f0f0f0" />
        {/* X-axis ticks and labels */}
        {[paddedMinDate, maxDate].map((date, i) => (
          <g key={i} transform={`translate(${xScale(date)}, ${height - margin.bottom})`}>
            <line y2="5" stroke="#f0f0f0" />
            <text y="15" textAnchor="middle" fill="#f0f0f0" fontSize="10px">
              {format(date, 'MMM dd')}
            </text>
          </g>
        ))}

        {/* Events as circles */}
        {events.map((event, i) => (
          <circle
            key={i}
            cx={xScale(event.date)}
            cy={yScale(event.event)}
            r={5}
            fill="#61dafb"
            stroke="#282c34"
            strokeWidth="1"
          >
            <title>{`${event.event} - ${format(event.date, 'yyyy-MM-dd HH:mm')}`}</title>
          </circle>
        ))}

        {/* Echo lines/highlights */}
        {Object.entries(echoes).map(([eventType, echo]) => {
          const relevantEvents = events.filter(e => e.event === eventType).sort((a, b) => a.date.getTime() - b.date.getTime());
          if (relevantEvents.length < echo.count) return null; // Not enough events to draw the echo

          const echoSegments = [];
          for (let i = 0; i <= relevantEvents.length - echo.count; i++) {
            let isEchoSegment = true;
            for (let j = 0; j < echo.count - 1; j++) {
              if (differenceInDays(relevantEvents[i + j + 1].date, relevantEvents[i + j].date) !== echo.interval) {
                isEchoSegment = false;
                break;
              }
            }
            if (isEchoSegment) {
              echoSegments.push({
                start: relevantEvents[i].date,
                end: relevantEvents[i + echo.count - 1].date,
                y: yScale(eventType)
              });
            }
          }

          return echoSegments.map((segment, idx) => (
            <line
              key={`${eventType}-echo-${idx}`}
              x1={xScale(segment.start)}
              y1={segment.y}
              x2={xScale(segment.end)}
              y2={segment.y}
              stroke="#ffeb3b"
              strokeWidth="2"
              strokeDasharray="4 2"
            >
              <title>{`Echo: ${eventType} every ${echo.interval} days`}</title>
            </line>
          ));
        })}

        {/* Y-axis labels (event types) */}
        {eventTypes.map((type, i) => (
          <text
            key={type}
            x={margin.left - 10}
            y={yScale(type)}
            textAnchor="end"
            alignmentBaseline="middle"
            fill="#f0f0f0"
            fontSize="10px"
          >
            {type}
          </text>
        ))}
      </svg>
    </div>
  );
};

export default EchoVisualizer;
