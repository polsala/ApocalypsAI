import { CosmicAlignment, CosmicEntity, AlignedEntity } from './types';

const ONE_DAY_MS = 24 * 60 * 60 * 1000;
const ONE_WEEK_MS = 7 * ONE_DAY_MS;
const ONE_MONTH_MS = 30 * ONE_DAY_MS;

export function calculateAlignment(entity: CosmicEntity, now: Date = new Date()): AlignedEntity {
  let score = 0;
  let recommendation = "";

  // Base score from priority (if available)
  if (entity.priority !== undefined) {
    score += (5 - entity.priority) * 10; // Higher priority (lower number) means higher score
  }

  // Influence from last modified date (age)
  if (entity.lastModified) {
    const ageMs = now.getTime() - entity.lastModified.getTime();
    if (ageMs < ONE_DAY_MS) {
      score += 30; // Very recent
      recommendation += "Freshly manifested, a beacon of the present. ";
    } else if (ageMs < ONE_WEEK_MS) {
      score += 20; // Recent
      recommendation += "Recently touched by the cosmic winds. ";
    } else if (ageMs < ONE_MONTH_MS) {
      score += 10; // Moderately old
      recommendation += "Drifting in the near past. ";
    } else {
      score -= 15; // Quite old
      recommendation += "An ancient relic, its temporal signature fading. ";
    }
  } else {
    // If no lastModified, assume it's relatively new/current for tasks/tabs
    score += 25;
    recommendation += "Its origin is now, its potential vast. ";
  }

  // Influence from size/weight
  if (entity.sizeBytes !== undefined) {
    if (entity.sizeBytes > 100 * 1024 * 1024) { // >100MB
      score -= 10; // Large, potentially heavy
      recommendation += "A colossal entity, demanding significant energy. ";
    } else if (entity.sizeBytes > 10 * 1024 * 1024) { // >10MB
      score += 5; // Medium-large
      recommendation += "Substantial in form, yet manageable. ";
    } else if (entity.sizeBytes > 1 * 1024 * 1024) { // >1MB
      score += 10; // Medium
      recommendation += "A well-proportioned fragment of the cosmos. ";
    } else {
      score += 15; // Small
      recommendation += "A nimble particle, easily shifted. ";
    }
  } else {
    // Default 'weight' for tasks/tabs
    if (entity.type === 'task') {
      score += 10; // Tasks are generally medium weight
      recommendation += "A task of moderate cosmic density. ";
    } else if (entity.type === 'tab') {
      score += 15; // Tabs are often lighter
      recommendation += "A fleeting thought, light as stardust. ";
    }
  }

  // Influence from keywords (simple example)
  if (entity.keywords && entity.keywords.some(k => ['urgent', 'critical', 'now'].includes(k.toLowerCase()))) {
    score += 20;
    recommendation += "Urgent cosmic energies converge. ";
  }

  // Clamp score to a reasonable range
  score = Math.max(0, Math.min(100, score));

  let alignment: CosmicAlignment;
  if (score >= 80) {
    alignment = CosmicAlignment.GalacticHarmony;
    recommendation = "The stars align perfectly. This is an ideal moment to engage. " + recommendation;
  } else if (score >= 60) {
    alignment = CosmicAlignment.StellarConvergence;
    recommendation = "A strong pull from the cosmic currents. Focus your energy here. " + recommendation;
  } else if (score >= 40) {
    alignment = CosmicAlignment.TemporalFlux;
    recommendation = "Time is in motion, but a window of opportunity exists. " + recommendation;
  } else if (score >= 20) {
    alignment = CosmicAlignment.NebulaDrift;
    recommendation = "It drifts in the cosmic dust. Consider its path, but no immediate action is required. " + recommendation;
  } else {
    alignment = CosmicAlignment.VoidResonance;
    recommendation = "Echoes from the void. This entity demands attention or release. " + recommendation;
  }

  return {
    entity,
    alignment,
    score,
    recommendation: recommendation.trim()
  };
}
