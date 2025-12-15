const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Mock test data
const testWorkflow = {
  name: 'Test Workflow',
  jobs: {
    build: {
      name: 'Build Application',
      runs-on: 'ubuntu-latest'
    },
    test: {
      name: 'Run Tests',
      runs-on: 'ubuntu-latest',
      needs: ['build']
    },
    deploy: {
      name: 'Deploy',
      runs-on: 'ubuntu-latest',
      needs: ['test']
    },
    notify: {
      name: 'Send Notifications',
      runs-on: 'ubuntu-latest',
      needs: ['deploy']
    }
  }
};

function extractWorkflowJobs(content) {
  try {
    const workflow = yaml.load(content);
    const jobs = workflow.jobs || {};
    const jobNames = Object.keys(jobs);
    
    let mermaid = 'graph TD\n';
    
    // Add all jobs as nodes
    jobNames.forEach(jobName => {
      const job = jobs[jobName];
      const displayName = job.name || jobName;
      mermaid += `  ${jobName}["${displayName}"]\n`;
    });
    
    // Add dependencies
    jobNames.forEach(jobName => {
      const job = jobs[jobName];
      if (job.needs) {
        const needs = Array.isArray(job.needs) ? job.needs : [job.needs];
        needs.forEach(dep => {
          mermaid += `  ${dep} --> ${jobName}\n`;
        });
      }
    });
    
    return mermaid;
  } catch (e) {
    console.error('Error parsing workflow:', e.message);
    return 'graph TD\n  error["Parse Error"]\n';
  }
}

// Test cases
function runTests() {
  console.log('Running workflow visualization tests...');
  
  // Test 1: Basic workflow with dependencies
  const yamlContent = yaml.dump(testWorkflow);
  const result = extractWorkflowJobs(yamlContent);
  
  console.log('Test 1: Basic workflow');
  console.log('Result:', result);
  
  // Verify expected elements
  const expectedNodes = ['build', 'test', 'deploy', 'notify'];
  const expectedEdges = ['build --> test', 'test --> deploy', 'deploy --> notify'];
  
  let passed = true;
  
  expectedNodes.forEach(node => {
    if (!result.includes(`  ${node}["`)) {
      console.error(`❌ Missing node: ${node}`);
      passed = false;
    }
  });
  
  expectedEdges.forEach(edge => {
    if (!result.includes(edge)) {
      console.error(`❌ Missing edge: ${edge}`);
      passed = false;
    }
  });
  
  if (passed) {
    console.log('✅ Test 1 passed');
  }
  
  // Test 2: Workflow with parallel jobs
  const parallelWorkflow = {
    jobs: {
      lint: { runs-on: 'ubuntu-latest' },
      build: { runs-on: 'ubuntu-latest' },
      test: { runs-on: 'ubuntu-latest', needs: ['lint', 'build'] }
    }
  };
  
  const parallelResult = extractWorkflowJobs(yaml.dump(parallelWorkflow));
  console.log('\nTest 2: Parallel workflow');
  console.log('Result:', parallelResult);
  
  const expectedParallelEdges = ['lint --> test', 'build --> test'];
  let parallelPassed = true;
  
  expectedParallelEdges.forEach(edge => {
    if (!parallelResult.includes(edge)) {
      console.error(`❌ Missing edge: ${edge}`);
      parallelPassed = false;
    }
  });
  
  if (parallelPassed) {
    console.log('✅ Test 2 passed');
  }
  
  // Test 3: Empty workflow
  const emptyResult = extractWorkflowJobs('name: Empty\njobs: {}');
  console.log('\nTest 3: Empty workflow');
  console.log('Result:', emptyResult);
  
  if (emptyResult.includes('graph TD')) {
    console.log('✅ Test 3 passed');
  } else {
    console.error('❌ Test 3 failed: Missing graph declaration');
  }
  
  // Test 4: Invalid YAML
  const invalidResult = extractWorkflowJobs('invalid: yaml: content: [');
  console.log('\nTest 4: Invalid YAML');
  console.log('Result:', invalidResult);
  
  if (invalidResult.includes('error["Parse Error"]')) {
    console.log('✅ Test 4 passed');
  } else {
    console.error('❌ Test 4 failed: Should handle invalid YAML gracefully');
  }
  
  console.log('\nAll tests completed!');
}

runTests();
