#!/usr/bin/env python3
"""
Simple web dashboard for the chaos monkey.
"""

from flask import Flask, render_template, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)

CHAOS_API_URL = "http://localhost:8080"

@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    """Get chaos monkey stats."""
    try:
        response = requests.get(f"{CHAOS_API_URL}/stats")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/events')
def api_events():
    """Get recent chaos events."""
    try:
        response = requests.get(f"{CHAOS_API_URL}/events")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config')
def api_config():
    """Get chaos monkey configuration."""
    try:
        response = requests.get(f"{CHAOS_API_URL}/config")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/trigger', methods=['POST'])
def api_trigger():
    """Trigger a manual chaos event."""
    try:
        response = requests.post(f"{CHAOS_API_URL}/chaos")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=False)
