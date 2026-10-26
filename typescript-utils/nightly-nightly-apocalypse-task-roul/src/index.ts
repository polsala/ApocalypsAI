export type FoodLevel = 'scarce' | 'low' | 'adequate' | 'abundant';
export type WaterLevel = 'scarce' | 'low' | 'adequate' | 'abundant';
export type MaterialsLevel = 'none' | 'low' | 'some' | 'plenty';
export type ToolsLevel = 'broken' | 'basic' | 'good' | 'advanced';
export type MoraleLevel = 'low' | 'neutral' | 'high';
export type EnergyLevel = 'exhausted' | 'tired' | 'normal' | 'energetic';

export interface ResourceState {
    food: FoodLevel;
    water: WaterLevel;
    materials: MaterialsLevel;
    tools: ToolsLevel;
    morale: MoraleLevel;
}

export interface Task {
    category: string;
    description: string;
    priority: number; // Lower number means higher priority
}

const tasks: Task[] = [
    {
        category: 'Rest & Recover',
        description: 'Your body is a temple, even if it\'s a crumbling one. Find a safe spot and catch some Zs. You\'ll thank yourself later.',
        priority: 1
    },
    {
        category: 'Scavenge for Food',
        description: 'The rumbling in your stomach is a clear sign. Head out to the ruins and see what forgotten treasures (or stale crackers) you can unearth. Watch out for mutated squirrels!',
        priority: 2
    },
    {
        category: 'Scavenge for Water',
        description: 'Thirst is a cruel mistress. Seek out any remaining water sources – a leaky pipe, a forgotten cistern, or perhaps even a dew collector.',
        priority: 2
    },
    {
        category: 'Scavenge for Materials',
        description: 'Every scrap counts! Explore abandoned buildings for metal, wood, fabric, or anything that can be repurposed. One person\'s rubble is another\'s fortress component.',
        priority: 2
    },
    {
        category: 'Fortify Shelter',
        description: 'A strong home is a safe home. Reinforce walls, patch holes, and set up defenses. The wasteland is full of unwelcome guests.',
        priority: 3
    },
    {
        category: 'Craft & Repair Tools',
        description: 'A dull blade is a dangerous blade. Sharpen your tools, repair broken equipment, or forge something new from salvaged parts. Ingenuity is key to survival.',
        priority: 3
    },
    {
        category: 'Explore Nearby Area',
        description: 'Adventure calls! Venture into the unexplored fringes of your known territory. Who knows what resources, dangers, or bizarre anomalies await?',
        priority: 4
    },
    {
        category: 'Boost Morale',
        description: 'The spirit needs sustenance too. Share stories, play a salvaged instrument, or simply find a moment of quiet reflection. A strong mind is as vital as a full stomach.',
        priority: 1 // Can be high priority if morale is critical
    },
    {
        category: 'Maintain Equipment',
        description: 'Keep your gear in top shape. Clean weapons, oil moving parts, and check for wear and tear. A well-maintained kit can be the difference between life and... well, you know.',
        priority: 3
    }
];

export function suggestTask(resources: ResourceState, energy: EnergyLevel): Task {
    let viableTasks: Task[] = [];

    // Prioritize Rest if energy is low
    if (energy === 'exhausted' || energy === 'tired') {
        viableTasks.push(tasks.find(t => t.category === 'Rest & Recover')!);
    }

    // Prioritize Morale if low
    if (resources.morale === 'low') {
        viableTasks.push(tasks.find(t => t.category === 'Boost Morale')!);
    }

    // Prioritize Scavenging if food/water/materials are low
    if (resources.food === 'scarce' || resources.food === 'low') {
        viableTasks.push(tasks.find(t => t.category === 'Scavenge for Food')!);
    }
    if (resources.water === 'scarce' || resources.water === 'low') {
        viableTasks.push(tasks.find(t => t.category === 'Scavenge for Water')!);
    }
    if (resources.materials === 'none' || resources.materials === 'low') {
        viableTasks.push(tasks.find(t => t.category === 'Scavenge for Materials')!);
    }

    // Prioritize Crafting/Repairing if tools are broken/basic and materials are available
    if ((resources.tools === 'broken' || resources.tools === 'basic') && (resources.materials === 'some' || resources.materials === 'plenty')) {
        viableTasks.push(tasks.find(t => t.category === 'Craft & Repair Tools')!);
    }

    // Prioritize Fortifying if materials are available and tools are good
    if ((resources.materials === 'some' || resources.materials === 'plenty') && (resources.tools === 'good' || resources.tools === 'advanced')) {
        viableTasks.push(tasks.find(t => t.category === 'Fortify Shelter')!);
    }

    // If no critical needs, suggest general maintenance or exploration
    if (viableTasks.length === 0) {
        if (energy === 'energetic' && resources.morale === 'high' &&
            resources.food !== 'scarce' && resources.water !== 'scarce') {
            viableTasks.push(tasks.find(t => t.category === 'Explore Nearby Area')!);
        }
        viableTasks.push(tasks.find(t => t.category === 'Maintain Equipment')!);
    }

    // Filter out duplicates and sort by priority
    const uniqueTasks = Array.from(new Set(viableTasks.map(t => t.category)))
        .map(category => viableTasks.find(t => t.category === category)!);

    uniqueTasks.sort((a, b) => a.priority - b.priority);

    // If multiple tasks have the same highest priority, pick one randomly
    if (uniqueTasks.length > 1 && uniqueTasks[0].priority === uniqueTasks[1].priority) {
        const topPriorityTasks = uniqueTasks.filter(t => t.priority === uniqueTasks[0].priority);
        return topPriorityTasks[Math.floor(Math.random() * topPriorityTasks.length)];
    }

    return uniqueTasks[0] || tasks[Math.floor(Math.random() * tasks.length)]; // Fallback to a completely random task
}

// CLI execution
if (require.main === module) {
    const args = process.argv.slice(2);
    const resourceState: Partial<ResourceState> = {};
    let energy: EnergyLevel | undefined;

    for (let i = 0; i < args.length; i += 2) {
        const key = args[i].replace('--', '');
        const value = args[i + 1];

        switch (key) {
            case 'food': resourceState.food = value as FoodLevel; break;
            case 'water': resourceState.water = value as WaterLevel; break;
            case 'materials': resourceState.materials = value as MaterialsLevel; break;
            case 'tools': resourceState.tools = value as ToolsLevel; break;
            case 'morale': resourceState.morale = value as MoraleLevel; break;
            case 'energy': energy = value as EnergyLevel; break;
            default:
                console.error(`Unknown argument: ${args[i]}`);
                process.exit(1);
        }
    }

    const requiredKeys: Array<keyof ResourceState> = ['food', 'water', 'materials', 'tools', 'morale'];
    const missingKeys = requiredKeys.filter(key => !(key in resourceState));

    if (missingKeys.length > 0 || !energy) {
        console.error('Error: All resource states and energy level must be provided.');
        console.error(`Missing: ${missingKeys.map(k => `--${k}`).join(', ')}${!energy ? ', --energy' : ''}`);
        console.error('Usage: node dist/index.js --food [level] --water [level] --materials [level] --tools [level] --morale [level] --energy [level]');
        process.exit(1);
    }

    const fullResourceState: ResourceState = resourceState as ResourceState;
    const suggested = suggestTask(fullResourceState, energy);

    console.log(`\n✨ Your next task: ${suggested.category} ✨`);
    console.log(`Description: ${suggested.description}\n`);
}
