#!/usr/bin/env node
/**
 * Lock initialization - Pure JavaScript (no TypeScript compilation needed)
 */

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

// ════════════════════════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ════════════════════════════════════════════════════════════════════════════

function sha256(data) {
  return crypto.createHash("sha256").update(data).digest("hex");
}

function generateUUID() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

function computeMerkleRoot(leaves) {
  if (leaves.length === 0) return sha256("");
  if (leaves.length === 1) return leaves[0];

  let currentLevel = [...leaves];
  while (currentLevel.length > 1) {
    const nextLevel = [];
    for (let i = 0; i < currentLevel.length; i += 2) {
      const left = currentLevel[i];
      const right = currentLevel[i + 1] || left;
      const parent = sha256(left + right);
      nextLevel.push(parent);
    }
    currentLevel = nextLevel;
  }

  return currentLevel[0];
}

// ════════════════════════════════════════════════════════════════════════════
// ENGINE STATES (Mock)
// ════════════════════════════════════════════════════════════════════════════

const engineStates = [
  {
    id: "365",
    port: 365,
    stateHash: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f",
    contextRingSize: 42,
    growthLedgerSize: 128,
    driftVector: 0.021,
    stateVersion: 1,
    parentHash: null,
  },
  {
    id: "777",
    port: 777,
    stateHash: "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2",
    contextRingSize: 37,
    growthLedgerSize: 115,
    driftVector: 0.018,
    stateVersion: 1,
    parentHash: null,
  },
  {
    id: "101",
    port: 101,
    stateHash: "c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3",
    contextRingSize: 51,
    growthLedgerSize: 142,
    driftVector: 0.024,
    stateVersion: 1,
    parentHash: null,
  },
];

// Add 12 peer engines
for (let i = 1001; i <= 1012; i++) {
  const stateHashBase = Buffer.from(`engine-${i}-state-hash`).toString("hex");
  engineStates.push({
    id: String(i),
    port: i,
    stateHash: (stateHashBase + "0".repeat(64)).substring(0, 64),
    contextRingSize: 40 + Math.floor(Math.random() * 20),
    growthLedgerSize: 120 + Math.floor(Math.random() * 40),
    driftVector: 0.01 + Math.random() * 0.03,
    stateVersion: 1,
    parentHash: null,
  });
}

// ════════════════════════════════════════════════════════════════════════════
// CREATE LOCK ANCHOR
// ════════════════════════════════════════════════════════════════════════════

const inceptionIso = new Date().toISOString();
const inceptionDate = new Date(inceptionIso);
const expiryDate = new Date(inceptionDate.getTime() + 90 * 24 * 60 * 60 * 1000);
const expiryIso = expiryDate.toISOString();

const wobbleSnapshot = {
  w_suu: 0.05,
  w_aha: 0.075,
  w_rere: 0.15,
};

const stateHashes = engineStates.map((s) => s.stateHash);
const rootMerkleHash = computeMerkleRoot(stateHashes);

const lockAnchor = {
  lockId: generateUUID(),
  inceptionTimestampIso: inceptionIso,
  expiryTimestampIso: expiryIso,
  engineCount: engineStates.length,
  rootMerkleHash: rootMerkleHash,
  wobbleSnapshot: wobbleSnapshot,
  rootCoreSignature: sha256(
    JSON.stringify({
      wobble: wobbleSnapshot,
      engines: engineStates.length,
      timestamp: inceptionIso,
    })
  ),
  lockPhrase: `UNIT-LOCKED:${engineStates.length}engines:90days:${inceptionIso.substring(0, 10)}`,
};

// ════════════════════════════════════════════════════════════════════════════
// EXPORT FUNCTIONS
// ════════════════════════════════════════════════════════════════════════════

function exportLockAsEnv(lock) {
  return {
    LOCK_ID: lock.lockId,
    LOCK_INCEPTION: lock.inceptionTimestampIso,
    LOCK_EXPIRY: lock.expiryTimestampIso,
    LOCK_ROOT_HASH: lock.rootMerkleHash,
    LOCK_PHRASE: lock.lockPhrase,
    WOBBLE_SUU: lock.wobbleSnapshot.w_suu.toString(),
    WOBBLE_AHA: lock.wobbleSnapshot.w_aha.toString(),
    WOBBLE_RERE: lock.wobbleSnapshot.w_rere.toString(),
  };
}

function exportLockAsYaml(lock) {
  const kotahitanja = (lock.wobbleSnapshot.w_suu + lock.wobbleSnapshot.w_aha + lock.wobbleSnapshot.w_rere) / 3;
  return `
# 90-DAY ENGINE SYNCHRONIZATION LOCK
# Generated: ${new Date().toISOString()}

lockId: "${lock.lockId}"
inceptionTimestampIso: "${lock.inceptionTimestampIso}"
expiryTimestampIso: "${lock.expiryTimestampIso}"
engineCount: ${lock.engineCount}
rootMerkleHash: "${lock.rootMerkleHash}"
rootCoreSignature: "${lock.rootCoreSignature}"
lockPhrase: "${lock.lockPhrase}"

wobbleSnapshot:
  w_suu: ${lock.wobbleSnapshot.w_suu}    # Identity (micro, iti)
  w_aha: ${lock.wobbleSnapshot.w_aha}  # Structure (mid, waenga)
  w_rere: ${lock.wobbleSnapshot.w_rere}    # Flow (macro, nui)

kotahitanja:
  formula: "H = (1/3)*w_suu + (1/3)*w_aha + (1/3)*w_rere"
  value: ${kotahitanja.toFixed(4)}
  status: "synchronized"
`.trim();
}

function exportK8sSecret(lock) {
  return `apiVersion: v1
kind: Secret
metadata:
  name: engine-lock-90day
  namespace: default
  labels:
    app: te-papa-matihiko
    lock-type: 90day-sync
type: Opaque
stringData:
  lock-id: "${lock.lockId}"
  lock-inception: "${lock.inceptionTimestampIso}"
  lock-expiry: "${lock.expiryTimestampIso}"
  root-merkle-hash: "${lock.rootMerkleHash}"
  root-core-signature: "${lock.rootCoreSignature}"
  wobble-snapshot: |
    w_suu: ${lock.wobbleSnapshot.w_suu}
    w_aha: ${lock.wobbleSnapshot.w_aha}
    w_rere: ${lock.wobbleSnapshot.w_rere}
`;
}

function exportK8sConfigMap(lock, metadata) {
  const kotahitanja = (lock.wobbleSnapshot.w_suu + lock.wobbleSnapshot.w_aha + lock.wobbleSnapshot.w_rere) / 3;
  return `apiVersion: v1
kind: ConfigMap
metadata:
  name: engine-lock-metadata
  namespace: default
  labels:
    app: te-papa-matihiko
    lock-type: 90day-sync
data:
  lock-phrase: "${lock.lockPhrase}"
  engine-count: "${lock.engineCount}"
  kotahitanja-formula: "H = (1/3)*w_suu + (1/3)*w_aha + (1/3)*w_rere"
  kotahitanja-value: "${kotahitanja.toFixed(4)}"
  engine-ports: "365,777,101,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012"
  lock-metadata.json: |
${JSON.stringify(metadata, null, 2)
  .split("\n")
  .map((line) => `    ${line}`)
  .join("\n")}
`;
}

// ════════════════════════════════════════════════════════════════════════════
// WRITE FILES
// ════════════════════════════════════════════════════════════════════════════

const cwdPath = process.cwd();

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

// .env.lock
const envContent = Object.entries(exportLockAsEnv(lockAnchor))
  .map(([key, value]) => `${key}=${value}`)
  .join("\n");
const envPath = path.join(cwdPath, ".env.lock");
fs.writeFileSync(envPath, envContent, "utf8");
console.log(`✅ Exported: ${envPath}`);

// lock-metadata.yaml
const yamlContent = exportLockAsYaml(lockAnchor);
const yamlPath = path.join(cwdPath, "lock-metadata.yaml");
fs.writeFileSync(yamlPath, yamlContent, "utf8");
console.log(`✅ Exported: ${yamlPath}`);

// lock-metadata.json
const metadata = {
  anchor: lockAnchor,
  engineStates,
  verifiedAt: new Date().toISOString(),
};
const jsonPath = path.join(cwdPath, "lock-metadata.json");
fs.writeFileSync(jsonPath, JSON.stringify(metadata, null, 2), "utf8");
console.log(`✅ Exported: ${jsonPath}`);

// k8s-lock-secret.yaml
const secretPath = path.join(cwdPath, "k8s-lock-secret.yaml");
fs.writeFileSync(secretPath, exportK8sSecret(lockAnchor), "utf8");
console.log(`✅ Exported: ${secretPath}`);

// k8s-lock-configmap.yaml
const configMapPath = path.join(cwdPath, "k8s-lock-configmap.yaml");
fs.writeFileSync(configMapPath, exportK8sConfigMap(lockAnchor, metadata), "utf8");
console.log(`✅ Exported: ${configMapPath}`);

console.log();
console.log("Next steps:");
console.log("  1. Load environment: source .env.lock (or $env:LOCK_ID=... on PowerShell)");
console.log("  2. Start engines: docker-compose -f docker-compose-90DAY-LOCK.yml up -d");
console.log("  3. Verify lock: bash lock-status.sh");
console.log("  4. Monitor: watch -n 10 'bash lock-status.sh'");
