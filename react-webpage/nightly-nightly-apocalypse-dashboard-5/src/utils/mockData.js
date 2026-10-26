export const generateMockAgentData = (count) => {
  const statuses = ['Active', 'Idle', 'Error', 'Active', 'Idle'];
  const names = [
    'Nightly Shelter Sentry Log', 'Nightly Silly Commit Message Generat',
    'Nightly Survival Cache Checksum Veri', 'Nightly Temporal Anomaly Detector',
    'Nightly Wasteland Resource Tracker', 'Nightly Whispering Walls Log Analyze',
    'Nightly Workflow Sanity Checker', 'Nightly Zen Quote Generator'
  ];

  return Array.from({ length: count }, (_, i) => ({
    id: i,
    name: names[i % names.length] + ` (${i + 1})`,
    status: statuses[Math.floor(Math.random() * statuses.length)]
  }));
};

export const generateMockWorkflowData = () => {
  const statuses = ['Success', 'Failure', 'Running', 'Success', 'Success'];
  return {
    status: statuses[Math.floor(Math.random() * statuses.length)]
  };
};
