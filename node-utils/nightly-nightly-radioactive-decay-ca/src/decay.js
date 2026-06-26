function calculateRemaining(initialAmount, halfLife, elapsedTime) {
  if (halfLife <= 0) {
    throw new Error('Half-life must be positive');
  }
  const decayFactor = Math.pow(0.5, elapsedTime / halfLife);
  return initialAmount * decayFactor;
}

module.exports = { calculateRemaining };
