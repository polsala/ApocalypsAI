import { TemporalEcho, EchoCategory, EchoRule } from './types';

const echoRules: EchoRule[] = [
  {
    keywords: ["lag", "delay", "stutter", "hiccup", "slow"],
    category: "Minor Glitch",
    protocol: "Recalibrate Chronometer: A brief moment of stillness can realign minor temporal discrepancies. Perhaps a cup of 'Temporal Tea'?"
  },
  {
    keywords: ["deja vu", "echo", "flicker", "loop", "repeat", "recurrent"],
    category: "Chronal Ripple",
    protocol: "Harmonize Resonance: Embrace the ripple. Sometimes, a gentle hum or a repetitive task can smooth out the temporal fabric. Try humming the 'Song of Infinite Loops'."
  },
  {
    keywords: ["empty", "hollow", "silence", "absence", "void", "nothingness"],
    category: "Void Whisper",
    protocol: "Amplify Affirmation: Fill the void with positive resonance. 'I am present. I am whole. The void is merely a canvas for new beginnings.' Repeat thrice."
  },
  {
    keywords: ["paradox", "shift", "warp", "discrepancy", "unusual", "anomaly", "out of sync"],
    category: "Temporal Anomaly",
    protocol: "Consult the Oracle of Now: This requires deeper introspection. Seek the wisdom of the present moment. 'What is truly happening, right here, right now?'"
  }
];

const defaultEcho: Omit<TemporalEcho, 'message'> = {
  category: "Unknown Echo",
  stabilizationProtocol: "Observe and Document: Not all echoes reveal their secrets immediately. Log this event for future analysis. 'The universe is full of surprises. I am ready to learn.'"
};

export function triageTemporalEcho(echoMessage: string): TemporalEcho {
  const lowerCaseMessage = echoMessage.toLowerCase();

  for (const rule of echoRules) {
    if (rule.keywords.some(keyword => lowerCaseMessage.includes(keyword))) {
      return {
        message: echoMessage,
        category: rule.category,
        stabilizationProtocol: rule.protocol
      };
    }
  }

  return {
    message: echoMessage,
    ...defaultEcho
  };
}
