export type TemporalAnomaly =
  | "déjà vu loop"
  | "minor time stutter"
  | "echo of forgotten past"
  | "chronal ripple"
  | "temporal echo"
  | "future premonition fragment"
  | "past memory bleed"
  | "temporal displacement itch"
  | "void whisper resonance"
  | "unsettling stillness";

export type HarmonizationRitual = {
  title: string;
  description: string;
  action: string;
};

const harmonizationMap: Record<TemporalAnomaly, HarmonizationRitual> = {
  "déjà vu loop": {
    title: "The Familiar Passage",
    description: "To break the loop, re-engage with a known text.",
    action: "Re-read a familiar passage from a pre-collapse book, focusing on a single word you've never truly noticed before. This grounds your perception in linear progression.",
  },
  "minor time stutter": {
    title: "Rhythmic Re-alignment",
    description: "Re-establish your internal clock with a steady rhythm.",
    action: "Perform a simple, repetitive task like sharpening a blade, mending a tear, or stirring a pot, allowing the rhythm to re-align your internal clock.",
  },
  "echo of forgotten past": {
    title: "Memory Anchor",
    description: "Anchor yourself to the present by creating a new, tangible memory.",
    action: "Find a small, interesting object you've never seen before. Observe it closely, describe it aloud, and place it somewhere new. This creates a fresh anchor in the present.",
  },
  "chronal ripple": {
    title: "Stillness Meditation",
    description: "Calm the ripples by embracing stillness.",
    action: "Find a quiet spot. Close your eyes and focus on your breath for five minutes, allowing the subtle vibrations of time to settle around you.",
  },
  "temporal echo": {
    title: "Echo Reflection",
    description: "Acknowledge the echo, then gently release it.",
    action: "Write down the fleeting thought or image that constitutes the echo. Then, crumple the paper and discard it, symbolizing the release of the temporal resonance.",
  },
  "future premonition fragment": {
    title: "Present Moment Grounding",
    description: "Ground yourself firmly in the 'now' to prevent future bleed-through.",
    action: "Engage all five senses: identify one thing you can see, two things you can hear, three things you can feel, four things you can smell, and five things you can taste (even if it's just the air).",
  },
  "past memory bleed": {
    title: "Historical Re-contextualization",
    description: "Place the past firmly in its historical context.",
    action: "Recall a specific, verifiable historical fact from before the collapse. Focus on its details, reminding yourself of the unchangeable nature of established history.",
  },
  "temporal displacement itch": {
    title: "Spatial Re-orientation",
    description: "Re-orient yourself physically to combat the feeling of displacement.",
    action: "Walk a familiar path backwards for a short distance, or rearrange a small set of objects in your immediate vicinity. This re-establishes your physical presence.",
  },
  "void whisper resonance": {
    title: "Affirmation of Being",
    description: "Counter the void's whispers with a strong affirmation of your existence.",
    action: "Speak aloud three things you are grateful for in this very moment, no matter how small. This reinforces your connection to the present reality.",
  },
  "unsettling stillness": {
    title: "Subtle Movement Activation",
    description: "Break the unsettling stillness with gentle, intentional movement.",
    action: "Perform a series of slow, deliberate stretches or gentle joint rotations. Re-introduce subtle motion to the environment and your body.",
  },
};

export function getHarmonizationRitual(
  anomaly: TemporalAnomaly
): HarmonizationRitual | undefined {
  return harmonizationMap[anomaly];
}

export function listTemporalAnomalies(): TemporalAnomaly[] {
  return Object.keys(harmonizationMap) as TemporalAnomaly[];
}
