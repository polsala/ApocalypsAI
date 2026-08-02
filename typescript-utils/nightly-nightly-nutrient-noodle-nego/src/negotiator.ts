import { NutrientPaste, ConsumptionRecord } from './types';

export class NutrientNoodleNegotiator {
  private pastes: NutrientPaste[];
  private consumptionRecord: ConsumptionRecord;
  private historySize: number;

  constructor(pastes: NutrientPaste[], record: ConsumptionRecord, historySize: number = 3) {
    if (pastes.length === 0) {
      throw new Error("No nutrient pastes available.");
    }
    this.pastes = pastes;
    this.consumptionRecord = {
      lastConsumedId: record.lastConsumedId,
      history: record.history || [],
    };
    this.historySize = historySize;
  }

  private getPasteById(id: string): NutrientPaste | undefined {
    return this.pastes.find(p => p.id === id);
  }

  private getNextRotationalPaste(): NutrientPaste {
    if (!this.consumptionRecord.lastConsumedId) {
      return this.pastes[0]; // Start with the first if nothing consumed yet
    }

    const lastIndex = this.pastes.findIndex(p => p.id === this.consumptionRecord.lastConsumedId);
    const nextIndex = (lastIndex + 1) % this.pastes.length;
    return this.pastes[nextIndex];
  }

  /**
   * Suggests the next nutrient paste.
   * If a moodTag is provided, it tries to find a matching paste not recently consumed.
   * Falls back to rotational suggestion if no mood match or all mood matches are in history.
   * @param moodTag An optional tag to influence the suggestion.
   * @returns An object containing the suggested NutrientPaste and the updated ConsumptionRecord.
   */
  suggestNext(moodTag?: string): { suggestion: NutrientPaste; record: ConsumptionRecord } {
    let suggestedPaste: NutrientPaste;

    if (moodTag) {
      const eligiblePastes = this.pastes.filter(p =>
        p.tags.includes(moodTag) && !this.consumptionRecord.history.includes(p.id)
      );

      if (eligiblePastes.length > 0) {
        // Prioritize mood-matching, not recently consumed. Pick the first eligible for simplicity.
        suggestedPaste = eligiblePastes[0];
      } else {
        // Fallback to rotational if no mood-match or all mood-matches recently consumed
        suggestedPaste = this.getNextRotationalPaste();
      }
    } else {
      suggestedPaste = this.getNextRotationalPaste();
    }

    // Update consumption record: add new suggestion to history and trim to historySize
    const newHistory = [suggestedPaste.id, ...this.consumptionRecord.history].slice(0, this.historySize);
    const newRecord: ConsumptionRecord = {
      lastConsumedId: suggestedPaste.id,
      history: newHistory,
    };

    return { suggestion: suggestedPaste, record: newRecord };
  }
}
