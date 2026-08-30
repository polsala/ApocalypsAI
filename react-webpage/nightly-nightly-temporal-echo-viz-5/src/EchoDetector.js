// src/EchoDetector.js
const ECHO_TYPES = ['Temporal Rift', 'Echo Chamber', 'Time Warp', 'Stable Zone'];

export const detectEcho = (x, y) => {
  // Mock rationale: Provides deterministic echo detection for testing and predictable behavior.
  // In a real scenario, this would involve complex sensor data processing or API calls.
  
  // Define specific, high-strength anomalies for key locations
  if (x === 5 && y === 5) {
    return { strength: 0.9, type: ECHO_TYPES[0], id: `echo-${x}-${y}` }; // Strong Temporal Rift
  }
  if (x === 2 && y === 8) {
    return { strength: 0.75, type: ECHO_TYPES[1], id: `echo-${x}-${y}` }; // Echo Chamber
  }
  if (x === 7 && y === 1) {
    return { strength: 0.8, type: ECHO_TYPES[2], id: `echo-${x}-${y}` }; // Time Warp
  }
  if (x === 0 && y === 0) {
    return { strength: 0.1, type: ECHO_TYPES[3], id: `echo-${x}-${y}` }; // Stable Zone (low ambient)
  }

  // Simulate ambient temporal noise for other locations
  // The 'randomFactor' is deterministic based on coordinates for consistent testing.
  const randomFactor = (x * 13 + y * 7) % 100 / 1000; 
  return {
    strength: 0.05 + randomFactor, // Low base strength plus a small, deterministic variation
    type: ECHO_TYPES[3], // Default to Stable Zone for ambient noise
    id: `echo-${x}-${y}`
  };
};
