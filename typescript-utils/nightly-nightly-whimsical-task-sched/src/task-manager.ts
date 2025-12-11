export interface Task {
  name: string;
  time: string;
}

export class TaskManager {
  tasks: Task[] = [];

  static async load(filePath: string): Promise<TaskManager> {
    try {
      const data = await readFile(filePath, 'utf-8');
      return new TaskManager(JSON.parse(data));
    } catch (err) {
      return new TaskManager();
    }
  }

  constructor(tasks: Task[] = []) {
    this.tasks = tasks;
  }

  addTask(task: Task): void {
    this.tasks.push(task);
  }

  removeTask(index: number): void {
    this.tasks.splice(index, 1);
  }

  async save(filePath: string): Promise<void> {
    await writeFile(filePath, JSON.stringify(this.tasks, null, 2));
  }
}
