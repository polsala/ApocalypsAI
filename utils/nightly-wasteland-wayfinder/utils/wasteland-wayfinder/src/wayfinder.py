import argparse
import json
import os
from datetime import datetime

DATA_FILE = 'wasteland_tasks.json'

URGENCY_MAP = {
    'critical': 4,
    'high': 3,
    'medium': 2,
    'low': 1
}

URGENCY_REVERSE_MAP = {v: k for k, v in URGENCY_MAP.items()}

def _load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def _save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(description, urgency_str, resources):
    tasks = _load_tasks()
    urgency = URGENCY_MAP.get(urgency_str.lower(), URGENCY_MAP['medium'])
    task = {
        'id': len(tasks) + 1,
        'description': description,
        'urgency': urgency,
        'resources': sorted(list(set(r.strip() for r in resources if r.strip()))), # Ensure unique and sorted resources
        'completed': False,
        'created_at': datetime.now().isoformat()
    }
    tasks.append(task)
    _save_tasks(tasks)
    print(f"Task '{description}' added with ID {task['id']}.")

def list_tasks(include_completed=False):
    tasks = _load_tasks()
    
    # Sort by urgency (descending), then by description (ascending) for deterministic output
    sorted_tasks = sorted(tasks, key=lambda t: (t['urgency'], t['description']), reverse=True)

    print("\n--- Wasteland Wayfinder: Current Objectives ---")
    active_tasks_found = False
    for task in sorted_tasks:
        if include_completed or not task['completed']:
            status = "[X]" if task['completed'] else "[ ]"
            urgency_label = URGENCY_REVERSE_MAP.get(task['urgency'], 'unknown').capitalize()
            resources_str = ', '.join(task['resources']) if task['resources'] else 'None'
            print(f"{status} ID: {task['id']} | Urgency: {urgency_label:<8} | Resources: {resources_str:<20} | Description: {task['description']}")
            active_tasks_found = True
    
    if not active_tasks_found:
        print("No tasks found. Time to scavenge for new objectives!")
    print("-----------------------------------------------\n")

def complete_task(task_id):
    tasks = _load_tasks()
    found = False
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            found = True
            print(f"Task '{task['description']}' (ID: {task_id}) marked as completed.")
            break
    if not found:
        print(f"Error: Task with ID {task_id} not found.")
    _save_tasks(tasks)

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Wayfinder: A CLI task manager for the post-apocalyptic era."
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', type=str, help='Description of the task')
    add_parser.add_argument('--urgency', type=str, default='medium', choices=URGENCY_MAP.keys(),
                            help='Urgency level of the task (critical, high, medium, low)')
    add_parser.add_argument('--resources', nargs='*', default=[],
                            help='Space-separated list of resources needed (e.g., Food Water Ammo)')

    # List command
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument('--completed', action='store_true', help='Include completed tasks')

    # Complete command
    complete_parser = subparsers.add_parser('complete', help='Mark a task as completed')
    complete_parser.add_argument('task_id', type=int, help='ID of the task to complete')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.description, args.urgency, args.resources)
    elif args.command == 'list':
        list_tasks(args.completed)
    elif args.command == 'complete':
        complete_task(args.task_id)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
