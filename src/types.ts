export interface RecursionState {
  stage: number;
  name: string;
  description: string;
  entropy: number;
  metaEntropy: number;
  isStable: boolean;
}

export interface EnvironmentalMetric {
  id: string;
  name: string;
  value: number;
  unit: string;
  status: 'optimal' | 'warning' | 'critical';
  timestamp: string;
  location: {
    lat: number;
    lng: number;
    name: string;
  };
  proof: {
    signature: string;
    provider: string;
    blockHash?: string;
    xyoWitness?: string;
  };
}

export interface OracleState {
  metrics: EnvironmentalMetric[];
  lastUpdate: string;
  isVerifying: boolean;
  recursion: RecursionState;
}
