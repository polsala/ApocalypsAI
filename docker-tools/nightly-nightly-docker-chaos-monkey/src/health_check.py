#!/usr/bin/env python3
"""
Health check endpoint for the chaos monkey.
"""

from flask import Flask, jsonify
from datetime import datetime
import docker

app = Flask(__name__)

docker_client = docker.from_env()

@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        # Test Docker connectivity
        docker_client.ping()
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "docker_connected": True,
            "version": "1.0.0"
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "docker_connected": False,
            "error": str(e)
        }), 503

@app.route('/ready')
def ready():
    """Readiness check endpoint."""
    try:
        # Check if we can list containers (basic readiness)
        containers = docker_client.containers.list()
        
        return jsonify({
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
            "containers_count": len(containers),
            "message": "Chaos Monkey is ready to inject chaos!"
        })
    except Exception as e:
        return jsonify({
            "status": "not ready",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
