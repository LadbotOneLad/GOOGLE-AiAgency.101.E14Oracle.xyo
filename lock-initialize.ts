#!/usr/bin/env node
/**
 * Initialize 90-Day Engine Lock
 * 
 * Usage:
 *   npx ts-node lock-initialize.ts
 * 
 * Output:
 *   - .env.lock (environment variables for docker-compose)
 *   - lock-metadata.json (Merkle tree + timestamps)
 *   - k8s-lock-secret.yaml (Kubernetes Secret)
 *   - k8s-lock-configmap.yaml (Kubernetes ConfigMap)
 */

import { createLockAnchor, exportLockAsEnv, exportLockAsYaml } from "./lock-90-day";
import fs from "fs";
import path from "path";

// Mock engine states (in production, these come from running engines)
const engineStates = [
  {
    id: "365",
    port: 365,
    stateHash:
      "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f",
    contextRingSize: 42,
    growthLedgerSize: 128,
    driftVector: 0.021,
    stateVersion: 1,
    parentHash: null,
  },
  {
    id: "777",
    port: 777,
    stateHash:
      "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2",
    contextRingSize: 37,
    growthLedgerSize: 115,
    driftVector: 0.018,
    stateVersion: 1,
    parentHash: null,
  },
  {
    id: "101",
    port: 101,
    stateHash:
      "c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3",
    contextRingSize: 51,
    growthLedgerSize: 142,
    driftVector: 0.024,
    stateVersion: 1,
    parentHash: null,
  },
];

// Add 12 peer engines (1001-1012)
for (let i = 1001; i <= 1012; i++) {
  engineStates.push({
    id: String(i),
    port: i,
    stateHash: Buffer.from(`engine-${i}-state-hash`).toString("hex").padEnd(64, "0"),
    contextRingSize: 40 + Math.floor(Math.random() * 20),
    growthLedgerSize: 120 + Math.floor(Math.random() * 40),
    driftVector: 0.01 + Math.random() * 0.03,
    stateVersion: 1,
    parentHash: null,
  });
}

// Create lock anchor
const lockAnchor = createLockAnchor(
  engineStates,
  new Date().toISOString(),
);

console.log("╔═══════════════════════════════════════════════════════════════╗");
console.log("║              90-DAY ENGINE SYNCHRONIZATION LOCK                ║");
console.log("╚═══════════════════════════════════════════════════════════════╝");
console.log();
console.log(`Lock ID:        ${lockAnchor.lockId}`);
console.log(`Inception:      ${lockAnchor.inceptionTimestampIso}`);
console.log(`Expiry:         ${lockAnchor.expiryTimestampIso}`);
console.log(`Engines:        ${lockAnchor.engineCount}`);
console.log(`Merkle Root:    ${lockAnchor.rootMerkleHash}`);
console.log(`Lock Phrase:    ${lockAnchor.lockPhrase}`);
console.log();
console.log("Wobble Snapshot:");
console.log(`  w_suu (identity):  ${lockAnchor.wobbleSnapshot.w_suu}`);
console.log(`  w_aha (structure): ${lockAnchor.wobbleSnapshot.w_aha}`);
console.log(`  w_rere (flow):     ${lockAnchor.wobbleSnapshot.w_rere}`);
console.log();

// Export .env file
const envContent = Object.entries(exportLockAsEnv(lockAnchor))
  .map(([key, value]) => `${key}=${value}`)
  .join("\n");

const envPath = path.join(process.cwd(), ".env.lock");
fs.writeFileSync(envPath, envContent, "utf8");
console.log(`✅ Exported: ${envPath}`);

// Export YAML
const yamlContent = exportLockAsYaml(lockAnchor);
const yamlPath = path.join(process.cwd(), "lock-metadata.yaml");
fs.writeFileSync(yamlPath, yamlContent, "utf8");
console.log(`✅ Exported: ${yamlPath}`);

// Export JSON metadata
const metadata = {
  anchor: lockAnchor,
  engineStates,
  verifiedAt: new Date().toISOString(),
};
const jsonPath = path.join(process.cwd(), "lock-metadata.json");
fs.writeFileSync(jsonPath, JSON.stringify(metadata, null, 2), "utf8");
console.log(`✅ Exported: ${jsonPath}`);

// Export Kubernetes Secret
const k8sSecret = `apiVersion: v1
kind: Secret
metadata:
  name: engine-lock-90day
  namespace: default
  labels:
    app: te-papa-matihiko
    lock-type: 90day-sync
type: Opaque
stringData:
  lock-id: "${lockAnchor.lockId}"
  lock-inception: "${lockAnchor.inceptionTimestampIso}"
  lock-expiry: "${lockAnchor.expiryTimestampIso}"
  root-merkle-hash: "${lockAnchor.rootMerkleHash}"
  root-core-signature: "${lockAnchor.rootCoreSignature}"
  wobble-snapshot: |
    w_suu: ${lockAnchor.wobbleSnapshot.w_suu}
    w_aha: ${lockAnchor.wobbleSnapshot.w_aha}
    w_rere: ${lockAnchor.wobbleSnapshot.w_rere}
`;

const secretPath = path.join(process.cwd(), "k8s-lock-secret.yaml");
fs.writeFileSync(secretPath, k8sSecret, "utf8");
console.log(`✅ Exported: ${secretPath}`);

// Export Kubernetes ConfigMap
const k8sConfigMap = `apiVersion: v1
kind: ConfigMap
metadata:
  name: engine-lock-metadata
  namespace: default
  labels:
    app: te-papa-matihiko
    lock-type: 90day-sync
data:
  lock-phrase: "${lockAnchor.lockPhrase}"
  engine-count: "${lockAnchor.engineCount}"
  kotahitanja-formula: "H = (1/3)*w_suu + (1/3)*w_aha + (1/3)*w_rere"
  kotahitanja-value: "${((lockAnchor.wobbleSnapshot.w_suu + lockAnchor.wobbleSnapshot.w_aha + lockAnchor.wobbleSnapshot.w_rere) / 3).toFixed(4)}"
  engine-ports: "365,777,101,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012"
  lock-metadata.json: |
${JSON.stringify(metadata, null, 2)
  .split("\n")
  .map((line) => `    ${line}`)
  .join("\n")}
`;

const configMapPath = path.join(process.cwd(), "k8s-lock-configmap.yaml");
fs.writeFileSync(configMapPath, k8sConfigMap, "utf8");
console.log(`✅ Exported: ${configMapPath}`);

console.log();
console.log("Next steps:");
console.log("  1. Source the lock environment: source .env.lock");
console.log("  2. Update docker-compose.yml with LOCK_* variables");
console.log("  3. Deploy to K8s: kubectl apply -f k8s-lock-secret.yaml k8s-lock-configmap.yaml");
console.log("  4. Start engines: docker-compose up -d");
console.log("  5. Verify lock: docker-compose exec <engine> curl http://localhost:PORT/lock/status");
