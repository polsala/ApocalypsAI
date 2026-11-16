import os
import datetime
import json

def handler(event, context):
    current_time = datetime.datetime.now(datetime.timezone.utc)
    # Simulate a "stable time" for comparison
    # Whimsical: Let's say the universe was stable on Jan 1, 2000, 00:00:00 UTC
    stable_time_str = os.environ.get("STABLE_TIME", "2000-01-01T00:00:00Z")
    stable_time = datetime.datetime.fromisoformat(stable_time_str.replace('Z', '+00:00'))

    time_difference = current_time - stable_time
    
    rift_threshold_seconds = int(os.environ.get("RIFT_THRESHOLD_SECONDS", "3600")) # 1 hour

    status = "STABLE"
    message = f"Temporal field is stable. Current time: {current_time.isoformat()}. Stable reference: {stable_time.isoformat()}."

    if abs(time_difference.total_seconds()) > rift_threshold_seconds:
        status = "RIFT_DETECTED"
        message = f"WARNING: Temporal rift detected! Time deviation of {time_difference.total_seconds()} seconds from stable reference. Current time: {current_time.isoformat()}."
    
    print(json.dumps({"status": status, "message": message}))
    
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }
