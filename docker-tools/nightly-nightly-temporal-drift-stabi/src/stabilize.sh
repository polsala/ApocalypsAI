#!/bin/sh

NTP_SERVER=${NTP_SERVER:-pool.ntp.org}
SYNC_INTERVAL=${SYNC_INTERVAL:-300} # Sync every 5 minutes by default

echo "Starting Temporal Drift Stabilizer..."
echo "NTP Server: ${NTP_SERVER}"
echo "Sync Interval: ${SYNC_INTERVAL} seconds"

while true; do
    echo "$(date): Attempting to synchronize time with ${NTP_SERVER}..."
    # ntpdate requires CAP_SYS_TIME capability, which should be granted when running the container.
    # For a more robust solution in production, consider chronyd or systemd-timesyncd if more advanced
    # time management (e.g., slew vs. step) is needed.
    if ntpdate -s "${NTP_SERVER}"; then
        echo "$(date): Time synchronization successful."
    else
        echo "$(date): WARNING: Time synchronization failed. Retrying in ${SYNC_INTERVAL} seconds."
    fi
    sleep "${SYNC_INTERVAL}"
done
