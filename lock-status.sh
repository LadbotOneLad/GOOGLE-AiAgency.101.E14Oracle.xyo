#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════
# 90-DAY ENGINE LOCK STATUS VERIFICATION
# ════════════════════════════════════════════════════════════════════════════
# 
# Displays comprehensive lock status across all 14 engines
# 
# Usage:
#   ./lock-status.sh
#   ./lock-status.sh watch     (continuous monitoring)
#   ./lock-status.sh json      (JSON output)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCK_FILE="${SCRIPT_DIR}/lock-metadata.json"
ENV_LOCK_FILE="${SCRIPT_DIR}/.env.lock"

# ════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════

check_lock_file() {
  if [[ ! -f "$LOCK_FILE" ]]; then
    echo "❌ Lock file not found: $LOCK_FILE"
    echo "   Run: npx ts-node lock-initialize.ts"
    exit 1
  fi
}

load_lock_vars() {
  if [[ -f "$ENV_LOCK_FILE" ]]; then
    set +a
    source "$ENV_LOCK_FILE"
    set -a
  fi
}

get_engine_status() {
  local port=$1
  local engine_id=$2

  if docker ps --format "{{.Names}}" | grep -q "engine-${engine_id}"; then
    # Container running
    local health=$(docker inspect "engine-${engine_id}" --format='{{.State.Health.Status}}' 2>/dev/null || echo "unknown")
    
    if [[ "$health" == "healthy" ]]; then
      echo "🟢"
    elif [[ "$health" == "unhealthy" ]]; then
      echo "🔴"
    else
      echo "🟡"
    fi
  else
    echo "⚪"
  fi
}

get_lock_expiry_remaining() {
  if [[ -n "${LOCK_EXPIRY:-}" ]]; then
    local expiry_epoch=$(date -d "$LOCK_EXPIRY" +%s 2>/dev/null || echo 0)
    local now_epoch=$(date +%s)
    local diff=$((expiry_epoch - now_epoch))
    
    if [[ $diff -gt 0 ]]; then
      local days=$((diff / 86400))
      local hours=$(((diff % 86400) / 3600))
      printf "%d days, %d hours" "$days" "$hours"
    else
      echo "EXPIRED"
    fi
  else
    echo "unknown"
  fi
}

format_hash() {
  local hash=$1
  echo "${hash:0:16}..."
}

# ════════════════════════════════════════════════════════════════════════════
# MAIN OUTPUT
# ════════════════════════════════════════════════════════════════════════════

display_status() {
  clear

  cat << 'EOF'
╔═════════════════════════════════════════════════════════════════════════════╗
║                   90-DAY ENGINE SYNCHRONIZATION LOCK STATUS                 ║
╚═════════════════════════════════════════════════════════════════════════════╝

EOF

  check_lock_file
  load_lock_vars

  # Parse lock metadata
  if [[ -f "$LOCK_FILE" ]]; then
    LOCK_ID=$(jq -r '.anchor.lockId' "$LOCK_FILE")
    LOCK_INCEPTION=$(jq -r '.anchor.inceptionTimestampIso' "$LOCK_FILE")
    LOCK_EXPIRY=$(jq -r '.anchor.expiryTimestampIso' "$LOCK_FILE")
    ENGINE_COUNT=$(jq -r '.anchor.engineCount' "$LOCK_FILE")
    LOCK_PHRASE=$(jq -r '.anchor.lockPhrase' "$LOCK_FILE")
    ROOT_HASH=$(jq -r '.anchor.rootMerkleHash' "$LOCK_FILE" | cut -c1-16)
    W_SUU=$(jq -r '.anchor.wobbleSnapshot.w_suu' "$LOCK_FILE")
    W_AHA=$(jq -r '.anchor.wobbleSnapshot.w_aha' "$LOCK_FILE")
    W_RERE=$(jq -r '.anchor.wobbleSnapshot.w_rere' "$LOCK_FILE")
  fi

  # ════════════════════════════════════════════════════════════════════════════
  # LOCK METADATA
  # ════════════════════════════════════════════════════════════════════════════

  cat << EOF
LOCK METADATA
─────────────────────────────────────────────────────────────────────────────
Lock ID:              ${LOCK_ID}
Lock Phrase:          ${LOCK_PHRASE}
Inception:            ${LOCK_INCEPTION}
Expiry:               ${LOCK_EXPIRY}
Time Remaining:       $(get_lock_expiry_remaining)
Root Merkle Hash:     ${ROOT_HASH}
Synchronized Engines: ${ENGINE_COUNT}

EOF

  # ════════════════════════════════════════════════════════════════════════════
  # WOBBLE SNAPSHOT
  # ════════════════════════════════════════════════════════════════════════════

  cat << EOF
WOBBLE CONSTANTS (Locked)
─────────────────────────────────────────────────────────────────────────────
  🔢 w_suu (Identity):   ${W_SUU}   iti (micro)
  📐 w_aha (Structure):  ${W_AHA}  waenga (mid)
  🔁 w_rere (Flow):      ${W_RERE}    nui (macro)

  Kotahitanja Formula: H = (1/3)*w_suu + (1/3)*w_aha + (1/3)*w_rere
  Kotahitanja Value:   $(echo "scale=4; ($W_SUU + $W_AHA + $W_RERE) / 3" | bc)

EOF

  # ════════════════════════════════════════════════════════════════════════════
  # ENGINE STATUS (14 engines)
  # ════════════════════════════════════════════════════════════════════════════

  cat << EOF
ENGINE STATUS
─────────────────────────────────────────────────────────────────────────────

CORE ENGINES:
  $(get_engine_status 365 365) engine-365  (Validator, 365-days)
  $(get_engine_status 777 777) engine-777  (Sovereign, ultimate)
  $(get_engine_status 101 101) engine-101  (Horizon, boundary)

PEER ENGINES (12):
EOF

  for i in {1001..1012}; do
    printf "  %s engine-%d  (Peer %d)\n" "$(get_engine_status $i $i)" "$i" "$((i - 1000))"
  done

  # ════════════════════════════════════════════════════════════════════════════
  # LOCK STRENGTH & HEALTH
  # ════════════════════════════════════════════════════════════════════════════

  cat << EOF

LOCK HEALTH
─────────────────────────────────────────────────────────────────────────────

Status Legend:
  🟢 healthy   - Engine running, lock validated
  🟡 warning   - Engine running, health checks pending
  🔴 critical  - Engine unhealthy or lock validation failed
  ⚪ offline   - Engine not running

Remaining Time Status:
  CRITICAL (< 7 days)  - Renewal soon required
  STRONG (7-30 days)   - Normal operation
  LOCKED (30+ days)    - Full synchronization window

EOF

  # Container count
  local running=$(docker ps --filter "label=lock=90day-sync" --format "{{.Names}}" 2>/dev/null | wc -l)
  echo "Containers Running:   $running / $((ENGINE_COUNT + 4)) (engines + observability)"

  echo ""
  echo "Next Steps:"
  echo "  • Monitor lock expiry: watch -n 10 './lock-status.sh'"
  echo "  • Check engine logs:   docker-compose -f docker-compose-90DAY-LOCK.yml logs -f engine-365"
  echo "  • Verify lock:         curl http://localhost:365/4gr/lock-status"
  echo "  • Renew lock (day 80): npx ts-node lock-initialize.ts"
  echo ""
}

# ════════════════════════════════════════════════════════════════════════════
# WATCH MODE
# ════════════════════════════════════════════════════════════════════════════

watch_status() {
  while true; do
    display_status
    sleep 10
  done
}

# ════════════════════════════════════════════════════════════════════════════
# JSON OUTPUT
# ════════════════════════════════════════════════════════════════════════════

output_json() {
  check_lock_file
  load_lock_vars

  jq . "$LOCK_FILE"
}

# ════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY
# ════════════════════════════════════════════════════════════════════════════

case "${1:-}" in
  watch)
    watch_status
    ;;
  json)
    output_json
    ;;
  *)
    display_status
    ;;
esac
