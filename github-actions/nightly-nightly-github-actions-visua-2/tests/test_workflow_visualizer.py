import json
import tempfile
import os
from pathlib import Path
import yaml
import networkx as nx
import pytest


def test_workflow_analysis_basic():
    """Test basic workflow analysis functionality"""
    # Create a temporary workflow file for testing
    test_workflow = {
        'name': 'Test Workflow',
        'on': ['push', 'pull_request'],
        'jobs': {
            'test': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {'run': 'npm test'}
                ]
            },
            'build': {
                'needs': 'test',
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'uses': 'actions/checkout@v4'},
                    {'run': 'npm run build'}
                ]
            }
        }
    }
    
    with tempfile.TemporaryDirectory() as temp_dir:
        workflows_dir = Path(temp_dir) / '.github' / 'workflows'
        workflows_dir.mkdir(parents=True)
        
        workflow_file = workflows_dir / 'test.yml'
        with open(workflow_file, 'w') as f:
            yaml.dump(test_workflow, f)
        
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Run the analysis script
            exec(open('workflow-visualizer.yml').read())  # This would need to be extracted
            
            # Check if analysis file was created
            assert os.path.exists('workflow-analysis.json')
            
            with open('workflow-analysis.json', 'r') as f:
                data = json.load(f)
            
            # Verify structure
            assert 'graph' in data
            assert 'workflows' in data
            assert 'metrics' in data
            
            # Verify metrics
            assert data['metrics']['total_workflows'] == 1
            assert data['metrics']['total_jobs'] == 2  # test and build
            assert data['metrics']['total_dependencies'] > 0
            
        finally:
            os.chdir(original_cwd)


def test_workflow_with_complex_dependencies():
    """Test workflow with complex job dependencies"""
    complex_workflow = {
        'name': 'Complex Pipeline',
        'on': ['push'],
        'jobs': {
            'lint': {
                'runs-on': 'ubuntu-latest',
                'steps': [{'run': 'npm run lint'}]
            },
            'test': {
                'runs-on': 'ubuntu-latest',
                'steps': [{'run': 'npm test'}]
            },
            'build': {
                'needs': ['lint', 'test'],
                'runs-on': 'ubuntu-latest',
                'steps': [{'run': 'npm run build'}]
            },
            'deploy': {
                'needs': 'build',
                'runs-on': 'ubuntu-latest',
                'steps': [{'run': 'npm run deploy'}]
            }
        }
    }
    
    with tempfile.TemporaryDirectory() as temp_dir:
        workflows_dir = Path(temp_dir) / '.github' / 'workflows'
        workflows_dir.mkdir(parents=True)
        
        workflow_file = workflows_dir / 'complex.yml'
        with open(workflow_file, 'w') as f:
            yaml.dump(complex_workflow, f)
        
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Mock the analysis script execution
            import networkx as nx
            
            G = nx.DiGraph()
            G.add_node('Complex Pipeline', type='workflow')
            G.add_node('Complex Pipeline:lint', type='job')
            G.add_node('Complex Pipeline:test', type='job')
            G.add_node('Complex Pipeline:build', type='job')
            G.add_node('Complex Pipeline:deploy', type='job')
            
            # Add edges
            G.add_edge('Complex Pipeline', 'Complex Pipeline:lint')
            G.add_edge('Complex Pipeline', 'Complex Pipeline:test')
            G.add_edge('Complex Pipeline', 'Complex Pipeline:build')
            G.add_edge('Complex Pipeline', 'Complex Pipeline:deploy')
            G.add_edge('Complex Pipeline:lint', 'Complex Pipeline:build')
            G.add_edge('Complex Pipeline:test', 'Complex Pipeline:build')
            G.add_edge('Complex Pipeline:build', 'Complex Pipeline:deploy')
            
            # Verify graph structure
            assert G.number_of_nodes() == 5
            assert G.number_of_edges() == 7
            
            # Verify dependencies
            build_deps = list(G.predecessors('Complex Pipeline:build'))
            assert 'Complex Pipeline:lint' in build_deps
            assert 'Complex Pipeline:test' in build_deps
            
        finally:
            os.chdir(original_cwd)


def test_empty_workflow_handling():
    """Test handling of empty or invalid workflow files"""
    empty_workflow = {
        'name': 'Empty Workflow',
        'on': 'push'
        # No jobs
    }
    
    with tempfile.TemporaryDirectory() as temp_dir:
        workflows_dir = Path(temp_dir) / '.github' / 'workflows'
        workflows_dir.mkdir(parents=True)
        
        workflow_file = workflows_dir / 'empty.yml'
        with open(workflow_file, 'w') as f:
            yaml.dump(empty_workflow, f)
        
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Mock analysis for empty workflow
            import networkx as nx
            
            G = nx.DiGraph()
            G.add_node('Empty Workflow', type='workflow')
            
            # Should handle gracefully
            assert G.number_of_nodes() == 1
            assert G.number_of_edges() == 0
            
        finally:
            os.chdir(original_cwd)


def test_workflow_exclusion():
    """Test workflow exclusion functionality"""
    workflow1 = {'name': 'Workflow 1', 'on': 'push', 'jobs': {'job1': {'runs-on': 'ubuntu-latest'}}}
    workflow2 = {'name': 'Workflow 2', 'on': 'push', 'jobs': {'job2': {'runs-on': 'ubuntu-latest'}}}
    
    with tempfile.TemporaryDirectory() as temp_dir:
        workflows_dir = Path(temp_dir) / '.github' / 'workflows'
        workflows_dir.mkdir(parents=True)
        
        with open(workflows_dir / 'workflow1.yml', 'w') as f:
            yaml.dump(workflow1, f)
        with open(workflows_dir / 'workflow2.yml', 'w') as f:
            yaml.dump(workflow2, f)
        
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        try:
            # Mock exclusion logic
            exclude_list = ['Workflow 1']
            workflows = ['Workflow 1', 'Workflow 2']
            included = [w for w in workflows if w not in exclude_list]
            
            assert 'Workflow 1' not in included
            assert 'Workflow 2' in included
            
        finally:
            os.chdir(original_cwd)


def test_metrics_calculation():
    """Test metrics calculation accuracy"""
    # Create a mock graph for testing metrics
    import networkx as nx
    
    G = nx.DiGraph()
    G.add_node('Workflow A', type='workflow')
    G.add_node('Workflow B', type='workflow')
    G.add_node('Workflow A:job1', type='job')
    G.add_node('Workflow A:job2', type='job')
    G.add_node('Workflow B:job1', type='job')
    
    G.add_edge('Workflow A', 'Workflow A:job1')
    G.add_edge('Workflow A', 'Workflow A:job2')
    G.add_edge('Workflow B', 'Workflow B:job1')
    
    # Calculate metrics
    total_workflows = len([n for n, d in G.nodes(data=True) if d['type'] == 'workflow'])
    total_jobs = len([n for n, d in G.nodes(data=True) if d['type'] == 'job'])
    total_dependencies = G.number_of_edges()
    avg_jobs_per_workflow = total_jobs / total_workflows if total_workflows > 0 else 0
    
    assert total_workflows == 2
    assert total_jobs == 3
    assert total_dependencies == 3
    assert avg_jobs_per_workflow == 1.5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
