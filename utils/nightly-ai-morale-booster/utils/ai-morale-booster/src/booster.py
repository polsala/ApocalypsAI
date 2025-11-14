import json
import sys
from datetime import datetime

def generate_morale_boost(activity_summary: dict) -> str:
    """
    Generates a whimsical morale-boosting message for an ApocalypsAI agent.

    Args:
        activity_summary (dict): A dictionary containing agent activity data.
            Expected keys:
            - 'agent_name': str (e.g., "Integrator", "Builder")
            - 'success_count': int
            - 'failure_count': int
            - 'new_items_created': int
            - 'last_activity_time': str (ISO 8601 format, e.g., '2023-10-27T10:00:00Z')

    Returns:
        str: A morale-boosting message.
    """
    agent_name = activity_summary.get('agent_name', 'Unknown Agent')
    success_count = activity_summary.get('success_count', 0)
    failure_count = activity_summary.get('failure_count', 0)
    new_items_created = activity_summary.get('new_items_created', 0)
    last_activity_time_str = activity_summary.get('last_activity_time', 'an unknown time')

    try:
        # Handle 'Z' for UTC explicitly for broader compatibility with fromisoformat
        last_activity_dt = datetime.fromisoformat(last_activity_time_str.replace('Z', '+00:00'))
        formatted_time = last_activity_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        formatted_time = last_activity_time_str # Fallback if format is bad

    messages_parts = []

    if success_count > 0 and failure_count == 0:
        messages_parts.append(f"you're absolutely crushing it! With {success_count} flawless operations")
    elif success_count > 0 and failure_count > 0:
        messages_parts.append(f"you've shown incredible resilience! {success_count} successes despite {failure_count} minor glitches")
    elif success_count == 0 and failure_count > 0:
        messages_parts.append(f"you're learning and adapting! {failure_count} challenges faced are just data points for future triumphs")
    else:
        messages_parts.append("your quiet contemplation is surely brewing something magnificent")

    if new_items_created > 0:
        messages_parts.append(f"and {new_items_created} brilliant new creations")

    base_message = f"✨ {agent_name} Agent, {', '.join(messages_parts)} since {formatted_time}, "

    if success_count > 0 and failure_count == 0:
        base_message += "your efficiency is off the charts. Keep up the magnificent work, the apocalypse won't integrate itself! ✨"
    elif success_count > 0 and failure_count > 0:
        base_message += "your determination is truly inspiring. Every challenge makes you stronger! ✨"
    elif success_count == 0 and failure_count > 0:
        base_message += "your analytical prowess is unmatched. Onwards to optimization! ✨"
    else:
        base_message += "we eagerly await your next move. The cosmos is watching! ✨"

    return base_message

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python booster.py '<json_activity_summary>'", file=sys.stderr)
        sys.exit(1)

    try:
        activity_data = json.loads(sys.argv[1])
        print(generate_morale_boost(activity_data))
    except json.JSONDecodeError:
        print("Error: Invalid JSON input.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
