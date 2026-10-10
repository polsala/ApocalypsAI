import os
import json
from flask import Flask, render_template, jsonify
import docker # type: ignore # Docker SDK is external

app = Flask(__name__)

def get_container_mood(container_logs):
    """Determines a whimsical mood based on container logs."""
    logs_lower = container_logs.lower()
    if "error" in logs_lower or "fail" in logs_lower or "exception" in logs_lower:
        return {"mood": "Wilting", "emoji": "🥀", "color": "red"}
    if "warning" in logs_lower or "slow" in logs_lower:
        return {"mood": "Droopy", "emoji": "💧", "color": "orange"}
    if "healthy" in logs_lower or "success" in logs_lower or "ready" in logs_lower:
        return {"mood": "Vibrant", "emoji": "🌿", "color": "green"}
    if "starting" in logs_lower or "initializing" in logs_lower:
        return {"mood": "Sprouting", "emoji": "🌱", "color": "lightblue"}
    return {"mood": "Content", "emoji": "🌼", "color": "lightgreen"}

def get_container_data():
    """Fetches data for all running containers."""
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)
        garden_data = []
        for container in containers:
            status_emoji = "❓"
            status_color = "gray"
            if "running" in container.status:
                status_emoji = "🟢"
                status_color = "green"
            elif "exited" in container.status or "dead" in container.status:
                status_emoji = "🔴"
                status_color = "red"
            elif "paused" in container.status:
                status_emoji = "⏸️"
                status_color = "yellow"
            elif "restarting" in container.status:
                status_emoji = "🔄"
                status_color = "blue"

            # Fetch recent logs for mood analysis
            # Using a small tail to avoid excessive log fetching for performance
            try:
                logs = container.logs(tail=10).decode('utf-8')
            except Exception: # Mock rationale: container.logs() might fail if container is not running or has no logs
                logs = ""
            
            mood_info = get_container_mood(logs)

            garden_data.append({
                "id": container.id[:12],
                "name": container.name,
                "status": container.status,
                "status_emoji": status_emoji,
                "status_color": status_color,
                "image": container.image.tags[0] if container.image.tags else "unknown",
                "mood": mood_info["mood"],
                "mood_emoji": mood_info["emoji"],
                "mood_color": mood_info["color"],
                "ports": [f"{p.public_port}->{p.private_port}/{p.ip_proto}" for p in container.ports.values() if p.public_port]
            })
        return garden_data
    except Exception as e:
        app.logger.error(f"Error fetching container data: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/containers')
def api_containers():
    data = get_container_data()
    return jsonify(data)

if __name__ == '__main__':
    # For development, run with `flask run` or `python app.py`
    # In production, use a WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
