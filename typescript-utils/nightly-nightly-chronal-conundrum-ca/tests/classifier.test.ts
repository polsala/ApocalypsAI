import { classifyConundrum } from '../src/classifier';
import { ConundrumCategory } from '../src/types';

describe('classifyConundrum', () => {
  it('should classify temporal ripples correctly', () => {
    const result = classifyConundrum('The clock is running backwards again.');
    expect(result.category).toBe<ConundrumCategory>('Temporal Ripple');
    expect(result.action).toContain('chronometer');
    expect(result.confidence).toBe(0.85);
  });

  it('should classify reality glitches correctly', () => {
    const result = classifyConundrum('My cat started speaking fluent Latin.');
    expect(result.category).toBe<ConundrumCategory>('Reality Glitch');
    expect(result.action).toContain('eye contact');
    expect(result.confidence).toBe(0.90);
  });

  it('should classify existential echoes correctly', () => {
    const result = classifyConundrum('I\'m questioning the meaning of my existence after seeing a sentient toaster.');
    expect(result.category).toBe<ConundrumCategory>('Existential Echo');
    expect(result.action).toContain('pun');
    expect(result.confidence).toBe(0.75);
  });

  it('should classify cosmic jokes correctly', () => {
    const result = classifyConundrum('A banana peel just tap-danced across the floor.');
    expect(result.category).toBe<ConundrumCategory>('Cosmic Joke');
    expect(result.action).toContain('absurdity');
    expect(result.confidence).toBe(0.95);
  });

  it('should classify unknown anomalies for unmatching descriptions', () => {
    const result = classifyConundrum('The air smells faintly of blueberries and regret.');
    expect(result.category).toBe<ConundrumCategory>('Unknown Anomaly');
    expect(result.action).toContain('caution');
    expect(result.confidence).toBe(0.50);
  });

  it('should handle case insensitivity for temporal ripples', () => {
    const result = classifyConundrum('YESTERDAY happened TWICE.');
    expect(result.category).toBe<ConundrumCategory>('Temporal Ripple');
  });

  it('should handle case insensitivity for reality glitches', () => {
    const result = classifyConundrum('My COFFEE turned into a NEWT.');
    expect(result.category).toBe<ConundrumCategory>('Reality Glitch');
  });

  it('should return a confidence score for all classifications', () => {
    const result1 = classifyConundrum('My coffee turned into a newt');
    expect(result1.confidence).toBeGreaterThan(0);
    expect(result1.confidence).toBeLessThanOrEqual(1);

    const result2 = classifyConundrum('Time is a flat circle.');
    expect(result2.confidence).toBeGreaterThan(0);
    expect(result2.confidence).toBeLessThanOrEqual(1);
  });
});
