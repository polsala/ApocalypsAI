import { TemporalEchoHarmonizer, TemporalEcho, HarmonizedNarrative } from '../src/index';

describe('TemporalEchoHarmonizer', () => {
  const MOCK_DATE_BASE = new Date('2023-01-01T12:00:00Z'); // # Mock rationale: Using a fixed base date for deterministic timestamp generation.

  const createEcho = (id: string, minutesOffset: number, message: string): TemporalEcho => ({
    id,
    timestamp: new Date(MOCK_DATE_BASE.getTime() + minutesOffset * 60 * 1000),
    message,
  });

  it('should return an empty array for no echoes', () => {
    const harmonizer = new TemporalEchoHarmonizer(5);
    expect(harmonizer.harmonize([])).toEqual([]);
  });

  it('should treat a single echo as one narrative', () => {
    const harmonizer = new TemporalEchoHarmonizer(5);
    const echoes = [createEcho('e1', 0, 'First contact.')];
    const narratives = harmonizer.harmonize(echoes);

    expect(narratives.length).toBe(1);
    expect(narratives[0].echoes).toEqual(echoes);
    expect(narratives[0].summary).toContain('Single echo');
    expect(narratives[0].sentiment).toBe('neutral');
    expect(narratives[0].temporalSpanMs).toBe(0);
  });

  it('should group echoes within the time threshold into one narrative', () => {
    const harmonizer = new TemporalEchoHarmonizer(10); // 10 minutes threshold
    const echoes = [
      createEcho('e1', 0, 'Signal detected.'),
      createEcho('e2', 5, 'Signal strength increasing.'),
      createEcho('e3', 8, 'Anomaly stable.'),
    ];
    const narratives = harmonizer.harmonize(echoes);

    expect(narratives.length).toBe(1);
    expect(narratives[0].echoes).toEqual(echoes);
    expect(narratives[0].summary).toContain('Sequence of 3 echoes');
    expect(narratives[0].sentiment).toBe('positive'); // 'stable' keyword
    expect(narratives[0].temporalSpanMs).toBe(8 * 60 * 1000);
  });

  it('should create multiple narratives for echoes outside the time threshold', () => {
    const harmonizer = new TemporalEchoHarmonizer(5); // 5 minutes threshold
    const echoes = [
      createEcho('e1', 0, 'First message.'),
      createEcho('e2', 3, 'Second message.'),
      createEcho('e3', 10, 'Third message, much later.'), // 7 min after e2, > 5 min threshold
      createEcho('e4', 12, 'Fourth message.'),
    ];
    const narratives = harmonizer.harmonize(echoes);

    expect(narratives.length).toBe(2);

    expect(narratives[0].echoes).toEqual([echoes[0], echoes[1]]);
    expect(narratives[0].summary).toContain('Sequence of 2 echoes');
    expect(narratives[0].sentiment).toBe('neutral');
    expect(narratives[0].temporalSpanMs).toBe(3 * 60 * 1000);

    expect(narratives[1].echoes).toEqual([echoes[2], echoes[3]]);
    expect(narratives[1].summary).toContain('Sequence of 2 echoes');
    expect(narratives[1].sentiment).toBe('neutral');
    expect(narratives[1].temporalSpanMs).toBe(2 * 60 * 1000);
  });

  it('should correctly analyze sentiment', () => {
    const harmonizer = new TemporalEchoHarmonizer(5);
    const echoesPositive = [createEcho('e1', 0, 'Found supplies, all good!')];
    const echoesNegative = [createEcho('e1', 0, 'Danger ahead, system broken.')];
    const echoesMixed = [createEcho('e1', 0, 'Found a resource, but the area is dangerous.')];
    const echoesNeutral = [createEcho('e1', 0, 'Just a regular log entry.')];

    expect(harmonizer.harmonize(echoesPositive)[0].sentiment).toBe('positive');
    expect(harmonizer.harmonize(echoesNegative)[0].sentiment).toBe('negative');
    expect(harmonizer.harmonize(echoesMixed)[0].sentiment).toBe('mixed');
    expect(harmonizer.harmonize(echoesNeutral)[0].sentiment).toBe('neutral');
  });

  it('should handle echoes with identical timestamps', () => {
    const harmonizer = new TemporalEchoHarmonizer(5);
    const echoes = [
      createEcho('e1', 0, 'Event A'),
      createEcho('e2', 0, 'Event B'),
      createEcho('e3', 1, 'Event C'),
    ];
    const narratives = harmonizer.harmonize(echoes);
    expect(narratives.length).toBe(1);
    expect(narratives[0].echoes.length).toBe(3);
    expect(narratives[0].temporalSpanMs).toBe(1 * 60 * 1000);
  });

  it('should handle a large gap followed by a small gap', () => {
    const harmonizer = new TemporalEchoHarmonizer(2); // 2 minutes threshold
    const echoes = [
      createEcho('e1', 0, 'Start sequence 1'),
      createEcho('e2', 1, 'Continue sequence 1'),
      createEcho('e3', 10, 'Start sequence 2'), // 9 min gap
      createEcho('e4', 11, 'Continue sequence 2'),
    ];
    const narratives = harmonizer.harmonize(echoes);

    expect(narratives.length).toBe(2);
    expect(narratives[0].echoes.length).toBe(2);
    expect(narratives[1].echoes.length).toBe(2);
    expect(narratives[0].echoes[0].id).toBe('e1');
    expect(narratives[1].echoes[0].id).toBe('e3');
  });

  it('should generate correct summary for short and long narratives', () => {
    const harmonizer = new TemporalEchoHarmonizer(5);
    const shortEchoes = [
      createEcho('e1', 0, 'Short message 1'),
      createEcho('e2', 1, 'Short message 2'),
    ];
    const longEchoes = [
      createEcho('e1', 0, 'This is a very long message that describes the beginning of a complex event.'),
      createEcho('e2', 1, 'Another long message detailing the middle part of the ongoing situation.'),
      createEcho('e3', 2, 'The final long message concluding the event with some important observations.'),
    ];

    const shortNarrative = harmonizer.harmonize(shortEchoes)[0];
    expect(shortNarrative.summary).toBe('Sequence of 2 echoes: "Short message 1; Short message 2"');

    const longNarrative = harmonizer.harmonize(longEchoes)[0];
    expect(longNarrative.summary).toContain('Sequence of 3 echoes, from "This is a very long message');
    expect(longNarrative.summary).toContain('to "The final long message');
  });
});
