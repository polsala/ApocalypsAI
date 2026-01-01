import { z } from 'zod';

export const LoreCategorySchema = z.enum(["Anomaly", "Artifact", "Event", "Person", "Location", "Faction", "Technology"]);

export const LoreEntrySchema = z.object({
  id: z.string().uuid("Lore entry ID must be a valid UUID."),
  title: z.string().min(3, "Title must be at least 3 characters long."),
  category: LoreCategorySchema,
  description: z.string().min(10, "Description must be at least 10 characters long."),
  discoveredBy: z.string().optional(),
  discoveryDate: z.string().datetime({ message: "Discovery date must be a valid ISO 8601 datetime string." }).optional(),
  threatLevel: z.number().int().min(1).max(5).optional(),
  relatedEntries: z.array(z.string().uuid("Related entry ID must be a valid UUID.")).optional(),
}).strict("Lore entry contains unexpected fields."); // Strict to prevent extra fields

export type LoreEntry = z.infer<typeof LoreEntrySchema>;
