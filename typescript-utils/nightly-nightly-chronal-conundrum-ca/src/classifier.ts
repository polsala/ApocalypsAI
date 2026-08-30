import { ConundrumClassification, ConundrumCategory } from './types';

export function classifyConundrum(description: string): ConundrumClassification {
  const lowerDesc = description.toLowerCase();

  // Rules for classification based on keywords
  if (lowerDesc.includes("time") || lowerDesc.includes("yesterday") || lowerDesc.includes("tomorrow") || lowerDesc.includes("loop") || lowerDesc.includes("past") || lowerDesc.includes("future") || lowerDesc.includes("clock") || lowerDesc.includes("moment") || lowerDesc.includes("chronometer")) {
    return {
      category: "Temporal Ripple",
      action: "Check your chronometer, then have a calming cup of tea (or whatever liquid isn't currently a newt).",
      confidence: 0.85,
    };
  }

  if (lowerDesc.includes("coffee") || lowerDesc.includes("cat") || lowerDesc.includes("dog") || lowerDesc.includes("object") || lowerDesc.includes("thing") || lowerDesc.includes("disappeared") || lowerDesc.includes("appeared") || lowerDesc.includes("changed") || lowerDesc.includes("reality") || lowerDesc.includes("glitch") || lowerDesc.includes("newt") || lowerDesc.includes("cheese")) {
    return {
      category: "Reality Glitch",
      action: "Document the anomaly with a sketch or a very confused selfie. Avoid direct eye contact if it starts talking.",
      confidence: 0.90,
    };
  }

  if (lowerDesc.includes("exist") || lowerDesc.includes("meaning") || lowerDesc.includes("purpose") || lowerDesc.includes("dream") || lowerDesc.includes("self") || lowerDesc.includes("void") || lowerDesc.includes("consciousness") || lowerDesc.includes("sentient") || lowerDesc.includes("philosophical")) {
    return {
      category: "Existential Echo",
      action: "Ponder the implications, then distract yourself with a truly terrible pun. Laughter is the best defense against cosmic dread.",
      confidence: 0.75,
    };
  }

  if (lowerDesc.includes("banana") || lowerDesc.includes("clown") || lowerDesc.includes("singing") || lowerDesc.includes("dance") || lowerDesc.includes("absurd") || lowerDesc.includes("silly") || lowerDesc.includes("joke") || lowerDesc.includes("giggle") || lowerDesc.includes("laughter")) {
    return {
      category: "Cosmic Joke",
      action: "Appreciate the absurdity. The universe has a strange sense of humor. Maybe join in?",
      confidence: 0.95,
    };
  }

  return {
    category: "Unknown Anomaly",
    action: "Proceed with extreme caution, or just ignore it until it goes away. Some things are best left un-categorized.",
    confidence: 0.50,
  };
}
