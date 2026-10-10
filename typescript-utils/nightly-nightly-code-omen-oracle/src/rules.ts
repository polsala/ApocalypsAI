import { OmenRule } from './types';

export const OMEN_RULES: OmenRule[] = [
  {
    match: 'no-unused-vars',
    omenTitle: 'The Whispering Ghost of Unused Variables',
    omenDescription: 'Unseen entities linger, consuming precious essence without purpose.',
    advice: 'Purge the forgotten spirits; let only the active thrive.',
    severity: 'minor',
  },
  {
    match: 'indent',
    omenTitle: 'The Shifting Sands of Indentation',
    omenDescription: 'The very foundation of your script wavers, causing disorientation.',
    advice: 'Align your pillars with unwavering precision, lest the structure collapse.',
    severity: 'moderate',
  },
  {
    match: 'semi',
    omenTitle: 'The Forgotten Semicolon',
    omenDescription: 'A crucial pause is omitted, leading to a cascade of unintended consequences.',
    advice: 'Mark the end of each thought with a decisive gesture, bringing clarity.',
    severity: 'minor',
  },
  {
    match: 'no-explicit-any',
    omenTitle: 'The Veil of Any',
    omenDescription: 'A shroud of ambiguity covers your intentions, inviting chaos.',
    advice: 'Unmask the true nature of your constructs; clarity banishes uncertainty.',
    severity: 'severe',
  },
  {
    match: 'max-len',
    omenTitle: 'The Endless Scroll',
    omenDescription: 'Your writings stretch beyond the horizon, wearying the reader\'s eye.',
    advice: 'Divide your wisdom into digestible verses, for brevity is a virtue.',
    severity: 'minor',
  },
  {
    match: /no-(unsafe|unnecessary|redundant)/, // Regex example
    omenTitle: 'The Burden of Excess',
    omenDescription: 'Superfluous elements weigh down your creation, hindering its swift flight.',
    advice: 'Shed the unnecessary; embrace the lean path to efficiency.',
    severity: 'moderate',
  },
  // Default omen for general errors
  {
    match: 'default-error',
    omenTitle: 'The Unseen Rift',
    omenDescription: 'A tear in the fabric of your logic, its origin obscured.',
    advice: 'Seek the source of the disturbance; mend the rift before it widens.',
    severity: 'severe',
  },
  // Default omen for general warnings
  {
    match: 'default-warning',
    omenTitle: 'The Faint Echo',
    omenDescription: 'A subtle dissonance resonates, a precursor to greater disharmony.',
    advice: 'Heed the whispers of caution; small adjustments now prevent future turmoil.',
    severity: 'moderate',
  },
];
