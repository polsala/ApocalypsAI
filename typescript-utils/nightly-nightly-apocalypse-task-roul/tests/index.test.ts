import { suggestTask, ResourceState, EnergyLevel, Task } from '../src/index';

describe('suggestTask', () => {
    let mockMathRandom: jest.SpyInstance;

    beforeEach(() => {
        // Mock rationale: Math.random is used for selecting a random task when multiple tasks
        // have the same highest priority. Mocking it ensures deterministic test results.
        mockMathRandom = jest.spyOn(Math, 'random').mockReturnValue(0.1); // Always pick the first item if random selection is needed
    });

    afterEach(() => {
        mockMathRandom.mockRestore();
    });

    it('should prioritize "Rest & Recover" when energy is exhausted', () => {
        const resources: ResourceState = {
            food: 'adequate', water: 'adequate', materials: 'some',
            tools: 'good', morale: 'neutral'
        };
        const energy: EnergyLevel = 'exhausted';
        const task = suggestTask(resources, energy);
        expect(task.category).toBe('Rest & Recover');
    });

    it('should prioritize "Boost Morale" when morale is low', () => {
        const resources: ResourceState = {
            food: 'adequate', water: 'adequate', materials: 'some',
            tools: 'good', morale: 'low'
        };
        const energy: EnergyLevel = 'normal';
        const task = suggestTask(resources, energy);
        expect(task.category).toBe('Boost Morale');
    });

    it('should prioritize "Scavenge for Food" when food is scarce', () => {
        const resources: ResourceState = {
            food: 'scarce', water: 'adequate', materials: 'some',
            tools: 'good', morale: 'neutral'
        };
        const energy: EnergyLevel = 'normal';
        const task = suggestTask(resources, energy);
        expect(task.category).toBe('Scavenge for Food');
    });

    it('should prioritize "Scavenge for Water" when water is low', () => {
        const resources: ResourceState = {
            food: 'adequate', water: 'low', materials: 'some',
            tools: 'good', morale: 'neutral'
        };
        const energy: EnergyLevel = 'normal';
        const task = suggestTask(resources, energy);
        expect(task.category).toBe('Scavenge for Water');
    });

    it('should prioritize "Scavenge for Materials" when materials are none', () => {
        const resources: ResourceState = {
            food: 'adequate', water: 'adequate', materials: 'none',
            tools: 'good', morale: 'neutral'
        };
        const energy: EnergyLevel = 'normal';
        const task = suggestTask(resources, energy);
        expect(task.category).toBe('Scavenge for Materials');
    });

    it('should prioritize "Craft & Repair Tools" when tools are broken and materials are plenty', () => {
        const resources: ResourceState = {
            food: 'adequate', water: 'adequate', materials: 'plenty',
            tools: 'broken', morale: 'neutral'
        };
        const energy: EnergyLevel = 'normal';
        const task = suggestTask(resources, energy);
        expect(task.category).toBe('Craft & Repair Tools');
    });

    it('should prioritize "Fortify Shelter" when materials are plenty and tools are good', () => {
        const resources: ResourceState = {
            food: 'adequate', water: 'adequate', materials: 'plenty',
            tools: 'good', morale: 'neutral'
        };
        const energy: EnergyLevel = 'normal';
        const task = suggestTask(resources, energy);
        expect(task.category).toBe('Fortify Shelter');
    });

    it('should suggest "Explore Nearby Area" when energetic and all resources are good', () => {
        const resources: ResourceState = {
            food: 'abundant', water: 'abundant', materials: 'plenty',
            tools: 'advanced', morale: 'high'
        };
        const energy: EnergyLevel = 'energetic';
        const task = suggestTask(resources, energy);
        expect(task.category).toBe('Explore Nearby Area');
    });

    it('should suggest "Maintain Equipment" as a fallback if no critical needs and not energetic enough to explore', () => {
        const resources: ResourceState = {
            food: 'adequate', water: 'adequate', materials: 'some',
            tools: 'good', morale: 'neutral'
        };
        const energy: EnergyLevel = 'normal';
        const task = suggestTask(resources, energy);
        expect(task.category).toBe('Maintain Equipment');
    });

    it('should handle multiple high-priority needs, picking one deterministically with mock', () => {
        const resources: ResourceState = {
            food: 'scarce', water: 'scarce', materials: 'none',
            tools: 'broken', morale: 'low'
        };
        const energy: EnergyLevel = 'exhausted';
        const task = suggestTask(resources, energy);
        // With mockMathRandom returning 0.1, and 'Rest & Recover' being the first priority 1 task added,
        // it should be selected when multiple top-priority tasks exist.
        expect(task.category).toBe('Rest & Recover');
    });

    it('should return a task even with minimal inputs (fallback)', () => {
        const resources: ResourceState = {
            food: 'adequate', water: 'adequate', materials: 'some',
            tools: 'good', morale: 'neutral'
        };
        const energy: EnergyLevel = 'normal';
        const task = suggestTask(resources, energy);
        expect(task).toBeDefined();
        expect(typeof task.category).toBe('string');
        expect(typeof task.description).toBe('string');
    });
});
