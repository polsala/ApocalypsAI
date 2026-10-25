const { analyzeMood, run } = require('../src/main');
const core = require('@actions/core');
const github = require('@actions/github');

// Mock rationale: We need to mock GitHub Actions toolkit functions and GitHub API calls
// to ensure tests are deterministic and do not make actual network requests.
jest.mock('@actions/core');
jest.mock('@actions/github', () => ({
    getOctokit: jest.fn(() => ({
        rest: {
            issues: {
                createComment: jest.fn()
            }
        }
    })),
    context: {
        repo: {
            owner: 'test-owner',
            repo: 'test-repo'
        },
        eventName: 'issues',
        payload: {
            issue: {
                number: 123,
                title: 'Test Issue Title',
                body: 'This is a test issue body.'
            }
        }
    }
}));

describe('analyzeMood', () => {
    const positive = ['great', 'success'];
    const negative = ['bug', 'failure'];
    const thematic = ['wasteland', 'anomaly'];
    const threshold = 0.1;

    test('should detect positive mood', () => {
        const text = 'This is a great success!';
        const result = analyzeMood(text, positive, negative, thematic, threshold);
        expect(result.mood).toBe('positive');
        expect(result.score).toBe(2);
        expect(result.suggestions).toContain('Your message radiates hope in the desolate future! Keep that spirit alive, survivor!');
    });

    test('should detect negative mood', () => {
        const text = 'Found a critical bug leading to system failure.';
        const result = analyzeMood(text, positive, negative, thematic, threshold);
        expect(result.mood).toBe('negative');
        expect(result.score).toBe(-2);
        expect(result.suggestions).toContain("A tremor of despair detected. Remember, even in the darkest rifts, solutions can be found. Let's rephrase for resilience!");
    });

    test('should detect neutral mood', () => {
        const text = 'This is a neutral statement.';
        const result = analyzeMood(text, positive, negative, thematic, threshold);
        expect(result.mood).toBe('neutral');
        expect(result.score).toBe(0);
        expect(result.suggestions).not.toContain('Your message radiates hope in the desolate future! Keep that spirit alive, survivor!');
        expect(result.suggestions).not.toContain("A tremor of despair detected. Remember, even in the darkest rifts, solutions can be found. Let's rephrase for resilience!");
    });

    test('should detect thematic content', () => {
        const text = 'Scavenging for resources in the wasteland.';
        const result = analyzeMood(text, positive, negative, thematic, threshold);
        expect(result.mood).toBe('thematic');
        expect(result.suggestions).toContain('Excellent thematic integration! Your words resonate with the spirit of ApocalypsAI.');
    });

    test('should suggest thematic improvements if missing', () => {
        const text = 'Working on a new feature.';
        const result = analyzeMood(text, positive, negative, thematic, threshold);
        expect(result.mood).toBe('off-topic');
        expect(result.suggestions).toContain("The void whispers for more thematic flair! Consider adding terms like 'wasteland', 'anomaly', or 'scavenge' to your description.");
    });

    test('should handle mixed sentiment and thematic', () => {
        const text = 'A great success in fixing the anomaly in the wasteland, despite some initial bugs.';
        const result = analyzeMood(text, positive, negative, thematic, threshold);
        expect(result.mood).toBe('positive'); // Positive score (2) - Negative score (1) = 1 > threshold
        expect(result.score).toBe(1);
        expect(result.suggestions).toContain('Excellent thematic integration! Your words resonate with the spirit of ApocalypsAI.');
        expect(result.suggestions).toContain('Your message radiates hope in the desolate future! Keep that spirit alive, survivor!');
    });

    test('should handle empty text', () => {
        const text = '';
        const result = analyzeMood(text, positive, negative, thematic, threshold);
        expect(result.mood).toBe('off-topic'); // No thematic words, no sentiment
        expect(result.score).toBe(0);
        expect(result.suggestions).toContain("The void whispers for more thematic flair! Consider adding terms like 'wasteland', 'anomaly', or 'scavenge' to your description.");
    });
});

describe('run', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        // Reset mocks for each test
        github.context.eventName = 'issues';
        github.context.payload = {
            issue: {
                number: 123,
                title: 'Test Issue Title',
                body: 'This is a test issue body.'
            }
        };
        core.getInput.mockImplementation((name) => {
            switch (name) {
                case 'github-token': return 'mock-token';
                case 'positive-keywords': return 'great, success';
                case 'negative-keywords': return 'bug, failure';
                case 'thematic-keywords': return 'wasteland, anomaly';
                case 'neutral-threshold': return '0.1';
                default: return '';
            }
        });
    });

    test('should post a comment for positive thematic content', async () => {
        github.context.payload.issue.title = 'Great success in the wasteland anomaly!';
        await run();

        expect(core.setOutput).toHaveBeenCalledWith('mood-status', 'positive');
        expect(github.getOctokit().rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 123,
            body: expect.stringContaining('Detected Mood: **Positive**')
        });
        expect(github.getOctokit().rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 123,
            body: expect.stringContaining('Excellent thematic integration! Your words resonate with the spirit of ApocalypsAI.')
        });
        expect(github.getOctokit().rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 123,
            body: expect.stringContaining('Your message radiates hope in the desolate future! Keep that spirit alive, survivor!')
        });
    });

    test('should post a comment for negative off-topic content', async () => {
        github.context.payload.issue.title = 'This is a terrible bug.';
        github.context.payload.issue.body = 'It causes a complete failure.';
        await run();

        expect(core.setOutput).toHaveBeenCalledWith('mood-status', 'negative');
        expect(github.getOctokit().rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 123,
            body: expect.stringContaining('Detected Mood: **Negative**')
        });
        expect(github.getOctokit().rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 123,
            body: expect.stringContaining("A tremor of despair detected. Remember, even in the darkest rifts, solutions can be found. Let's rephrase for resilience!")
        });
        expect(github.getOctokit().rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 123,
            body: expect.stringContaining("The void whispers for more thematic flair! Consider adding terms like 'wasteland', 'anomaly', or 'scavenge' to your description.")
        });
    });

    test('should not post a comment for neutral thematic content without specific suggestions', async () => {
        github.context.payload.issue.title = 'A neutral report on the wasteland.';
        github.context.payload.issue.body = 'Observing the anomaly.';
        await run();

        expect(core.setOutput).toHaveBeenCalledWith('mood-status', 'thematic');
        expect(github.getOctokit().rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 123,
            body: expect.stringContaining('Detected Mood: **Thematic**')
        });
        expect(github.getOctokit().rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 123,
            body: expect.stringContaining('Excellent thematic integration! Your words resonate with the spirit of ApocalypsAI.')
        });
    });

    test('should handle pull_request_target event', async () => {
        github.context.eventName = 'pull_request_target';
        github.context.payload = {
            pull_request: {
                number: 456,
                title: 'PR for a new wasteland feature',
                body: 'This PR introduces a great new feature for resource scavenging.'
            }
        };
        await run();

        expect(core.setOutput).toHaveBeenCalledWith('mood-status', 'positive');
        expect(github.getOctokit().rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 456,
            body: expect.stringContaining('Detected Mood: **Positive**')
        });
        expect(github.getOctokit().rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 456,
            body: expect.stringContaining('Excellent thematic integration! Your words resonate with the spirit of ApocalypsAI.')
        });
        expect(github.getOctokit().rest.issues.createComment).toHaveBeenCalledWith({
            owner: 'test-owner',
            repo: 'test-repo',
            issue_number: 456,
            body: expect.stringContaining('Your message radiates hope in the desolate future! Keep that spirit alive, survivor!')
        });
    });

    test('should set failed if issue/PR number is missing', async () => {
        github.context.payload.issue.number = undefined; // Simulate missing number
        await run();
        expect(core.setFailed).toHaveBeenCalledWith('Could not determine issue or pull request number.');
    });

    test('should set failed on error', async () => {
        core.getInput.mockImplementationOnce(() => { throw new Error('Input error'); });
        await run();
        expect(core.setFailed).toHaveBeenCalledWith('Input error');
    });

    test('should skip if event is not issues or pull_request_target', async () => {
        github.context.eventName = 'push';
        await run();
        expect(core.info).toHaveBeenCalledWith('This action only runs on issues or pull_request_target events. Skipping.');
        expect(core.setOutput).not.toHaveBeenCalled();
        expect(github.getOctokit().rest.issues.createComment).not.toHaveBeenCalled();
    });
});
