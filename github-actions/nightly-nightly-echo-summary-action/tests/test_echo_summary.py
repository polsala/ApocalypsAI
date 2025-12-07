import os
import pytest
from echo_summary import get_repo_stats, generate_echo_text

# Mock rationale: Isolates tests from GitHub API and ensures deterministic results
os.environ['MOCK_ENV'] = 'true'

def test_get_repo_stats():
    stats = get_repo_stats()
    assert stats['prs'] == 14
    assert stats['contributors'] == 7
    assert stats['issues_closed'] == 22
    assert 'Survival Kit' in stats['milestones']

def test_generate_echo_text():
    sample = generate_echo_text({
        'prs': 5,
        'contributors': 3,
        'issues_closed': 8,
        'milestones': ['Test Milestone']
    })
    assert 'PRs Merged: 5' in sample
    assert 'Contributors: 3' in sample
    assert 'Issues Closed: 8' in sample
    assert 'Milestones Achieved: Test Milestone' in sample

if __name__ == "__main__":
    pytest.main([__file__])
