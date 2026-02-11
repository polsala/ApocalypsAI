#!/bin/bash

set -euo pipefail

help() {
  echo "Usage: $0 --type <network|service> [OPTIONS] --interval <cron_expression>"
  echo "Options:"
  echo "  --type TYPE         Type of chaos (network/service)"
  echo "  --delay MS          Delay in milliseconds (network only)"
  echo "  --loss PERCENT      Packet loss percentage (network only)"
  echo "  --service NAME      Service name to restart (service only)"
  echo "  --interval CRON     Cron-style interval expression"
  echo "  --dry-run           Validate without scheduling"
  exit 1
}

TYPE=""
DELAY=""
LOSS=""
SERVICE=""
INTERVAL=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --type) TYPE="$2"; shift 2 ;;
    --delay) DELAY="$2"; shift 2 ;;
    --loss) LOSS="$2"; shift 2 ;;
    --service) SERVICE="$2"; shift 2 ;;
    --interval) INTERVAL="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    *) echo "Unknown option $1"; help ;;
  esac
done

if [[ -z "$TYPE" || -z "$INTERVAL" ]]; then
  echo "Error: --type and --interval are required."
  help
fi

if [[ "$TYPE" == "network" && -z "$DELAY" && -z "$LOSS" ]]; then
  echo "Error: network type requires --delay or --loss."
  help
fi

if [[ "$TYPE" == "service" && -z "$SERVICE" ]]; then
  echo "Error: service type requires --service."
  help
fi

CMD=""
if [[ "$TYPE" == "network" ]]; then
  CMD="tc qdisc add dev lo root netem"
  [[ -n "$DELAY" ]] && CMD+=" delay ${DELAY}ms"
  [[ -n "$LOSS" ]] && CMD+=" loss ${LOSS}%"
elif [[ "$TYPE" == "service" ]]; then
  CMD="systemctl restart $SERVICE"
fi

if [[ "$DRY_RUN" == true ]]; then
  echo "[DRY RUN] Would schedule: $CMD at '$INTERVAL'"
  exit 0
fi

# Create temporary script for cron
TMP_SCRIPT=$(mktemp)
cat > "$TMP_SCRIPT" <<EOF
#!/bin/bash
$CMD
EOF
chmod +x "$TMP_SCRIPT"

# Add to crontab
CRON_ENTRY="$INTERVAL $TMP_SCRIPT"
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "Chaos event scheduled: $CMD at '$INTERVAL'"
