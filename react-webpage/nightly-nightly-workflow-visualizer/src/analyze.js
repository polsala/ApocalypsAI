// CLI tool to analyze GitHub Actions workflows and generate dependency graphs
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const { program } = require('commander');

// Mock js-yaml for testing
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

// Mock fs for testing
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

// Use mocks in test environment
const yamlModule = process.env.NODE_ENV === 'test' ? mockYaml : yaml;
const fsModule = process.env.NODE_ENV === 'test' ? mockFs : fs;

function parseWorkflowDependencies(workflow) {
  const jobs = workflow.jobs || {};
  const nodes = [];
  const edges = [];
  
  // Create nodes for each job
  Object.keys(jobs).forEach(jobName => {
    const job = jobs[jobName];
    nodes.push({
      id: jobName,
      name: jobName,
      type: 'job',
      steps: job.steps ? job.steps.length : 0,
      runsOn: job['runs-on'] || 'unknown'
    });
    
    // Create edges for dependencies
    if (job.needs) {
      const needs = Array.isArray(job.needs) ? job.needs : [job.needs];
      needs.forEach(dep => {
        edges.push({
          source: dep,
          target: jobName,
          type: 'dependency'
        });
      });
    }
  });
  
  return { nodes, edges };
}

function analyzeWorkflows(workflowsDir) {
  const workflows = [];
  
  try {
    const files = fsModule.readdirSync(workflowsDir);
    const workflowFiles = files.filter(file => file.endsWith('.yml') || file.endsWith('.yaml'));
    
    workflowFiles.forEach(file => {
      try {
        const content = fsModule.readFileSync(path.join(workflowsDir, file), 'utf8');
        const workflow = yamlModule.load(content);
        
        if (workflow && workflow.jobs) {
          const deps = parseWorkflowDependencies(workflow);
          workflows.push({
            filename: file,
            name: workflow.name || file,
            jobs: Object.keys(workflow.jobs).length,
            dependencies: deps
          });
        }
      } catch (error) {
        console.warn(`Failed to parse ${file}: ${error.message}`);
      }
    });
    
  } catch (error) {
    console.error(`Failed to read workflows directory: ${error.message}`);
    process.exit(1);
  }
  
  return workflows;
}

function generateGraphData(workflows) {
  const allNodes = [];
  const allEdges = [];
  
  workflows.forEach(workflow => {
    workflow.dependencies.nodes.forEach(node => {
      allNodes.push({
        ...node,
        workflow: workflow.name
      });
    });
    
    workflow.dependencies.edges.forEach(edge => {
      allEdges.push({
        ...edge,
        workflow: workflow.name
      });
    });
  });
  
  return {
    nodes: allNodes,
    edges: allEdges,
    workflows: workflows.length
  };
}

function generateHTML(graphData) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workflow Dependency Visualizer</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px; background: #f6f8fa; }
        .header { margin-bottom: 20px; }
        .stats { display: flex; gap: 20px; margin-bottom: 20px; }
        .stat { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        #graph { width: 100%; height: 600px; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .controls { margin-bottom: 10px; }
        .legend { display: flex; gap: 15px; font-size: 12px; color: #666; }
        .legend-item { display: flex; align-items: center; gap: 5px; }
        .legend-color { width: 12px; height: 12px; border-radius: 50%; }
    </style>
    <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
    <div class="header">
        <h1>GitHub Actions Workflow Visualizer</h1>
        <div class="stats">
            <div class="stat">
                <strong>${graphData.nodes.length}</strong> Jobs
            </div>
            <div class="stat">
                <strong>${graphData.edges.length}</strong> Dependencies
            </div>
            <div class="stat">
                <strong>${graphData.workflows}</strong> Workflows
            </div>
        </div>
    </div>
    
    <div class="controls">
        <div class="legend">
            <div class="legend-item"><div class="legend-color" style="background: #3b82f6;"></div> Jobs</div>
            <div class="legend-item"><div class="legend-color" style="background: #ef4444;"></div> Dependencies</div>
            <div class="legend-item"><div class="legend-color" style="background: #10b981;"></div> Parallel</div>
        </div>
    </div>
    
    <div id="graph"></div>
    
    <script>
        const data = ${JSON.stringify(graphData)};
        
        const svg = d3.select("#graph")
            .append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", [0, 0, 800, 600]);
        
        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.edges).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(400, 300))
            .force("collide", d3.forceCollide(30));
        
        const link = svg.append("g")
            .selectAll("line")
            .data(data.edges)
            .join("line")
            .attr("stroke", "#ef4444")
            .attr("stroke-width", 2);
        
        const node = svg.append("g")
            .selectAll("circle")
            .data(data.nodes)
            .join("circle")
            .attr("r", 20)
            .attr("fill", "#3b82f6")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
        
        const label = svg.append("g")
            .selectAll("text")
            .data(data.nodes)
            .join("text")
            .text(d => d.name)
            .attr("text-anchor", "middle")
            .attr("dy", 4)
            .attr("font-size", 10)
            .attr("fill", "#333");
        
        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            
            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
            
            label
                .attr("x", d => d.x)
                .attr("y", d => d.y);
        });
        
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    </script>
</body>
</html>`;
}

// CLI setup
program
  .name('workflow-visualizer')
  .description('Generate interactive dependency graphs for GitHub Actions workflows')
  .version('1.0.0')
  .option('-w, --workflows-dir <dir>', 'Workflows directory', '.github/workflows')
  .option('-o, --output <dir>', 'Output directory', './visualization')
  .option('-f, --format <format>', 'Output format (html|json)', 'html');

program.parse();

const options = program.opts();

// Main execution
function main() {
  const workflowsDir = options.workflowsDir;
  const outputDir = options.output;
  
  if (!fsModule.existsSync(outputDir)) {
    fsModule.mkdirSync(outputDir, { recursive: true });
  }
  
  console.log(`Analyzing workflows in: ${workflowsDir}`);
  const workflows = analyzeWorkflows(workflowsDir);
  const graphData = generateGraphData(workflows);
  
  if (options.format === 'json') {
    const jsonPath = path.join(outputDir, 'workflow-graph.json');
    fsModule.writeFileSync(jsonPath, JSON.stringify(graphData, null, 2));
    console.log(`JSON data saved to: ${jsonPath}`);
  } else {
    const htmlPath = path.join(outputDir, 'index.html');
    const htmlContent = generateHTML(graphData);
    fsModule.writeFileSync(htmlPath, htmlContent);
    console.log(`Visualization saved to: ${htmlPath}`);
    console.log('Open index.html in your browser to view the interactive graph.');
  }
}

// Export for testing
module.exports = {
  parseWorkflowDependencies,
  analyzeWorkflows,
  generateGraphData,
  generateHTML,
  main
};

// Run if not in test environment
if (process.env.NODE_ENV !== 'test') {
  main();
}
