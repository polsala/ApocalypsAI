import { expect } from 'chai';
import { convertToCosmicDate } from '../src/main';

describe('Cosmic Calendar Converter', () => {

  // # Mock rationale: Date objects are inherently tied to the system clock or specific inputs.
  // To ensure deterministic and offline tests, we create specific Date instances for known Earth dates
  // and verify their conversion to Cosmic Dates against expected outcomes.
  // All test dates are explicitly created as UTC dates to match the utility's internal UTC processing.

  it('should correctly convert the Cosmic Epoch date (2000-01-01)', () => {
    const earthDate = new Date('2000-01-01T12:00:00Z'); // UTC date
    const cosmicDate = convertToCosmicDate(earthDate);
    expect(cosmicDate).to.deep.equal({
      stellarCycle: 1,
      phaseName: 'Genesis Glow',
      phaseNumber: 1,
      dayInPhase: 1,
      isTemporalFlux: false
    });
  });

  it('should correctly convert a date in the middle of a phase (2023-10-27)', () => {
    const earthDate = new Date('2023-10-27T12:00:00Z'); // Day 300 of 2023
    const cosmicDate = convertToCosmicDate(earthDate);
    expect(cosmicDate).to.deep.equal({
      stellarCycle: 24,
      phaseName: 'Celestial Chill',
      phaseNumber: 11,
      dayInPhase: 20,
      isTemporalFlux: false
    });
  });

  it('should correctly convert a date at the beginning of a new phase (2023-01-29)', () => {
    const earthDate = new Date('2023-01-29T12:00:00Z'); // Day 29 of 2023
    const cosmicDate = convertToCosmicDate(earthDate);
    expect(cosmicDate).to.deep.equal({
      stellarCycle: 24,
      phaseName: 'Astral Bloom',
      phaseNumber: 2,
      dayInPhase: 1,
      isTemporalFlux: false
    });
  });

  it('should correctly convert a date at the end of a phase (2023-01-28)', () => {
    const earthDate = new Date('2023-01-28T12:00:00Z'); // Day 28 of 2023
    const cosmicDate = convertToCosmicDate(earthDate);
    expect(cosmicDate).to.deep.equal({
      stellarCycle: 24,
      phaseName: 'Genesis Glow',
      phaseNumber: 1,
      dayInPhase: 28,
      isTemporalFlux: false
    });
  });

  it('should correctly convert the last phased day of a non-leap year (2023-12-30)', () => {
    const earthDate = new Date('2023-12-30T12:00:00Z'); // Day 364 of 2023
    const cosmicDate = convertToCosmicDate(earthDate);
    expect(cosmicDate).to.deep.equal({
      stellarCycle: 24,
      phaseName: 'Omega Orb',
      phaseNumber: 13,
      dayInPhase: 28,
      isTemporalFlux: false
    });
  });

  it('should correctly identify the first Temporal Flux day in a non-leap year (2023-12-31)', () => {
    const earthDate = new Date('2023-12-31T12:00:00Z'); // Day 365 of 2023
    const cosmicDate = convertToCosmicDate(earthDate);
    expect(cosmicDate).to.deep.equal({
      stellarCycle: 24,
      phaseName: 'Temporal Flux',
      phaseNumber: 0,
      dayInPhase: 0,
      isTemporalFlux: true,
      temporalFluxDayNumber: 1
    });
  });

  it('should correctly identify the last phased day of a leap year (2000-12-29)', () => {
    const earthDate = new Date('2000-12-29T12:00:00Z'); // Day 364 of 2000
    const cosmicDate = convertToCosmicDate(earthDate);
    expect(cosmicDate).to.deep.equal({
      stellarCycle: 1,
      phaseName: 'Omega Orb',
      phaseNumber: 13,
      dayInPhase: 28,
      isTemporalFlux: false
    });
  });

  it('should correctly identify the first Temporal Flux day in a leap year (2000-12-30)', () => {
    const earthDate = new Date('2000-12-30T12:00:00Z'); // Day 365 of 2000 (leap year)
    const cosmicDate = convertToCosmicDate(earthDate);
    expect(cosmicDate).to.deep.equal({
      stellarCycle: 1,
      phaseName: 'Temporal Flux',
      phaseNumber: 0,
      dayInPhase: 0,
      isTemporalFlux: true,
      temporalFluxDayNumber: 1
    });
  });

  it('should correctly identify the second Temporal Flux day in a leap year (2024-12-31)', () => {
    const earthDate = new Date('2024-12-31T12:00:00Z'); // Day 366 of 2024 (leap year)
    const cosmicDate = convertToCosmicDate(earthDate);
    expect(cosmicDate).to.deep.equal({
      stellarCycle: 25,
      phaseName: 'Temporal Flux',
      phaseNumber: 0,
      dayInPhase: 0,
      isTemporalFlux: true,
      temporalFluxDayNumber: 2
    });
  });

  it('should correctly convert a date in a leap year, not a flux day (2024-02-29)', () => {
    const earthDate = new Date('2024-02-29T12:00:00Z'); // Day 60 of 2024
    const cosmicDate = convertToCosmicDate(earthDate);
    expect(cosmicDate).to.deep.equal({
      stellarCycle: 25,
      phaseName: 'Nebula Nurture',
      phaseNumber: 3,
      dayInPhase: 4,
      isTemporalFlux: false
    });
  });

  it('should handle dates far in the past (1999-01-01) - before epoch', () => {
    const earthDate = new Date('1999-01-01T12:00:00Z');
    const cosmicDate = convertToCosmicDate(earthDate);
    expect(cosmicDate).to.deep.equal({
      stellarCycle: 0,
      phaseName: 'Genesis Glow',
      phaseNumber: 1,
      dayInPhase: 1,
      isTemporalFlux: false
    });
  });

  it('should handle dates far in the future (2100-07-15)', () => {
    const earthDate = new Date('2100-07-15T12:00:00Z'); // Day 196 of 2100 (not a leap year)
    const cosmicDate = convertToCosmicDate(earthDate);
    expect(cosmicDate).to.deep.equal({
      stellarCycle: 101,
      phaseName: 'Galactic Glimmer',
      phaseNumber: 7,
      dayInPhase: 28,
      isTemporalFlux: false
    });
  });

});
