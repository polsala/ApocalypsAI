import re

def decode_log(log_message: str) -> str:
    """
    Translates a cryptic log message into a more human-readable,
    often dramatically framed, warning or insight.
    """

    log_message_lower = log_message.lower()

    # Define patterns and their ancient whispers
    patterns = [
        (r"error:?.*connection refused", "A spectral barrier denies passage. The outer realms reject our touch."),
        (r"warn:?.*disk usage.*(9[0-9]|100)%", "The vessel's memory groans under the weight of accumulated dust. Soon, it shall burst!"),
        (r"error:?.*file not found", "A vital scroll is missing from the archives. The path to knowledge is broken."),
        (r"error:?.*permission denied", "The ancient guardians forbid this action. You lack the sacred sigils."),
        (r"critical:?.*system integrity compromised", "The very fabric of reality tears! A core meltdown of existence is at hand!"),
        (r"error:?.*memory leak", "A slow, insidious drain saps the lifeblood of the machine. Its essence dissipates into the void."),
        (r"error:?.*timeout", "The cosmic clock ticks, yet no response echoes. The connection to the beyond has been severed."),
        (r"error:?.*database connection failed", "The sacred scrolls are unreachable. The Oracle sleeps, or perhaps, has vanished."),
        (r"warn:?.*deprecated", "An ancient ritual, once potent, now wanes. Its power diminishes with each passing cycle."),
        (r"info:?.*logged in", "A new soul has entered the hallowed halls. Observe their movements."),
        (r"debug:?.*", "The seers peer into the minutiae, seeking patterns in the cosmic dust."),
        (r"error:?.*", "An unforeseen anomaly ripples through the ether. The weave of fate is disturbed."),
        (r"warn:?.*", "A tremor in the force. Heed this subtle warning, lest it grow into a cataclysm."),
        (r"success:?.*|completed:?.*|done:?.*", "The ritual is complete. The stars align, and balance is restored.")
    ]

    for pattern, whisper in patterns:
        if re.search(pattern, log_message_lower):
            return whisper

    # Default whisper if no pattern matches
    return "The ancients are silent on this matter, yet unease lingers. A mystery for the ages..."

if __name__ == "__main__":
    # Example usage for direct execution
    test_logs = [
        "ERROR: Connection refused by remote host 192.168.1.100:8080",
        "WARN: Disk usage on /var/log is at 95%",
        "INFO: User 'admin' logged in from 10.0.0.5",
        "DEBUG: Processing request with ID 12345",
        "CRITICAL: System integrity compromised, core meltdown imminent!",
        "Unknown error code 0xDEADBEEF",
        "ERROR: File 'config.yaml' not found in /etc/app/",
        "WARN: Using deprecated API endpoint /v1/old_feature",
        "SUCCESS: Data backup completed.",
        "ERROR: Database connection failed after 3 attempts.",
        "WARN: Low memory detected, consider increasing swap.",
        "ERROR: Permission denied for user 'guest' on resource '/data'.",
        "Operation done.",
        "Just a regular log message.",
        "ERROR: A memory leak was detected in module 'core_engine'.",
        "ERROR: Request to external service timed out after 30s."
    ]

    for log in test_logs:
        print(f"Original: {log}\nDecoded: {decode_log(log)}\n")
