import { readFileSync } from 'fs';
import { join } from 'path';

interface Resource {
  [key: string]: number;
}

interface Task {
  name: string;
  urgency: number;
  resources_needed: string[];
}

interface PrioritizedTask {
  task: Task;
  priorityScore: number;
  feasible: boolean;
}

function calculatePriority(task: Task, resources: Resource): PrioritizedTask {
  const resourcePenalty = task.resources_needed.reduce((sum, res) => {
    return sum + (resources[res] ? 0 : 1); // 1 penalty point per missing resource
  }, 0);

  return {
    task,
    priorityScore: task.urgency - resourcePenalty,
    feasible: resourcePenalty === 0
  };
}

function main() {
  const tasksPath = process.argv[2];
  const resourcesPath = process.argv[3];

  const tasks: Task[] = JSON.parse(readFileSync(join(process.cwd(), tasksPath)).toString());
  const resources: Resource = JSON.parse(readFileSync(join(process.cwd(), resourcesPath)).toString());

  const prioritized = tasks
    .map(task => calculatePriority(task, resources))
    .sort((a, b) => b.priorityScore - a.priorityScore);

  console.log(JSON.stringify(prioritized, null, 2));
}

main();
