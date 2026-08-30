export type Scarcity = 'common' | 'uncommon' | 'rare' | 'legendary';
export type Utility = 'essential' | 'useful' | 'archive' | 'ephemeral';

export interface DigitalItem {
  id: string;
  name: string;
  type: 'file' | 'url' | 'text';
  pathOrContent: string;
  scarcity: Scarcity;
  utility: Utility;
  addedAt: string; // ISO string
}
