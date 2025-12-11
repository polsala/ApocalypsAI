# Apocalypse Task Optimizer

CLI tool that prioritizes survival tasks based on resource availability, urgency, and environmental factors.

## Usage
```bash
npx task-optimizer --tasks tasks.json --resources resources.json
```

## Example Input
```json
tasks.json:
[
  { "name": "Find water", "urgency": 8, "resources_needed": ["rope", "container"] },
  { "name": "Build shelter", "urgency": 6, "resources_needed": ["wood"] }
]

resources.json:
{
  "rope": 2, "container": 1, "wood": 0
}
```

## Output
Sorted task list with priority scores and feasibility status
