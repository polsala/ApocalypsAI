#!/usr/bin/env python3
"""
Generate chaos event reports.
"""

import requests
import json
import argparse
from datetime import datetime
from typing import Dict, List

CHAOS_API_URL = "http://localhost:8080"


def get_stats() -> Dict:
    """Get chaos monkey statistics."""
    response = requests.get(f"{CHAOS_API_URL}/stats")
    return response.json()


def get_events() -> List[Dict]:
    """Get recent chaos events."""
    response = requests.get(f"{CHAOS_API_URL}/events")
    return response.json()


def generate_report(output_format='json'):
    """Generate a chaos report."""
    stats = get_stats()
    events = get_events()
    
    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "summary": {
            "total_events": stats.get('total_events', 0),
            "successful_events": stats.get('successful_events', 0),
            "failed_events": stats.get('failed_events', 0),
            "success_rate": stats.get('success_rate', 0),
            "uptime": stats.get('uptime', 0)
        },
        "events": events,
        "event_types": stats.get('event_types', {})
    }
    
    if output_format == 'json':
        print(json.dumps(report, indent=2))
    elif output_format == 'text':
        print("CHAOS MONKEY REPORT")
        print("=" * 50)
        print(f"Generated at: {report['generated_at']}")
        print()
        print("SUMMARY:")
        print(f"  Total Events: {report['summary']['total_events']}")
        print(f"  Successful: {report['summary']['successful_events']}")
        print(f"  Failed: {report['summary']['failed_events']}")
        print(f"  Success Rate: {report['summary']['success_rate']:.2%}")
        print(f"  Uptime: {report['summary']['uptime']:.2f} seconds")
        print()
        print("EVENT TYPES:")
        for event_type, count in report['event_types'].items():
            print(f"  {event_type}: {count}")
        print()
        print("RECENT EVENTS:")
        for event in report['events'][-10:]:  # Last 10 events
            status = "✓" if event['success'] else "✗"
            print(f"  {status} {event['event_type']} on {event['target']} at {event['timestamp']}")
    
    return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate chaos monkey report')
    parser.add_argument('--format', choices=['json', 'text'], default='text',
                       help='Output format')
    
    args = parser.parse_args()
    generate_report(args.format)


if __name__ == '__main__':
    main()
