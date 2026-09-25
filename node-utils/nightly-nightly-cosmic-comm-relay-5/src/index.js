/**
 * @typedef {object} RelayOptions
 * @property {number} [minDelayMs=100] - Minimum delay in milliseconds.
 * @property {number} [maxDelayMs=1000] - Maximum delay in milliseconds.
 * @property {number} [packetLossRate=0.05] - Probability of packet loss (0.0 to 1.0).
 */

/**
 * Simulates interstellar communication delays and packet loss.
 */
class CosmicCommRelay {
  /**
   * @param {RelayOptions} options - Configuration options for the relay.
   */
  constructor(options = {}) {
    this.minDelayMs = options.minDelayMs || 100;
    this.maxDelayMs = options.maxDelayMs || 1000;
    this.packetLossRate = options.packetLossRate || 0.05;

    if (this.minDelayMs < 0 || this.maxDelayMs < 0 || this.minDelayMs > this.maxDelayMs) {
      throw new Error('Invalid delay options. minDelayMs must be non-negative and less than or equal to maxDelayMs.');
    }
    if (this.packetLossRate < 0 || this.packetLossRate > 1) {
      throw new Error('Invalid packetLossRate. Must be between 0.0 and 1.0.');
    }
  }

  /**
   * Simulates a delay.
   * @returns {Promise<void>}
   */
  async simulateDelay() {
    const delay = Math.random() * (this.maxDelayMs - this.minDelayMs) + this.minDelayMs;
    await new Promise(resolve => setTimeout(resolve, delay));
  }

  /**
   * Simulates packet loss.
   * @returns {boolean} - True if packet is lost, false otherwise.
   */
  simulatePacketLoss() {
    return Math.random() < this.packetLossRate;
  }

  /**
   * Fetches a resource with simulated cosmic communication effects.
   * @param {string} url - The URL to fetch.
   * @param {object} [fetchOptions={}] - Options to pass to the underlying fetch.
   * @returns {Promise<Response>}
   */
  async fetch(url, fetchOptions = {}) {
    await this.simulateDelay();

    if (this.simulatePacketLoss()) {
      const error = new Error(`Cosmic interference: Packet lost to ${url}`);
      // Mock rationale: Simulate a network error that fetch would throw.
      error.code = 'ENETUNREACH'; // Example error code
      throw error;
    }

    // Mock rationale: Use a mock fetch implementation for deterministic testing.
    // In a real-world scenario, this would be the actual fetch API.
    const mockFetch = global.fetch || (() => {
      throw new Error('Global fetch not available. This should be mocked during tests.');
    });

    try {
      const response = await mockFetch(url, fetchOptions);
      if (!response.ok) {
        // Mock rationale: Simulate non-ok HTTP responses.
        const error = new Error(`Cosmic anomaly: HTTP error ${response.status} for ${url}`);
        error.status = response.status;
        throw error;
      }
      return response;
    } catch (error) {
      // Re-throw any errors from the underlying fetch, potentially adding context.
      throw error;
    }
  }
}

module.exports = { CosmicCommRelay };
