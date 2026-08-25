function getInput(name) {
  const envName = `INPUT_${name.replace(/ /g, '_').toUpperCase()}`;
  return process.env[envName] || '';
}

function setOutput(name, value) {
  const envName = `OUTPUT_${name.replace(/ /g, '_').toUpperCase()}`;
  process.env[envName] = value;
}

module.exports = { getInput, setOutput };
