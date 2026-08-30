#!/bin/bash

# Default values
DEFAULT_EXPIRATION_LABEL="apocalypsai.expires_at"
DEFAULT_EPHEMERAL_LABEL="apocalypsai.ephemeral"
CURRENT_TIME=$(date +%s)

echo "ApocalypsAI Container Wrangler starting..."
echo "Current Unix timestamp: ${CURRENT_TIME}"

# List all containers, including stopped ones, and extract ID and labels
# Format: ID\tLabels
docker ps -a --format "{{.ID}}\t{{.Labels}}" | while IFS=$'\t' read -r CONTAINER_ID CONTAINER_LABELS; do
    IS_EPHEMERAL="false"
    EXPIRES_AT=""

    # Parse labels
    IFS=',' read -ra LABELS_ARRAY <<< "$CONTAINER_LABELS"
    for LABEL in "${LABELS_ARRAY[@]}"; do
        KEY=$(echo "$LABEL" | cut -d'=' -f1)
        VALUE=$(echo "$LABEL" | cut -d'=' -f2)
        if [[ "$KEY" == "$DEFAULT_EPHEMERAL_LABEL" && "$VALUE" == "true" ]]; then
            IS_EPHEMERAL="true"
        elif [[ "$KEY" == "$DEFAULT_EXPIRATION_LABEL" ]]; then
            EXPIRES_AT="$VALUE"
        fi
    done

    if [[ "$IS_EPHEMERAL" == "true" ]]; then
        echo "Found ephemeral container: $CONTAINER_ID with labels: $CONTAINER_LABELS"
        if [[ -n "$EXPIRES_AT" ]]; then
            if [[ "$EXPIRES_AT" -lt "$CURRENT_TIME" ]]; then
                echo "Container $CONTAINER_ID (expires: $EXPIRES_AT) has expired. Wrangling it!"
                # In a real scenario, uncomment the lines below to stop and remove the container.
                # docker stop "$CONTAINER_ID" > /dev/null 2>&1
                # docker rm "$CONTAINER_ID" > /dev/null 2>&1
                echo "MOCK: Would stop and remove container $CONTAINER_ID"
            else
                echo "Container $CONTAINER_ID (expires: $EXPIRES_AT) is still active. Leaving it be."
            fi
        else
            echo "Ephemeral container $CONTAINER_ID has no '$DEFAULT_EXPIRATION_LABEL' label. Leaving it be."
        fi
    fi
done

echo "ApocalypsAI Container Wrangler finished."
