import { PlantState, WhisperData, interpretWhispers, suggestAction } from '../src/plantWhisperer';

describe('interpretWhispers', () => {
  it('should return Thirsty for low moisture', () => {
    const data: WhisperData = { moisture: 10, light: 50, temperature: 22, vibrationFrequency: 15 };
    expect(interpretWhispers(data)).toBe(PlantState.Thirsty);
  });

  it('should return Stressed for low light', () => {
    const data: WhisperData = { moisture: 50, light: 10, temperature: 22, vibrationFrequency: 15 };
    expect(interpretWhispers(data)).toBe(PlantState.Stressed);
  });

  it('should return Stressed for high temperature', () => {
    const data: WhisperData = { moisture: 50, light: 50, temperature: 35, vibrationFrequency: 15 };
    expect(interpretWhispers(data)).toBe(PlantState.Stressed);
  });

  it('should return Stressed for low temperature', () => {
    const data: WhisperData = { moisture: 50, light: 50, temperature: 5, vibrationFrequency: 15 };
    expect(interpretWhispers(data)).toBe(PlantState.Stressed);
  });

  it('should return Lonely for low vibration frequency', () => {
    const data: WhisperData = { moisture: 50, light: 50, temperature: 22, vibrationFrequency: 2 };
    expect(interpretWhispers(data)).toBe(PlantState.Lonely);
  });

  it('should return Happy for optimal conditions', () => {
    const data: WhisperData = { moisture: 85, light: 75, temperature: 25, vibrationFrequency: 12 };
    expect(interpretWhispers(data)).toBe(PlantState.Happy);
  });

  it('should return Confused for conflicting/unclear conditions (e.g., overwatered but dark)', () => {
    const data: WhisperData = { moisture: 85, light: 20, temperature: 22, vibrationFrequency: 15 };
    expect(interpretWhispers(data)).toBe(PlantState.Confused);
  });

  it('should return Confused for default unknown state', () => {
    const data: WhisperData = { moisture: 60, light: 60, temperature: 15, vibrationFrequency: 8 }; // Not happy, not clearly stressed/thirsty/lonely
    expect(interpretWhispers(data)).toBe(PlantState.Confused);
  });
});

describe('suggestAction', () => {
  it('should suggest action for Happy state', () => {
    expect(suggestAction(PlantState.Happy)).toContain('thriving');
  });

  it('should suggest action for Thirsty state', () => {
    expect(suggestAction(PlantState.Thirsty)).toContain('drink');
  });

  it('should suggest action for Stressed state', () => {
    expect(suggestAction(PlantState.Stressed)).toContain('environment');
  });

  it('should suggest action for Lonely state', () => {
    expect(suggestAction(PlantState.Lonely)).toContain('quality time');
  });

  it('should suggest action for Confused state', () => {
    expect(suggestAction(PlantState.Confused)).toContain('Re-evaluate');
  });

  it('should suggest action for Hungry state (even if not directly interpreted yet)', () => {
    expect(suggestAction(PlantState.Hungry)).toContain('nutrient solution');
  });
});
