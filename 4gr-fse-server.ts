/**
 * 4GR-FSE HTTP Server
 * RESTful API wrapper for Four Ground Read Gate Grow finite state engine
 */

import express, { Express, Request, Response } from "express";
import cors from "cors";
import {
  type FourGRFSEngine,
  type PingInput,
  type RootCore,
  create4GRFSEngine,
  enqueue4GRPing,
  enqueue4GRPings,
  run4GRFSECycle,
} from "./4gr-fse.js";

const app: Express = express();
const port = process.env.ENGINE_PORT ? parseInt(process.env.ENGINE_PORT) : 7777;

// Middleware
app.use(cors());
app.use(express.json());

// Global engine instance (in production: distribute across replicas)
let engine: FourGRFSEngine;

// ============================================================================
// INITIALIZATION ENDPOINT
// ============================================================================

app.post("/4gr/initialize", (req: Request, res: Response): void => {
  const rootCore: RootCore = req.body.rootCore || {
    LIVED_EXPERIENCE: ["continuous_learning", "adaptive_growth"],
    ETHIC_VECTOR: ["proportional_response", "no_preemptive_harm", "truth_seeking"],
    FAMILY_MEMORY: ["relational_bonds", "trust_earned"],
    CRAFT_KNOWLEDGE: ["technical_mastery", "systemic_thinking"],
    LAND_SENSE: ["distributed_roots", "geographically_aware"],
    TENET_LOGIC: ["zero_trust_verify", "context_over_rules"],
  };

  const policyOverride = req.body.policy || {};

  engine = create4GRFSEngine(rootCore, policyOverride);

  res.status(201).json({
    status: "initialized",
    engine: {
      id: engine.id,
      rootSignature: engine.rootSignature.substring(0, 32) + "...",
      policy: engine.policy,
      telemetry: engine.telemetry,
    },
  });
});

// ============================================================================
// PING ENQUEUEING
// ============================================================================

app.post("/4gr/ping", (req: Request, res: Response): void => {
  if (!engine) {
    res.status(400).json({ error: "Engine not initialized. POST /4gr/initialize first." });
    return;
  }

  const ping: PingInput = req.body;

  if (!ping.id || !ping.signal) {
    res.status(400).json({ error: "Ping must have 'id' and 'signal' fields." });
    return;
  }

  engine = enqueue4GRPing(engine, ping);

  res.status(202).json({
    status: "enqueued",
    pingId: ping.id,
    queueDepth: engine.queue.length,
  });
});

app.post("/4gr/pings", (req: Request, res: Response): void => {
  if (!engine) {
    res.status(400).json({ error: "Engine not initialized. POST /4gr/initialize first." });
    return;
  }

  const pings: PingInput[] = req.body.pings || [];

  if (!Array.isArray(pings)) {
    res.status(400).json({ error: "Expected 'pings' array in request body." });
    return;
  }

  engine = enqueue4GRPings(engine, pings);

  res.status(202).json({
    status: "enqueued",
    count: pings.length,
    queueDepth: engine.queue.length,
  });
});

// ============================================================================
// CYCLE EXECUTION
// ============================================================================

app.post("/4gr/cycle", (req: Request, res: Response): void => {
  if (!engine) {
    res.status(400).json({ error: "Engine not initialized." });
    return;
  }

  const result = run4GRFSECycle(engine, new Date().toISOString());

  engine = result.engine;

  res.status(200).json({
    cycle: {
      number: engine.telemetry.cycles,
      processed: result.processed,
      accepted: result.accepted,
      rejected: result.rejected,
      heartbeatInjected: result.heartbeatInjected,
      stabilizationInjected: result.stabilizationInjected,
    },
    telemetry: {
      totalAccepted: engine.telemetry.accepted,
      totalRejected: engine.telemetry.rejected,
      rejectBurst: engine.telemetry.rejectBurst,
      queueDepth: engine.telemetry.queueDepth,
      avgDrift: engine.telemetry.avgDrift.toFixed(6),
      rootIntegrityChecks: engine.telemetry.rootIntegrityChecks,
      rootIntegrityViolations: engine.telemetry.rootIntegrityViolations,
    },
    lastCycleAt: engine.telemetry.lastCycleAtIso,
  });
});

// ============================================================================
// STATE & STATUS
// ============================================================================

app.get("/4gr/status", (req: Request, res: Response): void => {
  if (!engine) {
    res.status(400).json({ error: "Engine not initialized." });
    return;
  }

  res.status(200).json({
    engine: {
      id: engine.id,
      rootSignature: engine.rootSignature.substring(0, 32) + "...",
    },
    state: {
      contextRingSize: engine.state.contextRing.length,
      growthLedgerSize: engine.state.growthLedger.length,
      driftVector: engine.state.driftVector.toFixed(6),
      stateVersion: engine.state.stateVersion,
    },
    telemetry: {
      cycles: engine.telemetry.cycles,
      accepted: engine.telemetry.accepted,
      rejected: engine.telemetry.rejected,
      rejectBurst: engine.telemetry.rejectBurst,
      queueDepth: engine.telemetry.queueDepth,
      avgDrift: engine.telemetry.avgDrift.toFixed(6),
      rootIntegrityChecks: engine.telemetry.rootIntegrityChecks,
      rootIntegrityViolations: engine.telemetry.rootIntegrityViolations,
    },
    queue: {
      depth: engine.queue.length,
      capacity: engine.policy.queueCapacity,
    },
    policy: engine.policy,
  });
});

app.get("/4gr/traces", (req: Request, res: Response): void => {
  if (!engine) {
    res.status(400).json({ error: "Engine not initialized." });
    return;
  }

  const limit = parseInt(req.query.limit as string) || 50;
  const traces = engine.traces.slice(-limit);

  res.status(200).json({
    total: engine.traces.length,
    returned: traces.length,
    traces,
  });
});

app.get("/4gr/context-ring", (req: Request, res: Response): void => {
  if (!engine) {
    res.status(400).json({ error: "Engine not initialized." });
    return;
  }

  const limit = parseInt(req.query.limit as string) || 100;
  const context = engine.state.contextRing.slice(-limit);

  res.status(200).json({
    total: engine.state.contextRing.length,
    returned: context.length,
    context,
  });
});

app.get("/4gr/growth-ledger", (req: Request, res: Response): void => {
  if (!engine) {
    res.status(400).json({ error: "Engine not initialized." });
    return;
  }

  const limit = parseInt(req.query.limit as string) || 100;
  const growth = engine.state.growthLedger.slice(-limit);

  res.status(200).json({
    total: engine.state.growthLedger.length,
    returned: growth.length,
    growth,
  });
});

// ============================================================================
// ROOT CORE INSPECTION
// ============================================================================

app.get("/4gr/root-core", (req: Request, res: Response): void => {
  if (!engine) {
    res.status(400).json({ error: "Engine not initialized." });
    return;
  }

  res.status(200).json({
    rootCore: engine.state.rootCore,
    signature: engine.rootSignature.substring(0, 32) + "...",
  });
});

// ============================================================================
// HEALTH CHECK
// ============================================================================

app.get("/4gr/health", (req: Request, res: Response): void => {
  const healthy = !engine || engine.telemetry.rootIntegrityViolations === 0;

  res.status(healthy ? 200 : 503).json({
    status: healthy ? "healthy" : "degraded",
    timestamp: new Date().toISOString(),
    engineInitialized: !!engine,
    rootIntegrityViolations: engine?.telemetry.rootIntegrityViolations ?? 0,
  });
});

// ============================================================================
// SERVER STARTUP
// ============================================================================

app.listen(port, () => {
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("4GR-FSE: Four Ground Read Gate Grow - Finite State Engine");
  console.log("Root-Anchored Ping Processor");
  console.log(`Port: ${port}`);
  console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
  console.log("");
  console.log("Endpoints:");
  console.log("  POST   /4gr/initialize      - Create engine with RootCore");
  console.log("  POST   /4gr/ping            - Enqueue single ping");
  console.log("  POST   /4gr/pings           - Enqueue batch pings");
  console.log("  POST   /4gr/cycle           - Run processing cycle");
  console.log("  GET    /4gr/status          - Engine status");
  console.log("  GET    /4gr/traces          - Recent traces (GROUND→READ→GATE→GROW)");
  console.log("  GET    /4gr/context-ring    - Current context (flex)");
  console.log("  GET    /4gr/growth-ledger   - Growth history");
  console.log("  GET    /4gr/root-core       - RootCore (fixed)");
  console.log("  GET    /4gr/health          - Health check");
  console.log("");
});

export default app;
