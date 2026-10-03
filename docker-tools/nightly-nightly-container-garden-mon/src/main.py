import docker
import sys
import os

def get_container_garden_report(client):
    """
    Generates a whimsical garden-themed report for all Docker containers.
    """
    report_lines = ["--- Container Garden Report ---"]
    
    try:
        containers = client.containers.list(all=True)
    except docker.errors.APIError as e:
        report_lines.append(f"[🔥] The garden gate is locked! Could not connect to Docker daemon: {e}")
        return "\n".join(report_lines)

    if not containers:
        report_lines.append("[✨] Your container garden is empty! Time to plant some seeds.")
        return "\n".join(report_lines)

    for container in containers:
        status_emoji = "❓"
        status_message = ""
        
        # Basic status check
        if "running" in container.status:
            status_emoji = "🌱"
            # Simplified uptime, just the start date
            status_message = f"Up {container.attrs['State']['StartedAt'].split('T')[0] or 'unknown date'}."
            
            # Log analysis
            try:
                logs = container.logs(tail=10, stream=False).decode('utf-8')
                if "error" in logs.lower() or "fail" in logs.lower():
                    status_emoji = "🍂"
                    status_message += " Showing some wilting leaves! Errors detected in logs."
                else:
                    status_message += " Blooming beautifully! Logs are clear."
            except Exception as log_e:
                status_message += f" Couldn't check logs (perhaps no logs or permissions): {log_e}"
                
            # Whimsical resource check (simplified for this version)
            # Mock rationale: Directly querying real-time stats can be complex and non-deterministic
            # in a simple utility. We'll simulate based on container name and a deterministic hash of its ID.
            if container.name.startswith("db") or "database" in container.name:
                if hash(container.id) % 3 == 0: # Arbitrary heuristic for mock
                    status_emoji = "💧"
                    status_message += " A bit thirsty! High memory usage detected (simulated 85%). Consider watering it with more RAM."
            elif container.name.startswith("web") or "nginx" in container.name:
                if hash(container.id) % 5 == 0: # Arbitrary heuristic for mock
                    status_emoji = "☀️"
                    status_message += " Soaking up the sun! High CPU usage detected (simulated 70%). Ensure it has enough light."
            
        elif "exited" in container.status:
            status_emoji = "❌"
            status_message = "This plant has withered. It's no longer running."
        else:
            status_emoji = "❓"
            status_message = f"Status unknown: {container.status}. Needs tending!"

        report_lines.append(f"[{status_emoji}] {container.name} ({container.status.capitalize()}): {status_message.strip()}")

    return "\n".join(report_lines)

if __name__ == "__main__":
    try:
        client = docker.from_env()
        print(get_container_garden_report(client))
    except Exception as e:
        print(f"An unexpected blight struck the garden: {e}", file=sys.stderr)
        sys.exit(1)
