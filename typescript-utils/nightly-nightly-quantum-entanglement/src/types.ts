export interface EntanglementOptions {
  nodeA: string;
  nodeB: string;
  distance: number;
}

export interface EntanglementReport {
  nodeA: string;
  nodeB: string;
  distance: number;
  bellState: string;
  stateDescription: string;
  fidelity: number;
  coherenceTime: number;
  entangled: boolean;
  timestamp: string;
}
