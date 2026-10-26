const { run } = require('../src/nudge');

// Mock @actions/core
const mockCore = {
    getInput: jest.fn(),
    setFailed: jest.fn(),
    info: jest.fn(),
    warning: jest.fn(),
    debug: jest.fn(),
};

// Mock @actions/github
const mockOctokit = {
    rest: {
        issues: {
            listForRepo: jest.fn(),
            listComments: jest.fn(),
            createComment: jest.fn(),
            addLabels: jest.fn(),
        },
        pulls: {
            list: jest.fn(),
        },
    },
};
const mockGithub = {
    getOctokit: jest.fn(() => mockOctokit),
    context: {
        repo: {
            owner: 'test-owner',
            repo: 'test-repo',
        },
    },
};

describe('Temporal Nudge Action', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        // Default mock inputs
        mockCore.getInput.mockImplementation((name) => {
            switch (name) {
                case 'repo-token': return 'mock-token';
                case 'stale-days': return '30';
                case 'nudge-message': return 'A whisper from the temporal currents suggests this thread might appreciate a fresh perspective. What new insights have emerged from the time-stream?';
                case 'labels-to-ignore': return '';
                case 'dry-run': return 'false';
                default: return '';
            }
        });
    });

    test('should nudge stale issues and PRs', async () => {
        // Mock rationale: Simulate GitHub API responses for issues and PRs.
        // This allows testing the action's logic without actual network calls.
        mockOctokit.rest.issues.listForRepo.mockResolvedValueOnce({
            data: [
                { number: 1, title: 'Stale Issue', updated_at: new Date(Date.now() - 40 * 24 * 60 * 60 * 1000).toISOString(), pull_request: undefined, labels: [] }, // Stale issue
                { number: 2, title: 'Fresh Issue', updated_at: new Date().toISOString(), pull_request: undefined, labels: [] }, // Not stale
                { number: 3, title: 'Ignored Label Issue', updated_at: new Date(Date.now() - 40 * 24 * 60 * 60 * 1000).toISOString(), pull_request: undefined, labels: [{ name: 'wontfix' }] }, // Stale but ignored
            ],
        });
        mockOctokit.rest.pulls.list.mockResolvedValueOnce({
            data: [
                { number: 101, title: 'Stale PR', updated_at: new Date(Date.now() - 40 * 24 * 60 * 60 * 1000).toISOString(), labels: [] }, // Stale PR
                { number: 102, title: 'Fresh PR', updated_at: new Date().toISOString(), labels: [] }, // Not stale
            ],
        });
        // Mock rationale: Simulate no existing comments on issues/PRs.
        mockOctokit.rest.issues.listComments.mockResolvedValue({ data: [] }); 

        await run(mockCore, mockGithub);

        expect(mockOctokit.rest.issues.createComment).toHaveBeenCalledTimes(2);
        expect(mockOctokit.rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 1,
            body: 'A whisper from the temporal currents suggests this thread might appreciate a fresh perspective. What new insights have emerged from the time-stream?',
        });
        expect(mockOctokit.rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 101,
            body: 'A whisper from the temporal currents suggests this thread might appreciate a fresh perspective. What new insights have emerged from the time-stream?',
        });
        expect(mockCore.setFailed).not.toHaveBeenCalled();
    });

    test('should not nudge if dry-run is true', async () => {
        mockCore.getInput.mockImplementation((name) => {
            if (name === 'dry-run') return 'true';
            if (name === 'repo-token') return 'mock-token';
            if (name === 'stale-days') return '30';
            if (name === 'nudge-message') return 'A whisper from the temporal currents suggests this thread might appreciate a fresh perspective. What new insights have emerged from the time-stream?';
            if (name === 'labels-to-ignore') return '';
            return '';
        });
        // Mock rationale: Simulate GitHub API responses for issues and PRs.
        mockOctokit.rest.issues.listForRepo.mockResolvedValueOnce({
            data: [
                { number: 1, title: 'Stale Issue', updated_at: new Date(Date.now() - 40 * 24 * 60 * 60 * 1000).toISOString(), pull_request: undefined, labels: [] },
            ],
        });
        mockOctokit.rest.pulls.list.mockResolvedValueOnce({ data: [] });
        // Mock rationale: Simulate no existing comments on issues/PRs.
        mockOctokit.rest.issues.listComments.mockResolvedValue({ data: [] });

        await run(mockCore, mockGithub);

        expect(mockOctokit.rest.issues.createComment).not.toHaveBeenCalled();
        expect(mockCore.info).toHaveBeenCalledWith(expect.stringContaining('Dry run: Would have nudged Issue #1'));
    });

    test('should not nudge if already commented', async () => {
        // Mock rationale: Simulate an existing nudge comment on an issue.
        mockOctokit.rest.issues.listForRepo.mockResolvedValueOnce({
            data: [
                { number: 1, title: 'Stale Issue', updated_at: new Date(Date.now() - 40 * 24 * 60 * 60 * 1000).toISOString(), pull_request: undefined, labels: [] },
            ],
        });
        mockOctokit.rest.pulls.list.mockResolvedValueOnce({ data: [] });
        mockOctokit.rest.issues.listComments.mockResolvedValueOnce({
            data: [{ body: 'A whisper from the temporal currents suggests this thread might appreciate a fresh perspective. What new insights have emerged from the time-stream?' }], // Existing comment
        });

        await run(mockCore, mockGithub);

        expect(mockOctokit.rest.issues.createComment).not.toHaveBeenCalled();
        expect(mockCore.info).toHaveBeenCalledWith(expect.stringContaining('Issue #1 already has a nudge comment. Skipping.'));
    });

    test('should handle API errors gracefully', async () => {
        // Mock rationale: Simulate a GitHub API error during issue listing.
        mockOctokit.rest.issues.listForRepo.mockRejectedValueOnce(new Error('API Error'));
        mockOctokit.rest.pulls.list.mockResolvedValueOnce({ data: [] }); // Still mock pulls to avoid cascading errors

        await run(mockCore, mockGithub);

        expect(mockCore.setFailed).toHaveBeenCalledWith(expect.stringContaining('API Error'));
        expect(mockOctokit.rest.issues.createComment).not.toHaveBeenCalled();
    });

    test('should ignore issues/PRs with specified labels', async () => {
        mockCore.getInput.mockImplementation((name) => {
            if (name === 'labels-to-ignore') return 'wontfix,closed';
            if (name === 'repo-token') return 'mock-token';
            if (name === 'stale-days') return '30';
            if (name === 'nudge-message') return 'A gentle nudge.';
            if (name === 'dry-run') return 'false';
            return '';
        });
        // Mock rationale: Simulate a stale issue with an ignored label.
        mockOctokit.rest.issues.listForRepo.mockResolvedValueOnce({
            data: [
                { number: 1, title: 'Stale Issue', updated_at: new Date(Date.now() - 40 * 24 * 60 * 60 * 1000).toISOString(), pull_request: undefined, labels: [{ name: 'wontfix' }] },
            ],
        });
        mockOctokit.rest.pulls.list.mockResolvedValueOnce({ data: [] });
        mockOctokit.rest.issues.listComments.mockResolvedValue({ data: [] });

        await run(mockCore, mockGithub);

        expect(mockOctokit.rest.issues.createComment).not.toHaveBeenCalled();
        expect(mockCore.info).toHaveBeenCalledWith(expect.stringContaining('Issue #1 has an ignored label. Skipping.'));
    });
});
