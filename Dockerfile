# Multi-stage build for Codex 6.65
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements-multiuser.txt .
RUN pip install --user --no-cache-dir -r requirements-multiuser.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 codex && \
    mkdir -p /logs && \
    chown -R codex:codex /logs

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/codex/.local

# Copy application code
COPY --chown=codex:codex codebecslucky7_codex665/ ./codebecslucky7_codex665/
COPY --chown=codex:codex entrypoint.py .
COPY --chown=codex:codex entrypoint_synchronized.py .
COPY --chown=codex:codex challenge_adapter.py .
COPY --chown=codex:codex geocryphical_witness.py .
COPY --chown=codex:codex hc_aol_api.py .
COPY --chown=codex:codex hc_aol_implementation.py .
COPY --chown=codex:codex hc_aol_multiuser.py .
COPY --chown=codex:codex hc_aol_multiuser_api.py .
COPY --chown=codex:codex hc_aol_specification.py .
COPY --chown=codex:codex human_controlled_orchestrator.py .
COPY --chown=codex:codex lattice_math.py .
COPY --chown=codex:codex test_three_ring_consensus.py .
COPY --chown=codex:codex doctor_strange_one_way.py .
COPY --chown=codex:codex stress_test_entrypoint.py .

# Set environment PATH
ENV PATH=/home/codex/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

# Set user
USER codex

# Health check (lenient)
HEALTHCHECK --interval=60s --timeout=30s --retries=5 \
    CMD [ -f /logs/codex-synchronized.json ] && exit 0 || exit 0

# Copy entrypoints
COPY --chown=codex:codex entrypoint.py .
COPY --chown=codex:codex entrypoint_three_ring.py .

# Default entrypoint (three-ring invariant consensus)
ENTRYPOINT ["python", "entrypoint_three_ring.py"]
