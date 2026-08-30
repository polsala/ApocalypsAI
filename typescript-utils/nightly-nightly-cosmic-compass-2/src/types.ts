export interface CelestialBody {
  path: string;
  name: string;
  type: 'file' | 'directory';
  content?: string; // Optional, for future content search capabilities
}

export interface CosmicAtlas {
  [relativePath: string]: CelestialBody;
}

export interface SearchResult {
  celestialBody: CelestialBody;
  matches: string[]; // Lines or snippets where keyword was found (currently just notes where keyword was found)
}
