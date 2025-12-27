/**
 * @file ChronoWeave.js
 * @description Core visualization component for chrono-threads and anomalies.
 */

import React, { useRef, useEffect, useState, useCallback } from 'react';
import ChronoThread from './ChronoThread';
import { shouldTriggerAnomaly, getAnomalyDuration } from './AnomalyDetector';

const NUM_THREADS = 10;
const THREAD_LENGTH = 100; // Number of points per thread
const THREAD_SPACING = 30; // Vertical spacing between threads

const ChronoWeave = ({ isRunning, speed, anomalyFrequency }) => {
  const svgRef = useRef(null);
  const animationFrameId = useRef();
  const lastUpdateTime = useRef(0);
  const [threads, setThreads] = useState([]);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  const initializeThreads = useCallback((width, height) => {
    const newThreads = Array.from({ length: NUM_THREADS }).map((_, i) => ({
      id: i,
      points: Array.from({ length: THREAD_LENGTH }).map((_, j) => ({
        x: width - (j * (width / THREAD_LENGTH)), // Start from right, move left
        y: (i * THREAD_SPACING) + (THREAD_SPACING / 2) + (height - (NUM_THREADS * THREAD_SPACING)) / 2
      })),
      isAnomalous: false,
      anomalyEndTime: 0,
      baseY: (i * THREAD_SPACING) + (THREAD_SPACING / 2) + (height - (NUM_THREADS * THREAD_SPACING)) / 2,
      amplitude: Math.random() * 5 + 2 // For subtle wave effect
    }));
    setThreads(newThreads);
  }, []);

  // Update dimensions on resize
  useEffect(() => {
    const updateDimensions = () => {
      if (svgRef.current) {
        setDimensions({
          width: svgRef.current.clientWidth,
          height: svgRef.current.clientHeight,
        });
      }
    };
    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  // Re-initialize threads when dimensions change
  useEffect(() => {
    if (dimensions.width > 0 && dimensions.height > 0) {
      initializeThreads(dimensions.width, dimensions.height);
    }
  }, [dimensions, initializeThreads]);

  const animate = useCallback((timestamp) => {
    if (!isRunning) {
      animationFrameId.current = requestAnimationFrame(animate);
      return;
    }

    const deltaTime = timestamp - lastUpdateTime.current;
    // Adjust update interval based on speed. Lower speed means larger interval.
    const updateInterval = Math.max(10, 100 - (speed * 0.9)); // 10ms to 100ms

    if (deltaTime > updateInterval) {
      setThreads(prevThreads => prevThreads.map(thread => {
        const now = Date.now();
        let newIsAnomalous = thread.isAnomalous;
        let newAnomalyEndTime = thread.anomalyEndTime;

        // Check if anomaly should end
        if (newIsAnomalous && now > newAnomalyEndTime) {
          newIsAnomalous = false;
          newAnomalyEndTime = 0;
        }

        // Check if new anomaly should start
        if (!newIsAnomalous && shouldTriggerAnomaly(anomalyFrequency)) {
          newIsAnomalous = true;
          newAnomalyEndTime = now + getAnomalyDuration();
        }

        const newPoints = thread.points.slice(1); // Remove oldest point
        const lastPoint = newPoints[newPoints.length - 1];

        // Calculate new point's Y based on a subtle wave and anomaly status
        let newY = thread.baseY + Math.sin(timestamp * 0.005 + thread.id) * thread.amplitude;
        if (newIsAnomalous) {
          newY += Math.sin(timestamp * 0.02 + thread.id) * 10; // More pronounced wiggle
        }

        newPoints.push({
          x: dimensions.width,
          y: newY
        });

        // Shift all points left
        const shiftedPoints = newPoints.map(p => ({
          x: p.x - (dimensions.width / THREAD_LENGTH) * (deltaTime / updateInterval), // Move left proportionally
          y: p.y
        }));

        return {
          ...thread,
          points: shiftedPoints,
          isAnomalous: newIsAnomalous,
          anomalyEndTime: newAnomalyEndTime,
        };
      }));
      lastUpdateTime.current = timestamp;
    }

    animationFrameId.current = requestAnimationFrame(animate);
  }, [isRunning, speed, anomalyFrequency, dimensions.width, dimensions.height]);

  useEffect(() => {
    if (dimensions.width > 0 && dimensions.height > 0) {
      lastUpdateTime.current = performance.now();
      animationFrameId.current = requestAnimationFrame(animate);
    }

    return () => {
      if (animationFrameId.current) {
        cancelAnimationFrame(animationFrameId.current);
      }
    };
  }, [animate, dimensions]);

  return (
    <div ref={svgRef} className="chrono-weave-container">
      <svg>
        {threads.map(thread => (
          <ChronoThread
            key={thread.id}
            id={thread.id}
            points={thread.points}
            isAnomalous={thread.isAnomalous}
          />
        ))}
      </svg>
    </div>
  );
};

export default ChronoWeave;
