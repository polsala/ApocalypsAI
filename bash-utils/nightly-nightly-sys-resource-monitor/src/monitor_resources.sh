#!/bin/bash

# Default thresholds
CPU_THRESHOLD=${CPU_THRESHOLD:-80}
MEM_THRESHOLD=${MEM_THRESHOLD:-80}
DISK_THRESHOLD=${DISK_THRESHOLD:-90}
ALERT_EMAIL=${ALERT_EMAIL:-}

# --- Helper Functions ---

# Function to log messages
log_message() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message"
}

# Function to send email alert
send_alert() {
    local subject="$1"
    local body="$2"
    if [ -n "$ALERT_EMAIL" ]; then
        echo -e "$body" | sendmail "$ALERT_EMAIL"
        if [ $? -eq 0 ]; then
            log_message "INFO" "Alert email sent to $ALERT_EMAIL: $subject"
        else
            log_message "ERROR" "Failed to send alert email to $ALERT_EMAIL."
        fi
    else
        log_message "INFO" "No ALERT_EMAIL configured. Alert: $subject"
    fi
}

# --- Main Logic ---

log_message "INFO" "Starting system resource monitoring."

# Monitor CPU Usage
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')

if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l) )); then
    ALERT_BODY="CPU usage is critically high: ${CPU_USAGE}% (Threshold: ${CPU_THRESHOLD}%)"
    send_alert "High CPU Usage" "$ALERT_BODY"
    log_message "WARN" "$ALERT_BODY"
else
    log_message "INFO" "CPU usage: ${CPU_USAGE}% (Threshold: ${CPU_THRESHOLD}%)"
fi

# Monitor Memory Usage
MEM_USAGE=$(free | grep Mem: | awk '{print ($3/$2)*100}')

if (( $(echo "$MEM_USAGE > $MEM_THRESHOLD" | bc -l) )); then
    ALERT_BODY="Memory usage is critically high: ${MEM_USAGE}% (Threshold: ${MEM_THRESHOLD}%)"
    send_alert "High Memory Usage" "$ALERT_BODY"
    log_message "WARN" "$ALERT_BODY"
else
    log_message "INFO" "Memory usage: ${MEM_USAGE}% (Threshold: ${MEM_THRESHOLD}%)"
fi

# Monitor Disk Usage
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -gt "$DISK_THRESHOLD" ]; then
    ALERT_BODY="Disk usage is critically high on /: ${DISK_USAGE}% (Threshold: ${DISK_THRESHOLD}%)"
    send_alert "High Disk Usage" "$ALERT_BODY"
    log_message "WARN" "$ALERT_BODY"
else
    log_message "INFO" "Disk usage on /: ${DISK_USAGE}% (Threshold: ${DISK_THRESHOLD}%)"
fi

log_message "INFO" "System resource monitoring finished."

exit 0
