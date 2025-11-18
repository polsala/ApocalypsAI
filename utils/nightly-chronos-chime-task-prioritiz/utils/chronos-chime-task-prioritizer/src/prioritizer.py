import json
import sys
from collections import defaultdict, deque

class TaskScheduler:
    def __init__(self, tasks_data):
        self.tasks = {task['name']: task for task in tasks_data}
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self.critical_tasks = set()

        for task in tasks_data:
            if task.get('critical', False):
                self.critical_tasks.add(task['name'])
            for dep_name in task.get('dependencies', []):
                if dep_name not in self.tasks:
                    raise ValueError(f"Dependency '{dep_name}' for task '{task['name']}' not found.")
                self.graph[dep_name].append(task['name'])
                self.in_degree[task['name']] += 1

        # Ensure all tasks are in in_degree map, even if they have no dependencies
        for task_name in self.tasks:
            if task_name not in self.in_degree:
                self.in_degree[task_name] = 0

    def _topological_sort(self):
        q = deque([name for name, degree in self.in_degree.items() if degree == 0])
        sorted_tasks = []
        
        # Kahn's algorithm for topological sort
        while q:
            # Prioritize critical tasks if multiple options are available at the same dependency level
            current_level_tasks = []
            while q:
                current_level_tasks.append(q.popleft())
            
            # Sort current_level_tasks: critical tasks first, then by name for determinism
            current_level_tasks.sort(key=lambda x: (x not in self.critical_tasks, x))
            
            for u in current_level_tasks:
                sorted_tasks.append(u)
                for v in self.graph[u]:
                    self.in_degree[v] -= 1
                    if self.in_degree[v] == 0:
                        q.append(v)

        if len(sorted_tasks) != len(self.tasks):
            # If not all tasks are sorted, there's a cycle
            raise ValueError("Circular dependency detected in tasks.")
        
        return sorted_tasks

    def schedule(self):
        try:
            sorted_task_names = self._topological_sort()
        except ValueError as e:
            return {"error": str(e)}

        scheduled_tasks = []
        total_duration = 0
        critical_path_tasks = []

        for task_name in sorted_task_names:
            task = self.tasks[task_name]
            scheduled_tasks.append({
                "name": task['name'],
                "duration": task['duration'],
                "is_critical": task.get('critical', False)
            })
            total_duration += task['duration']
            if task.get('critical', False):
                critical_path_tasks.append(task['name'])

        return {
            "scheduled_tasks": scheduled_tasks,
            "total_duration": total_duration,
            "critical_path_tasks": critical_path_tasks
        }

def format_duration(minutes):
    if minutes == 0:
        return "0 minutes"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    parts = []
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if remaining_minutes > 0:
        parts.append(f"{remaining_minutes} minute{'s' if remaining_minutes > 1 else ''}")
    return " ".join(parts)

def main():
    if len(sys.argv) < 2:
        print("Usage: python prioritizer.py <path_to_tasks_json>")
        sys.exit(1)

    tasks_file_path = sys.argv[1]
    try:
        with open(tasks_file_path, 'r') as f:
            tasks_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Task file not found at '{tasks_file_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{tasks_file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        sys.exit(1)

    try:
        scheduler = TaskScheduler(tasks_data)
        result = scheduler.schedule()

        if "error" in result:
            print(f"Error: {result['error']}")
            sys.exit(1)

        print("\nChronos-Chime Task Prioritizer Report\n")
        print(f"Total estimated time: {format_duration(result['total_duration'])}\n")
        print("--- Schedule ---")
        for i, task in enumerate(result['scheduled_tasks']):
            status = ""
            if task['is_critical']:
                status = " [CRITICAL PATH: Impending Doom!]"
            print(f"{i+1}. {task['name']} ({format_duration(task['duration'])}){status}")

        if result['critical_path_tasks']:
            print("\n--- Warnings ---")
            print(f"- Critical tasks identified: {', '.join(result['critical_path_tasks'])}")
            print("- Prioritize these tasks for survival!")
        else:
            print("\n--- No Critical Tasks Identified ---")
            print("Enjoy the calm before the storm... or just the calm.")

    except Exception as e:
        print(f"An unexpected error occurred during scheduling: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
