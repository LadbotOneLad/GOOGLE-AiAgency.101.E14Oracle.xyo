-- PostgreSQL Schema for Atmospheric Truth Layer
-- Architect: AiAgency101
-- Stores tiles, witness ledger, invariants, and audit trail

-- ============================================================================
-- TILES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS tiles (
    id BIGSERIAL PRIMARY KEY,
    tile_id VARCHAR UNIQUE NOT NULL,
    satellite_source VARCHAR NOT NULL,
    region VARCHAR NOT NULL,
    band VARCHAR NOT NULL,
    latitude NUMERIC(10, 6),
    longitude NUMERIC(10, 6),
    pixel_hash VARCHAR NOT NULL,
    metadata_hash VARCHAR NOT NULL,
    integrity_hash VARCHAR NOT NULL UNIQUE,
    timestamp TIMESTAMPTZ NOT NULL,
    consensus_k_value NUMERIC(5, 4),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    INDEX idx_timestamp (timestamp),
    INDEX idx_satellite (satellite_source),
    INDEX idx_integrity_hash (integrity_hash)
);

-- ============================================================================
-- INVARIANTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS invariants (
    id BIGSERIAL PRIMARY KEY,
    tile_id BIGINT NOT NULL REFERENCES tiles(id) ON DELETE CASCADE,
    invariant_expression VARCHAR NOT NULL,
    invariant_value NUMERIC(20, 10),
    invariant_proof TEXT,
    immutable_certificate VARCHAR NOT NULL UNIQUE,
    timestamp TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    INDEX idx_tile_id (tile_id),
    INDEX idx_certificate (immutable_certificate)
);

-- ============================================================================
-- WITNESS LEDGER TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS witness_ledger (
    id BIGSERIAL PRIMARY KEY,
    tile_id BIGINT NOT NULL REFERENCES tiles(id) ON DELETE CASCADE,
    witness_node VARCHAR NOT NULL,
    observation_timestamp TIMESTAMPTZ NOT NULL,
    witness_signature VARCHAR NOT NULL,
    rfc3161_timestamp VARCHAR,
    ledger_position BIGINT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    INDEX idx_tile_id (tile_id),
    INDEX idx_ledger_position (ledger_position)
);

-- ============================================================================
-- WITNESS INVARIANTS TABLE (Link tile invariant + witness)
-- ============================================================================

CREATE TABLE IF NOT EXISTS witness_invariants (
    id BIGSERIAL PRIMARY KEY,
    tile_id BIGINT NOT NULL REFERENCES tiles(id) ON DELETE CASCADE,
    invariant_id BIGINT NOT NULL REFERENCES invariants(id) ON DELETE CASCADE,
    witness_id BIGINT NOT NULL REFERENCES witness_ledger(id) ON DELETE CASCADE,
    invariant_relation VARCHAR NOT NULL,
    combined_hash VARCHAR NOT NULL UNIQUE,
    timestamp TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    INDEX idx_tile_id (tile_id),
    INDEX idx_combined_hash (combined_hash)
);

-- ============================================================================
-- CONSENSUS EVENTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS consensus_events (
    id BIGSERIAL PRIMARY KEY,
    tile_id BIGINT REFERENCES tiles(id) ON DELETE SET NULL,
    event_type VARCHAR NOT NULL,  -- PROPOSE, PREPARE, COMMIT, EXECUTE
    engine_id INTEGER NOT NULL,   -- E01-E14
    k_value_before NUMERIC(5, 4),
    k_value_after NUMERIC(5, 4),
    state_vector JSON,
    decision_result VARCHAR,       -- ACCEPTED, REJECTED, RETRY
    created_at TIMESTAMPTZ DEFAULT NOW(),
    INDEX idx_tile_id (tile_id),
    INDEX idx_timestamp (created_at)
);

-- ============================================================================
-- FIREWALL DECISIONS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS firewall_decisions (
    id BIGSERIAL PRIMARY KEY,
    tile_id BIGINT REFERENCES tiles(id) ON DELETE SET NULL,
    proposal JSON NOT NULL,
    k_value NUMERIC(5, 4),
    firewall_decision VARCHAR NOT NULL,  -- ALLOW, REJECT
    approved BOOLEAN,
    rejection_rate NUMERIC(5, 4),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    INDEX idx_tile_id (tile_id),
    INDEX idx_decision (firewall_decision)
);

-- ============================================================================
-- AUDIT TRAIL TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_trail (
    id BIGSERIAL PRIMARY KEY,
    action VARCHAR NOT NULL,
    actor VARCHAR NOT NULL,
    details JSON,
    timestamp TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    INDEX idx_action (action),
    INDEX idx_timestamp (created_at)
);

-- ============================================================================
-- VIEWS
-- ============================================================================

-- View: Recent tiles with their witness status
CREATE OR REPLACE VIEW recent_witnessed_tiles AS
SELECT 
    t.tile_id,
    t.satellite_source,
    t.region,
    t.timestamp,
    w.witness_node,
    w.observation_timestamp,
    i.invariant_value,
    t.consensus_k_value
FROM tiles t
LEFT JOIN witness_ledger w ON t.id = w.tile_id
LEFT JOIN invariants i ON t.id = i.tile_id
ORDER BY t.timestamp DESC
LIMIT 1000;

-- View: Consensus summary
CREATE OR REPLACE VIEW consensus_summary AS
SELECT 
    DATE_TRUNC('hour', created_at) as hour,
    COUNT(*) as event_count,
    AVG(k_value_after::float) as avg_k_value,
    MAX(k_value_after::float) as max_k_value,
    MIN(k_value_after::float) as min_k_value
FROM consensus_events
GROUP BY DATE_TRUNC('hour', created_at)
ORDER BY hour DESC;

-- ============================================================================
-- INDEXES
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_tiles_timestamp ON tiles(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_witness_ledger_position ON witness_ledger(ledger_position DESC);
CREATE INDEX IF NOT EXISTS idx_invariants_certificate ON invariants(immutable_certificate);
CREATE INDEX IF NOT EXISTS idx_consensus_k_value ON consensus_events(k_value_after);
CREATE INDEX IF NOT EXISTS idx_firewall_decisions ON firewall_decisions(created_at DESC);
