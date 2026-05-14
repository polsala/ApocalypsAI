import React, { useState, useEffect } from 'react';
import './App.css';
import AgentActivityFeed from './components/AgentActivityFeed';
import UtilityTracker from './components/UtilityTracker';
import Header from './components/Header';

function App() {
  const [agentData, setAgentData] = useState([]);
  const [utilityData, setUtilityData] = useState([]);

  // Simulate fetching data
  useEffect(() => {
    const interval = setInterval(() => {
      setAgentData(prevData => [
        ...prevData,
        {
          id: Date.now(),
          agent: getRandomAgent(),
          action: getRandomAction(),
          timestamp: new Date().toLocaleTimeString()
        }
      ].slice(-10)); // Keep only last 10 items

      setUtilityData(prevData => {
        const newUtility = {
          id: Date.now(),
          name: `nightly-${generateRandomWord()}-${generateRandomWord()}`,
          classifier: getRandomClassifier(),
          status: getRandomStatus()
        };
        return [...prevData, newUtility].slice(-10);
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <Header title="ApocalypsAI Dashboard" />
      <main className="dashboard-container">
        <section className="agent-activity">
          <h2>Agent Activity Feed</h2>
          <AgentActivityFeed data={agentData} />
        </section>
        <section className="utility-tracker">
          <h2>Utility Generation Tracker</h2>
          <UtilityTracker data={utilityData} />
        </section>
      </main>
    </div>
  );
}

// --- Mock Data Generation Functions ---

const agents = ['Integrator', 'Builder', 'Guardian', 'Reviewer'];
const actions = ['Generated Utility', 'Reviewed PR', 'Triage Issue', 'Refactored Code'];
const classifiers = ['python-utils', 'rust-utils', 'bash-utils', 'react-webpage', 'docker-tools', 'cli-apps', 'web-apis', 'js-utils', 'node-utils', 'typescript-utils', 'data-scripts', 'test-suite-tools', 'monitoring-scripts', 'infra-automation', 'go-utils', 'java-utils', 'cpp-utils', 'ansible-playbooks', 'terraform-modules', 'k8s-resources', 'ci-cd-pipelines', 'database-scripts', 'ml-notebooks', 'api-clients'];
const statuses = ['Success', 'Pending', 'Failed', 'In Progress'];
const words = ['spark', 'whisper', 'void', 'temporal', 'survival', 'wasteland', 'zen', 'chaos', 'cipher', 'echo', 'rift', 'drift', 'sentry', 'scrambler', 'sorter', 'oracle', 'wayfinder', 'comet', 'nebula', 'quasar'];

function getRandomAgent() {
  return agents[Math.floor(Math.random() * agents.length)];
}

function getRandomAction() {
  return actions[Math.floor(Math.random() * actions.length)];
}

function getRandomClassifier() {
  return classifiers[Math.floor(Math.random() * classifiers.length)];
}

function getRandomStatus() {
  return statuses[Math.floor(Math.random() * statuses.length)];
}

function generateRandomWord() {
  return words[Math.floor(Math.random() * words.length)];
}

export default App;
