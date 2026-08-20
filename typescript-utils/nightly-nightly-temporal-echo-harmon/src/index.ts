export interface TemporalEcho {
  id: string;
  timestamp: Date;
  message: string;
}

export interface HarmonizedNarrative {
  id: string;
  echoes: TemporalEcho[];
  summary: string;
  sentiment: 'positive' | 'negative' | 'neutral' | 'mixed';
  temporalSpanMs: number;
}

export class TemporalEchoHarmonizer {
  private readonly timeThresholdMs: number; // Max time difference between echoes to be considered part of the same narrative

  constructor(timeThresholdMinutes: number = 5) {
    this.timeThresholdMs = timeThresholdMinutes * 60 * 1000;
  }

  /**
   * Analyzes the sentiment of a message.
   * # Mock rationale: This is a simplified, deterministic sentiment analysis for offline testing.
   * In a real-world scenario, this would involve a more complex NLP library or API.
   */
  private analyzeSentiment(message: string): 'positive' | 'negative' | 'neutral' | 'mixed' {
    const lowerMessage = message.toLowerCase();
    let positiveCount = 0;
    let negativeCount = 0;

    const positiveKeywords = ['hope', 'safe', 'resource', 'found', 'good', 'clear', 'stable', 'repair'];
    const negativeKeywords = ['danger', 'threat', 'lost', 'broken', 'empty', 'storm', 'anomaly', 'corrupt'];

    for (const keyword of positiveKeywords) {
      if (lowerMessage.includes(keyword)) {
        positiveCount++;
      }
    }
    for (const keyword of negativeKeywords) {
      if (lowerMessage.includes(keyword)) {
        negativeCount++;
      }
    }

    if (positiveCount > 0 && negativeCount === 0) return 'positive';
    if (negativeCount > 0 && positiveCount === 0) return 'negative';
    if (positiveCount > 0 && negativeCount > 0) return 'mixed';
    return 'neutral';
  }

  /**
   * Generates a summary for a narrative.
   * # Mock rationale: This is a simplified summary generation for offline testing.
   * A real summary might use extractive or abstractive summarization.
   */
  private generateSummary(echoes: TemporalEcho[]): string {
    if (echoes.length === 0) return "No echoes found.";
    if (echoes.length === 1) return `Single echo: "${echoes[0].message}"`;

    const messages = echoes.map(e => e.message);
    const firstMessage = messages[0];
    const lastMessage = messages[messages.length - 1];

    // Simple summary: first and last message, or a concatenation if short
    if (messages.join(' ').length < 150) {
      return `Sequence of ${echoes.length} echoes: "${messages.join('; ')}"`;
    }
    return `Sequence of ${echoes.length} echoes, from "${firstMessage}" to "${lastMessage}".`;
  }

  /**
   * Harmonizes a list of temporal echoes into coherent narratives.
   * @param echoes An array of TemporalEcho objects.
   * @returns An array of HarmonizedNarrative objects.
   */
  public harmonize(echoes: TemporalEcho[]): HarmonizedNarrative[] {
    if (echoes.length === 0) {
      return [];
    }

    // Sort echoes by timestamp
    const sortedEchoes = [...echoes].sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());

    const narratives: HarmonizedNarrative[] = [];
    let currentNarrativeEchoes: TemporalEcho[] = [];

    for (let i = 0; i < sortedEchoes.length; i++) {
      const currentEcho = sortedEchoes[i];

      if (currentNarrativeEchoes.length === 0) {
        currentNarrativeEchoes.push(currentEcho);
      } else {
        const lastEchoInNarrative = currentNarrativeEchoes[currentNarrativeEchoes.length - 1];
        if (currentEcho.timestamp.getTime() - lastEchoInNarrative.timestamp.getTime() <= this.timeThresholdMs) {
          currentNarrativeEchoes.push(currentEcho);
        } else {
          // Current echo is too far apart, finalize the current narrative and start a new one
          const firstTimestamp = currentNarrativeEchoes[0].timestamp.getTime();
          const lastTimestamp = currentNarrativeEchoes[currentNarrativeEchoes.length - 1].timestamp.getTime();
          const temporalSpanMs = lastTimestamp - firstTimestamp;

          const allMessages = currentNarrativeEchoes.map(e => e.message).join(' ');
          narratives.push({
            id: `narrative-${narratives.length + 1}`,
            echoes: currentNarrativeEchoes,
            summary: this.generateSummary(currentNarrativeEchoes),
            sentiment: this.analyzeSentiment(allMessages),
            temporalSpanMs: temporalSpanMs,
          });
          currentNarrativeEchoes = [currentEcho]; // Start new narrative
        }
      }
    }

    // Add the last narrative if it exists
    if (currentNarrativeEchoes.length > 0) {
      const firstTimestamp = currentNarrativeEchoes[0].timestamp.getTime();
      const lastTimestamp = currentNarrativeEchoes[currentNarrativeEchoes.length - 1].getTime();
      const temporalSpanMs = lastTimestamp - firstTimestamp;

      const allMessages = currentNarrativeEchoes.map(e => e.message).join(' ');
      narratives.push({
        id: `narrative-${narratives.length + 1}`,
        echoes: currentNarrativeEchoes,
        summary: this.generateSummary(currentNarrativeEchoes),
        sentiment: this.analyzeSentiment(allMessages),
        temporalSpanMs: temporalSpanMs,
      });
    }

    return narratives;
  }
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log("Usage: ts-node src/index.ts <timeThresholdMinutes> [echo1_timestamp] [echo1_message] [echo2_timestamp] [echo2_message] ...");
    console.log("Example: ts-node src/index.ts 5 2023-01-01T10:00:00Z 'Found supplies' 2023-01-01T10:02:00Z 'Area clear'");
    process.exit(1);
  }

  const timeThresholdMinutes = parseInt(args[0], 10);
  if (isNaN(timeThresholdMinutes) || timeThresholdMinutes <= 0) {
    console.error("Error: timeThresholdMinutes must be a positive number.");
    process.exit(1);
  }

  const echoes: TemporalEcho[] = [];
  for (let i = 1; i < args.length; i += 2) {
    if (i + 1 < args.length) {
      const timestampStr = args[i];
      const message = args[i + 1];
      try {
        const timestamp = new Date(timestampStr);
        if (isNaN(timestamp.getTime())) {
          throw new Error(`Invalid timestamp format: ${timestampStr}`);
        }
        echoes.push({ id: `echo-${echoes.length + 1}`, timestamp, message });
      } catch (e: any) {
        console.error(`Error parsing echo at index ${i}: ${e.message}`);
        process.exit(1);
      }
    } else {
      console.error("Error: Mismatched timestamp and message arguments.");
      process.exit(1);
    }
  }

  const harmonizer = new TemporalEchoHarmonizer(timeThresholdMinutes);
  const narratives = harmonizer.harmonize(echoes);

  console.log(JSON.stringify(narratives, null, 2));
}
