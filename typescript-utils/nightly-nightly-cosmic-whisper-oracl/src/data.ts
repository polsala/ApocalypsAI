import { WhisperPrompt, WhisperCategory } from './types';

export const WHISPER_PROMPTS: WhisperPrompt[] = [
  { id: "res-1", category: "Resource", prompt: "Seek the shimmering dew-drops beneath the rusted bridge.", actionVerb: "Scavenge", riskLevel: "Low" },
  { id: "res-2", category: "Resource", prompt: "The ancient vending machine hums with forgotten sustenance.", actionVerb: "Investigate", riskLevel: "Medium" },
  { id: "res-3", category: "Resource", prompt: "Harvest the glowing fungi from the abandoned subway tunnels.", actionVerb: "Gather", riskLevel: "High" },
  { id: "shel-1", category: "Shelter", prompt: "Reinforce the eastern wall with salvaged corrugated iron.", actionVerb: "Fortify", riskLevel: "Low" },
  { id: "shel-2", category: "Shelter", prompt: "Explore the collapsed subway tunnel for a new, hidden refuge.", actionVerb: "Relocate", riskLevel: "High" },
  { id: "shel-3", category: "Shelter", prompt: "Patch the roof of your current dwelling with scavenged tarps.", actionVerb: "Repair", riskLevel: "Low" },
  { id: "soc-1", category: "Social", prompt: "Share a story by the flickering barrel fire, fostering camaraderie.", actionVerb: "Connect", riskLevel: "Low" },
  { id: "soc-2", category: "Social", prompt: "Negotiate with the wandering merchant for vital medical supplies.", actionVerb: "Barter", riskLevel: "Medium" },
  { id: "soc-3", category: "Social", prompt: "Send a coded message via the old radio tower, seeking allies.", actionVerb: "Broadcast", riskLevel: "High" },
  { id: "exp-1", category: "Exploration", prompt: "Map the forgotten overgrown botanical garden for rare herbs.", actionVerb: "Survey", riskLevel: "Medium" },
  { id: "exp-2", category: "Exploration", prompt: "Venture into the Silent Peaks, where strange signals emanate.", actionVerb: "Ascend", riskLevel: "High" },
  { id: "exp-3", category: "Exploration", prompt: "Investigate the source of the distant, rhythmic hum.", actionVerb: "Probe", riskLevel: "Unknown" },
  { id: "self-1", category: "Self-Care", prompt: "Meditate on the resilience of the wasteland flora.", actionVerb: "Reflect", riskLevel: "Low" },
  { id: "self-2", category: "Self-Care", prompt: "Repair your worn boots; a journey awaits.", actionVerb: "Mend", riskLevel: "Low" },
  { id: "self-3", category: "Self-Care", prompt: "Find a quiet spot to listen to the wind's ancient song.", actionVerb: "Rest", riskLevel: "Low" },
  { id: "wild-1", category: "Wildcard", prompt: "The void whispers of a forgotten melody; try to hum it.", actionVerb: "Create", riskLevel: "Unknown" },
  { id: "wild-2", category: "Wildcard", prompt: "A lone crow watches; interpret its message.", actionVerb: "Observe", riskLevel: "Unknown" },
  { id: "wild-3", category: "Wildcard", prompt: "Follow the path of the shimmering dust motes.", actionVerb: "Pursue", riskLevel: "Unknown" }
];
