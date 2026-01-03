const assert = require('assert');
const {
  parseWorkflowDependencies,
  analyzeWorkflows,
  generateGraphData,
  generateHTML
} = require('../src/analyze');

// Mock dependencies for testing
const mockYaml = {
  load: (content) => {
    // Mock rationale: Simulate YAML parsing for workflow files
    if (content.includes('nightly_self_heal.yml')) {
      return {
        name: 'Nightly Self Heal',
        jobs: {
          check: { runs-on: 'ubuntu-latest', steps: [{ run: 'echo check' }] },
          fix: { runs-on: 'ubuntu-latest', needs: ['check'], steps: [{ run: 'echo fix' }] },
          notify: { runs-on: 'ubuntu-latest', needs: ['fix'], steps: [{ run: 'echo notify' }] }
        }
      };
    }
    return { name: 'Test Workflow', jobs: {} };
  }
};

const mockFs = {
  readdirSync: (dir) => {
    // Mock rationale: Simulate finding workflow files
    return ['nightly_self_heal.yml', 'test_workflow.yml'];
  },
  readFileSync: (file) => {
    // Mock rationale: Return mock YAML content
    return 'mock yaml content';
  },
  writeFileSync: (file, content) => {
    // Mock rationale: Simulate writing output files
    console.log(`Would write to: ${file}`);
  }
};

// Override modules for testing
const originalYaml = require('js-yaml');
const originalFs = require('fs');

// Test parseWorkflowDependencies
function testParseWorkflowDependencies() {
  console.log('Testing parseWorkflowDependencies...');
  
  const mockWorkflow = {
    jobs: {
      job1: { runs-on: 'ubuntu-latest', steps: [{ run: 'echo 1' }] },
      job2: { runs-on: 'ubuntu-latest', needs: ['job1'], steps: [{ run: 'echo 2' }] },
      job3: { runs-on: 'ubuntu-latest', needs: ['job1'], steps: [{ run: 'echo 3' }] }
    }
  };
  
  const result = parseWorkflowDependencies(mockWorkflow);
  
  assert.strictEqual(result.nodes.length, 3, 'Should have 3 nodes');
  assert.strictEqual(result.edges.length, 2, 'Should have 2 edges');
  
  const job1Node = result.nodes.find(n => n.id === 'job1');
  const job2Node = result.nodes.find(n => n.id === 'job2');
  
  assert.strictEqual(job1Node.name, 'job1', 'Node name should match job name');
  assert.strictEqual(job1Node.type, 'job', 'Node type should be job');
  assert.strictEqual(job1Node.steps, 1, 'Node should have correct step count');
  
  const edge1 = result.edges.find(e => e.source === 'job1' && e.target === 'job2');
  assert.notStrictEqual(edge1, undefined, 'Should have edge from job1 to job2');
  assert.strictEqual(edge1.type, 'dependency', 'Edge type should be dependency');
  
  console.log('✓ parseWorkflowDependencies tests passed');
}

// Test analyzeWorkflows
function testAnalyzeWorkflows() {
  console.log('Testing analyzeWorkflows...');
  
  // Mock the modules
  require.cache[require.resolve('js-yaml')] = { exports: mockYaml };
  require.cache[require.resolve('fs')] = { exports: mockFs };
  
  // Reload the module with mocks
  delete require.cache[require.resolve('../src/analyze')];
  const { analyzeWorkflows } = require('../src/analyze');
  
  const workflows = analyzeWorkflows('/mock/workflows');
  
  assert.strictEqual(workflows.length, 2, 'Should analyze 2 workflows');
  
  const mainWorkflow = workflows.find(w => w.name === 'Nightly Self Heal');
  assert.notStrictEqual(mainWorkflow, undefined, 'Should find Nightly Self Heal workflow');
  assert.strictEqual(mainWorkflow.jobs, 3, 'Should have 3 jobs');
  assert.strictEqual(mainWorkflow.dependencies.nodes.length, 3, 'Should have 3 dependency nodes');
  assert.strictEqual(mainWorkflow.dependencies.edges.length, 2, 'Should have 2 dependency edges');
  
  console.log('✓ analyzeWorkflows tests passed');
}

// Test generateGraphData
function testGenerateGraphData() {
  console.log('Testing generateGraphData...');
  
  const mockWorkflows = [
    {
      name: 'Test Workflow',
      dependencies: {
        nodes: [
          { id: 'job1', name: 'job1', type: 'job' },
          { id: 'job2', name: 'job2', type: 'job' }
        ],
        edges: [
          { source: 'job1', target: 'job2', type: 'dependency' }
        ]
      }
    }
  ];
  
  const result = generateGraphData(mockWorkflows);
  
  assert.strictEqual(result.nodes.length, 2, 'Should have 2 nodes total');
  assert.strictEqual(result.edges.length, 1, 'Should have 1 edge total');
  assert.strictEqual(result.workflows, 1, 'Should have 1 workflow');
  
  const node1 = result.nodes.find(n => n.id === 'job1');
  assert.strictEqual(node1.workflow, 'Test Workflow', 'Node should have workflow name');
  
  const edge1 = result.edges.find(e => e.source === 'job1');
  assert.strictEqual(edge1.workflow, 'Test Workflow', 'Edge should have workflow name');
  
  console.log('✓ generateGraphData tests passed');
}

// Test generateHTML
function testGenerateHTML() {
  console.log('Testing generateHTML...');
  
  const mockGraphData = {
    nodes: [
      { id: 'job1', name: 'job1', workflow: 'Test' },
      { id: 'job2', name: 'job2', workflow: 'Test' }
    ],
    edges: [
      { source: 'job1', target: 'job2', workflow: 'Test' }
    ],
    workflows: 1
  };
  
  const html = generateHTML(mockGraphData);
  
  assert(html.includes('GitHub Actions Workflow Visualizer'), 'HTML should include title');
  assert(html.includes('2 Jobs'), 'HTML should show correct job count');
  assert(html.includes('1 Dependencies'), 'HTML should show correct dependency count');
  assert(html.includes('1 Workflows'), 'HTML should show correct workflow count');
  assert(html.includes('d3.v7.min.js'), 'HTML should include D3.js');
  assert(html.includes('JSON.stringify(graphData)'), 'HTML should include graph data');
  
  console.log('✓ generateHTML tests passed');
}

// Run all tests
function runTests() {
  console.log('Running workflow visualizer tests...\n');
  
  try {
    testParseWorkflowDependencies();
    testAnalyzeWorkflows();
    testGenerateGraphData();
    testGenerateHTML();
    
    console.log('\n✅ All tests passed!');
  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    process.exit(1);
  }
}

// Run tests if this file is executed directly
if (require.main === module) {
  runTests();
}

module.exports = { runTests };
