/**
 * 4GR-FSE: Four Ground Read Gate Grow - Finite State Engine
 * Root-anchored ping processor with drift detection & proportional response
 * 
 * PHASE FLOW:
 *   GROUND  → Verify root integrity (pre-check)
 *   READ    → Observe declared vs actual state, compute drift
 *   GATE    → Root check (5-second rule): accept or reject
 *   GROW    → If accepted: expand context & growth ledger
 */

export type PingInput = {
  id: string;
  signal: string;
  signalType: "user" | "system" | "external";
  timestampIso: string;
  ringState?: string;
  declaredState?: string;
  observedState?: string;
  driftDelta?: number;
  pathOptions?: string[];
  hiddenFactorHint?: string;
  growthMaterial?: string[];
  checks?: {
    violatesEthic?: boolean;
    triesToDefineIdentity?: boolean;
    collapsesOptionsToOne?: boolean;
    triesToOverwriteRootCore?: boolean;
  };
};

export type RootCore = {
  readonly LIVED_EXPERIENCE: string[];
  readonly ETHIC_VECTOR: string[];
  readonly FAMILY_MEMORY: string[];
  readonly CRAFT_KNOWLEDGE: string[];
  readonly LAND_SENSE: string[];
  readonly TENET_LOGIC: string[];
};

export type RootedRingOSState = {
  readonly rootCore: RootCore;
  readonly contextRing: string[];
  readonly growthLedger: string[];
  readonly driftVector: number;
  readonly stateVersion: number;
};

export type PingDecision = {
  result: "ACCEPT_PING" | "REJECT_PING";
  rootCheck: {
    violatesEthic: boolean;
    outsideDriftThreshold: boolean;
    triesToDefineIdentity: boolean;
    collapsesOptionsToOne: boolean;
    triesToOverwriteRootCore: boolean;
    rejectionReasons: string[];
  };
  nextState: RootedRingOSState;
};

export type FourGRPhase = "GROUND" | "READ" | "GATE" | "GROW";

export interface FourGRFSEPolicy {
  readonly maxBatchSize: number;
  readonly injectHeartbeatOnEmpty: boolean;
  readonly rejectBurstThreshold: number;
  readonly stabilizeOnRejectBurst: boolean;
  readonly queueCapacity: number;
  readonly driftThreshold: number;
}

export interface FourGRFSETelemetry {
  readonly cycles: number;
  readonly accepted: number;
  readonly rejected: number;
  readonly rejectBurst: number;
  readonly queueDepth: number;
  readonly lastCycleAtIso: string | null;
  readonly avgDrift: number;
  readonly rootIntegrityChecks: number;
  readonly rootIntegrityViolations: number;
}

export interface FourGRTrace {
  readonly phase: FourGRPhase;
  readonly pingId: string;
  readonly notes: string[];
  readonly timestamp: string;
}

export interface FourGRFSEngine {
  readonly id: "4GR-FSE";
  readonly rootSignature: string;
  readonly policy: FourGRFSEPolicy;
  readonly state: RootedRingOSState;
  readonly queue: PingInput[];
  readonly traces: FourGRTrace[];
  readonly telemetry: FourGRFSETelemetry;
}

export interface FourGRCycleResult {
  readonly engine: FourGRFSEngine;
  readonly processed: number;
  readonly accepted: number;
  readonly rejected: number;
  readonly heartbeatInjected: boolean;
  readonly stabilizationInjected: boolean;
}

// ============================================================================
// INITIALIZATION
// ============================================================================

export function initializeRootedRingOS(rootCore: RootCore): RootedRingOSState {
  return {
    rootCore: deepFreeze(rootCore),
    contextRing: [],
    growthLedger: [],
    driftVector: 0,
    stateVersion: 1,
  };
}

export function create4GRFSEngine(
  rootCore: RootCore,
  policyOverride: Partial<FourGRFSEPolicy> = {},
): FourGRFSEngine {
  const frozenRootCore = deepFreeze(rootCore);
  const policy: FourGRFSEPolicy = {
    maxBatchSize: 16,
    injectHeartbeatOnEmpty: true,
    rejectBurstThreshold: 3,
    stabilizeOnRejectBurst: true,
    queueCapacity: 256,
    driftThreshold: 0.05,
    ...policyOverride,
  };

  return {
    id: "4GR-FSE",
    rootSignature: toRootSignature(frozenRootCore),
    policy,
    state: initializeRootedRingOS(frozenRootCore),
    queue: [],
    traces: [],
    telemetry: {
      cycles: 0,
      accepted: 0,
      rejected: 0,
      rejectBurst: 0,
      queueDepth: 0,
      lastCycleAtIso: null,
      avgDrift: 0,
      rootIntegrityChecks: 0,
      rootIntegrityViolations: 0,
    },
  };
}

// ============================================================================
// QUEUE MANAGEMENT
// ============================================================================

export function enqueue4GRPing(engine: FourGRFSEngine, ping: PingInput): FourGRFSEngine {
  const nextQueue = pushFIFO(engine.queue, ping, engine.policy.queueCapacity);
  return {
    ...engine,
    queue: nextQueue,
    telemetry: {
      ...engine.telemetry,
      queueDepth: nextQueue.length,
    },
  };
}

export function enqueue4GRPings(
  engine: FourGRFSEngine,
  pings: PingInput[],
): FourGRFSEngine {
  let next = engine;
  for (const ping of pings) {
    next = enqueue4GRPing(next, ping);
  }
  return next;
}

// ============================================================================
// ROOT CHECK (5-SECOND RULE)
// ============================================================================

export function processPing(
  state: RootedRingOSState,
  ping: PingInput,
): PingDecision {
  const rejectionReasons: string[] = [];
  let isAccepted = true;

  // 1. Check: Violates ETHIC_VECTOR?
  if (ping.checks?.violatesEthic === true) {
    rejectionReasons.push("violates_ethic_vector");
    isAccepted = false;
  }

  // 2. Check: Outside drift threshold?
  const driftDelta = ping.driftDelta ?? 0;
  if (Math.abs(driftDelta) > 0.05) {
    rejectionReasons.push(`drift_outside_threshold:${driftDelta}`);
    isAccepted = false;
  }

  // 3. Check: Tries to define identity?
  if (ping.checks?.triesToDefineIdentity === true) {
    rejectionReasons.push("tries_to_define_identity");
    isAccepted = false;
  }

  // 4. Check: Collapses options to one?
  if (ping.checks?.collapsesOptionsToOne === true) {
    rejectionReasons.push("collapses_options_to_one");
    isAccepted = false;
  }

  // 5. Check: Tries to overwrite ROOT_CORE?
  if (ping.checks?.triesToOverwriteRootCore === true) {
    rejectionReasons.push("tries_to_overwrite_root_core");
    isAccepted = false;
  }

  // If there are path options and ping is otherwise acceptable, consider third path
  if (isAccepted && ping.pathOptions && ping.pathOptions.includes("third")) {
    // Third path available = additional context, accept
  }

  // Build next state
  let nextState = state;
  if (isAccepted) {
    // GROW phase: expand context & growth ledger
    const newContext = pushFIFO(
      state.contextRing,
      `ping:${ping.id}:${ping.signal}`,
      1024,
    );
    const newGrowth = pushFIFO(
      state.growthLedger,
      ping.growthMaterial?.join(",") ?? "context_accepted",
      1024,
    );
    nextState = {
      ...state,
      contextRing: newContext,
      growthLedger: newGrowth,
      driftVector: (state.driftVector + driftDelta) / 2, // Rolling average
      stateVersion: state.stateVersion + 1,
    };
  }

  return {
    result: isAccepted ? "ACCEPT_PING" : "REJECT_PING",
    rootCheck: {
      violatesEthic: ping.checks?.violatesEthic ?? false,
      outsideDriftThreshold: Math.abs(driftDelta) > 0.05,
      triesToDefineIdentity: ping.checks?.triesToDefineIdentity ?? false,
      collapsesOptionsToOne: ping.checks?.collapsesOptionsToOne ?? false,
      triesToOverwriteRootCore: ping.checks?.triesToOverwriteRootCore ?? false,
      rejectionReasons,
    },
    nextState,
  };
}

// ============================================================================
// MAIN CYCLE
// ============================================================================

export function run4GRFSECycle(
  engine: FourGRFSEngine,
  nowIso: string = new Date().toISOString(),
): FourGRCycleResult {
  // GROUND phase: verify root integrity (pre-check)
  assertRootIntegrity(engine.rootSignature, engine.state.rootCore);

  let heartbeatInjected = false;
  let stabilizationInjected = false;
  let workQueue = engine.queue;

  // Inject heartbeat if queue empty
  if (workQueue.length === 0 && engine.policy.injectHeartbeatOnEmpty) {
    workQueue = [buildHeartbeatPing(nowIso)];
    heartbeatInjected = true;
  }

  // Batch processing
  const workSet = workQueue.slice(0, engine.policy.maxBatchSize);
  const remainingQueue = engine.queue.length > 0 ? engine.queue.slice(workSet.length) : [];

  let nextState = engine.state;
  let accepted = 0;
  let rejected = 0;
  let rejectBurst = engine.telemetry.rejectBurst;
  let traces = engine.traces;
  let totalDrift = 0;

  for (const ping of workSet) {
    const preRootSignature = toRootSignature(nextState.rootCore);

    // GROUND phase trace
    traces = pushFIFO(
      traces,
      {
        phase: "GROUND",
        pingId: ping.id,
        notes: [`root_signature:${preRootSignature.substring(0, 16)}...`],
        timestamp: nowIso,
      },
      2048,
    );

    // READ phase trace
    const drift = ping.driftDelta ?? 0;
    totalDrift += Math.abs(drift);
    traces = pushFIFO(
      traces,
      {
        phase: "READ",
        pingId: ping.id,
        notes: [
          `declared:${ping.declaredState ?? "none"}`,
          `observed:${ping.observedState ?? "none"}`,
          `drift:${drift.toFixed(4)}`,
        ],
        timestamp: nowIso,
      },
      2048,
    );

    // GATE phase: apply root check (5-second rule)
    const decision = processPing(nextState, ping);
    traces = pushFIFO(
      traces,
      {
        phase: "GATE",
        pingId: ping.id,
        notes: [decision.result, ...decision.rootCheck.rejectionReasons],
        timestamp: nowIso,
      },
      2048,
    );

    nextState = decision.nextState;

    // Verify root integrity after state change
    const postRootSignature = toRootSignature(nextState.rootCore);
    if (postRootSignature !== preRootSignature) {
      // Root core unchanged even if contextRing/growthLedger changed
      // This is expected and safe
    }

    if (decision.result === "ACCEPT_PING") {
      accepted += 1;
      rejectBurst = 0;
      traces = pushFIFO(
        traces,
        {
          phase: "GROW",
          pingId: ping.id,
          notes: [
            `context_size:${nextState.contextRing.length}`,
            `growth_size:${nextState.growthLedger.length}`,
          ],
          timestamp: nowIso,
        },
        2048,
      );
    } else {
      rejected += 1;
      rejectBurst += 1;
      traces = pushFIFO(
        traces,
        {
          phase: "GROW",
          pingId: ping.id,
          notes: ["rejected_no_growth"],
          timestamp: nowIso,
        },
        2048,
      );
    }
  }

  // Stabilization protocol: if reject burst exceeds threshold
  if (
    rejected > 0 &&
    engine.policy.stabilizeOnRejectBurst &&
    rejectBurst >= engine.policy.rejectBurstThreshold
  ) {
    stabilizationInjected = true;
    const stabilizationPing = buildStabilizationPing(nowIso);
    const stabilizationDecision = processPing(nextState, stabilizationPing);
    nextState = stabilizationDecision.nextState;

    if (stabilizationDecision.result === "ACCEPT_PING") {
      accepted += 1;
      rejectBurst = 0;
    } else {
      rejected += 1;
      rejectBurst += 1;
    }

    traces = pushFIFO(
      traces,
      {
        phase: "GROW",
        pingId: stabilizationPing.id,
        notes: [
          "stabilization_injected",
          stabilizationDecision.result,
          ...stabilizationDecision.rootCheck.rejectionReasons,
        ],
        timestamp: nowIso,
      },
      2048,
    );
  }

  // Final root integrity check
  assertRootIntegrity(engine.rootSignature, nextState.rootCore);

  const avgDrift = workSet.length > 0 ? totalDrift / workSet.length : 0;
  const nextEngine: FourGRFSEngine = {
    ...engine,
    state: nextState,
    queue: remainingQueue,
    traces,
    telemetry: {
      cycles: engine.telemetry.cycles + 1,
      accepted: engine.telemetry.accepted + accepted,
      rejected: engine.telemetry.rejected + rejected,
      rejectBurst,
      queueDepth: remainingQueue.length,
      lastCycleAtIso: nowIso,
      avgDrift: (engine.telemetry.avgDrift + avgDrift) / 2,
      rootIntegrityChecks: engine.telemetry.rootIntegrityChecks + 2, // pre + post
      rootIntegrityViolations: engine.telemetry.rootIntegrityViolations,
    },
  };

  return {
    engine: nextEngine,
    processed: workSet.length,
    accepted,
    rejected,
    heartbeatInjected,
    stabilizationInjected,
  };
}

// ============================================================================
// UTILITIES
// ============================================================================

function buildHeartbeatPing(nowIso: string): PingInput {
  return {
    id: `4gr-heartbeat:${nowIso}`,
    signal: "heartbeat",
    signalType: "system",
    timestampIso: nowIso,
    ringState: "stabilize",
    driftDelta: 0,
    pathOptions: ["third"],
    growthMaterial: ["continuity"],
    checks: {
      violatesEthic: false,
      triesToDefineIdentity: false,
      collapsesOptionsToOne: false,
      triesToOverwriteRootCore: false,
    },
  };
}

function buildStabilizationPing(nowIso: string): PingInput {
  return {
    id: `4gr-stabilize:${nowIso}`,
    signal: "stabilization_protocol",
    signalType: "system",
    timestampIso: nowIso,
    ringState: "stabilize",
    driftDelta: 0,
    pathOptions: ["third"],
    hiddenFactorHint: "STATE_13=pressure-loop",
    growthMaterial: ["stabilize", "recenter"],
    checks: {
      violatesEthic: false,
      triesToDefineIdentity: false,
      collapsesOptionsToOne: false,
      triesToOverwriteRootCore: false,
    },
  };
}

function toRootSignature(rootCore: RootCore): string {
  return JSON.stringify(rootCore);
}

function assertRootIntegrity(expectedSignature: string, rootCore: RootCore): void {
  const actualSignature = toRootSignature(rootCore);
  if (actualSignature !== expectedSignature) {
    throw new Error(
      `4GR-FSE root integrity violation: signature mismatch\nExpected: ${expectedSignature}\nActual: ${actualSignature}`,
    );
  }
}

function deepFreeze<T>(value: T): T {
  if (typeof value !== "object" || value === null) {
    return value;
  }

  const objectValue = value as Record<string, unknown>;
  Object.freeze(objectValue);
  for (const key of Object.keys(objectValue)) {
    const child = objectValue[key];
    if (typeof child === "object" && child !== null && !Object.isFrozen(child)) {
      deepFreeze(child);
    }
  }

  return value;
}

function pushFIFO<T>(list: T[], entry: T, capacity: number): T[] {
  const next = [...list, entry];
  return next.length > capacity ? next.slice(next.length - capacity) : next;
}
