import { WhisperCategory, WhisperPrompt, WhisperOutcome } from './types';
import { WHISPER_PROMPTS } from './data';

/**
 * Generates a whimsical, structured piece of advice (a 'whisper') for post-apocalyptic decisions.
 * @param category An optional category to filter the whispers (e.g., "Resource", "Shelter").
 * @returns A WhisperOutcome object containing the advice.
 * @throws Error if no whispers are found for the specified category.
 */
export function generateWhisper(category?: WhisperCategory): WhisperOutcome {
  const availablePrompts = category
    ? WHISPER_PROMPTS.filter(p => p.category === category)
    : WHISPER_PROMPTS;

  if (availablePrompts.length === 0) {
    throw new Error(`No whispers found for category: ${category}`);
  }

  const randomIndex = Math.floor(Math.random() * availablePrompts.length);
  const selectedPrompt = availablePrompts[randomIndex];

  return {
    category: selectedPrompt.category,
    prompt: selectedPrompt.prompt,
    action: selectedPrompt.actionVerb,
    risk: selectedPrompt.riskLevel,
    timestamp: new Date().toISOString(),
  };
}
