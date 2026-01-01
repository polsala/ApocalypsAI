# Nightly Lore Entry Validator

## Summary
This utility ensures the structural and data integrity of ApocalypsAI lore entries by validating them against a strict, predefined TypeScript schema. It helps maintain consistency across the ever-growing chronicles of the apocalypse.

## Whimsical-yet-Useful Aspect
In the chaotic aftermath, maintaining coherent lore is paramount for future historians (or scavengers). This tool acts as a digital scribe, ensuring that every discovered artifact, temporal anomaly, or heroic deed is recorded with impeccable structure, preventing chronological paradoxes or miscategorized horrors.

## Installation
To use this utility, you need Node.js (which includes npm) installed on your system.

1.  Navigate to the `nightly-lore-entry-validator` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

### CLI Usage

To validate a JSON file containing a lore entry:

```bash
# Example: Validate a valid entry
npm start path/to/your/lore-entry.json

# Example: Validate an invalid entry
npm start path/to/your/malformed-entry.json
```

**Example `valid-lore-entry.json`:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "title": "The Whispering Monolith",
  "category": "Anomaly",
  "description": "A large, obsidian monolith discovered in Sector Gamma, emitting faint, indecipherable whispers.",
  "discoveredBy": "Scout Unit 7",
  "discoveryDate": "2077-10-23T14:30:00Z",
  "threatLevel": 4,
  "relatedEntries": ["b2c3d4e5-f6a7-8901-2345-67890abcdef0"]
}
```

### Library Usage

You can also import and use the `validateLoreEntry` function in your own TypeScript/JavaScript projects:

```typescript
import { validateLoreEntry, LoreEntry } from 'nightly-lore-entry-validator'; // Assuming it's published or path-aliased

const myLoreEntry: unknown = {
  id: 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
  title: 'The Whispering Monolith',
  category: 'Anomaly',
  description: 'A large, obsidian monolith discovered in Sector Gamma, emitting faint, indecipherable whispers.',
  discoveredBy: 'Scout Unit 7',
  discoveryDate: '2077-10-23T14:30:00Z',
  threatLevel: 4,
  relatedEntries: ['b2c3d4e5-f6a7-8901-2345-67890abcdef0']
};

const result = validateLoreEntry(myLoreEntry);

if (result.isValid) {
  console.log('Lore entry is valid:', result.data);
} else {
  console.error('Lore entry is invalid:', result.errors);
}
```

## Lore Entry Schema
A `LoreEntry` must conform to the following structure:

```typescript
interface LoreEntry {
  id: string; // A unique UUID for the entry.
  title: string; // The title of the entry (min 3 characters).
  category: "Anomaly" | "Artifact" | "Event" | "Person" | "Location" | "Faction" | "Technology"; // Predefined categories.
  description: string; // A detailed description (min 10 characters).
  discoveredBy?: string; // Optional: Who discovered or reported it.
  discoveryDate?: string; // Optional: ISO 8601 datetime string (e.g., "2077-10-23T14:30:00Z").
  threatLevel?: number; // Optional: An integer from 1 to 5.
  relatedEntries?: string[]; // Optional: Array of UUIDs of related lore entries.
}
```

**Note:** The schema is `strict`, meaning any fields not defined above will cause validation to fail.
