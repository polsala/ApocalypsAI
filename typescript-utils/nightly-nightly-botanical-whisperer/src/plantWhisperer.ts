export enum PlantState {
  Happy = "Happy",
  Thirsty = "Thirsty",
  Hungry = "Hungry",
  Stressed = "Stressed",
  Lonely = "Lonely",
  Confused = "Confused",
}

export interface WhisperData {
  moisture: number; // 0-100%
  light: number;    // 0-100%
  temperature: number; // Celsius
  vibrationFrequency: number; // Hz, e.g., for "loneliness"
}

export function interpretWhispers(data: WhisperData): PlantState {
  if (data.moisture < 20) return PlantState.Thirsty;
  if (data.light < 30) return PlantState.Stressed; // Not enough light
  if (data.temperature > 30 || data.temperature < 10) return PlantState.Stressed;
  if (data.vibrationFrequency < 5) return PlantState.Lonely; // Low hum, needs attention
  if (data.moisture > 80 && data.light > 70 && data.temperature > 20 && data.temperature < 28 && data.vibrationFrequency > 10) return PlantState.Happy;
  
  // More complex rules or default
  if (data.moisture > 70 && data.light < 50) return PlantState.Confused; // Overwatered but dark?
  
  return PlantState.Confused; // Default if no clear state
}

export function suggestAction(state: PlantState): string {
  switch (state) {
    case PlantState.Happy:
      return "Your plant is thriving! Keep up the good work, and perhaps offer a gentle leaf polish.";
    case PlantState.Thirsty:
      return "A parched whisper! Offer a refreshing drink of filtered water, slowly and deeply.";
    case PlantState.Hungry:
      return "A rumbling root! Consider a gentle, diluted nutrient solution.";
    case PlantState.Stressed:
      return "A tense rustle! Check its environment: too hot, too cold, or not enough light? Adjust accordingly.";
    case PlantState.Lonely:
      return "A faint tremor! Spend some quality time: talk to it, rotate it, or introduce a friendly plant neighbor.";
    case PlantState.Confused:
      return "A bewildered rustle! Re-evaluate all conditions. Perhaps it needs a change of scenery or a new pot?";
    default:
      return "The whispers are unclear. Observe closely and trust your intuition, caretaker.";
  }
}
