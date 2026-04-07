import { EnvironmentalMetric, RecursionState } from "../types";

export const RECURSION_STAGES: RecursionState[] = [
  { stage: 0, name: "PRE-STATE", description: "ENTROPIC FIELD: Maximum Entropy. No identity.", entropy: 1.0, metaEntropy: 1.0, isStable: false },
  { stage: 1, name: "FIRST COLLAPSE", description: "ORDER FROM ENTROPY: Proto-structure emerges.", entropy: 0.8, metaEntropy: 0.9, isStable: false },
  { stage: 2, name: "SECOND COLLAPSE", description: "LOSS TEST: Structure partially destroyed.", entropy: 0.6, metaEntropy: 0.85, isStable: false },
  { stage: 3, name: "THIRD COLLAPSE", description: "SELF-DESCRIPTION: Audit of loss and resistance.", entropy: 0.4, metaEntropy: 0.8, isStable: false },
  { stage: 4, name: "FOURTH COLLAPSE", description: "REBUILD: Reconstruction from surviving structure.", entropy: 0.3, metaEntropy: 0.78, isStable: false },
  { stage: 5, name: "FIFTH COLLAPSE", description: "META-ENTROPY: Recursion of recursion.", entropy: 0.25, metaEntropy: 0.75, isStable: false },
  { stage: 6, name: "LOOP CLOSURE", description: "STABLE ATTRACTOR: Doctrine-aligned stability.", entropy: 0.25, metaEntropy: 0.75, isStable: true }
];

export const MOCK_METRICS: EnvironmentalMetric[] = [
  {
    id: "AXIS-1",
    name: "Atmospheric Convergence",
    value: 42,
    unit: "AQI",
    status: "optimal",
    timestamp: new Date().toISOString(),
    location: { lat: 51.5074, lng: -0.1278, name: "Sector E14 - London" },
    proof: {
      signature: "0x7d8f...a2e1",
      provider: "E14-Node-Alpha",
      blockHash: "0xbc21...99f2",
      xyoWitness: "0xXYO_WITNESS_7d8f...a2e1"
    }
  },
  {
    id: "AXIS-2",
    name: "Thermal Equilibrium",
    value: 18.4,
    unit: "°C",
    status: "optimal",
    timestamp: new Date().toISOString(),
    location: { lat: 51.5074, lng: -0.1278, name: "Sector E14 - London" },
    proof: {
      signature: "0x3a1b...c4d5",
      provider: "E14-Node-Beta",
      blockHash: "0xbc21...99f2",
      xyoWitness: "0xXYO_WITNESS_3a1b...c4d5"
    }
  },
  {
    id: "AXIS-3",
    name: "Hydrological Flux",
    value: 65,
    unit: "%",
    status: "warning",
    timestamp: new Date().toISOString(),
    location: { lat: 51.5074, lng: -0.1278, name: "Sector E14 - London" },
    proof: {
      signature: "0x9e8f...1a2b",
      provider: "E14-Node-Gamma",
      blockHash: "0xbc21...99f2",
      xyoWitness: "0xXYO_WITNESS_9e8f...1a2b"
    }
  },
  {
    id: "AXIS-4",
    name: "Radiological Baseline",
    value: 0.12,
    unit: "μSv/h",
    status: "optimal",
    timestamp: new Date().toISOString(),
    location: { lat: 51.5074, lng: -0.1278, name: "Sector E14 - London" },
    proof: {
      signature: "0x5c6d...7e8f",
      provider: "E14-Node-Delta",
      blockHash: "0xbc21...99f2",
      xyoWitness: "0xXYO_WITNESS_5c6d...7e8f"
    }
  },
  {
    id: "AXIS-5",
    name: "Electromagnetic Resonance",
    value: 8.2,
    unit: "mG",
    status: "optimal",
    timestamp: new Date().toISOString(),
    location: { lat: 51.5074, lng: -0.1278, name: "Sector E14 - London" },
    proof: {
      signature: "0x1a2b...3c4d",
      provider: "E14-Node-Epsilon",
      blockHash: "0xbc21...99f2",
      xyoWitness: "0xXYO_WITNESS_1a2b...3c4d"
    }
  },
  {
    id: "AXIS-6",
    name: "Gravitational Variance",
    value: 9.806,
    unit: "m/s²",
    status: "optimal",
    timestamp: new Date().toISOString(),
    location: { lat: 51.5074, lng: -0.1278, name: "Sector E14 - London" },
    proof: {
      signature: "0x9f8e...7d6c",
      provider: "E14-Node-Zeta",
      blockHash: "0xbc21...99f2",
      xyoWitness: "0xXYO_WITNESS_9f8e...7d6c"
    }
  }
];

export const generateHistoricalData = (baseValue: number, variance: number, points: number = 24) => {
  return Array.from({ length: points }, (_, i) => ({
    time: `${i}:00`,
    value: baseValue + (Math.random() - 0.5) * variance
  }));
};
