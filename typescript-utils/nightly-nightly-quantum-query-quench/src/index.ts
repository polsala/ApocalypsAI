type RetryStrategy = {
  maxRetries: number;
  initialDelayMs: number;
  backoffFactor: number;
};

type RateLimitStrategy = {
  maxRequests: number;
  intervalMs: number;
};

interface QuantumQuencherConfig {
  retryStrategy?: RetryStrategy;
  rateLimitStrategy?: RateLimitStrategy;
}

const DEFAULT_RETRY_STRATEGY: RetryStrategy = {
  maxRetries: 3,
  initialDelayMs: 100,
  backoffFactor: 2,
};

const DEFAULT_RATE_LIMIT_STRATEGY: RateLimitStrategy = {
  maxRequests: 5,
  intervalMs: 1000, // 5 requests per second
};

class QuantumQuencher {
  private retryStrategy: RetryStrategy;
  private rateLimitStrategy: RateLimitStrategy;
  private requestTimestamps: number[] = [];

  constructor(config?: QuantumQuencherConfig) {
    this.retryStrategy = { ...DEFAULT_RETRY_STRATEGY, ...config?.retryStrategy };
    this.rateLimitStrategy = { ...DEFAULT_RATE_LIMIT_STRATEGY, ...config?.rateLimitStrategy };
  }

  private async delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private async waitForRateLimit(): Promise<void> {
    const now = Date.now();
    // Clean up old timestamps
    this.requestTimestamps = this.requestTimestamps.filter(
      timestamp => now - timestamp < this.rateLimitStrategy.intervalMs
    );

    if (this.requestTimestamps.length >= this.rateLimitStrategy.maxRequests) {
      const oldestRequestTime = this.requestTimestamps[0];
      const timeToWait = this.rateLimitStrategy.intervalMs - (now - oldestRequestTime);
      if (timeToWait > 0) {
        await this.delay(timeToWait);
      }
    }
    this.requestTimestamps.push(Date.now());
  }

  public async query<T>(
    operation: () => Promise<T>,
    operationName: string = 'Unnamed Operation'
  ): Promise<T> {
    let retries = 0;
    let delayMs = this.retryStrategy.initialDelayMs;

    while (retries <= this.retryStrategy.maxRetries) {
      try {
        await this.waitForRateLimit();
        const result = await operation();
        return result;
      } catch (error: any) {
        console.warn(
          `[QuantumQuencher] ${operationName} failed (attempt ${retries + 1}/${this.retryStrategy.maxRetries + 1}). Error: ${error.message || error}`
        );
        if (retries < this.retryStrategy.maxRetries) {
          await this.delay(delayMs);
          delayMs *= this.retryStrategy.backoffFactor;
          retries++;
        } else {
          throw new Error(`[QuantumQuencher] ${operationName} failed after ${this.retryStrategy.maxRetries + 1} attempts: ${error.message || error}`);
        }
      }
    }
    // This line should theoretically not be reached due to the throw in the else block
    throw new Error(`[QuantumQuencher] Unexpected termination for ${operationName}`);
  }
}

export { QuantumQuencher, QuantumQuencherConfig, RetryStrategy, RateLimitStrategy };
