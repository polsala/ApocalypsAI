import { EchoManager } from './echoManager';
import { TemporalEcho, ReframedEcho, EchoData } from './types';

const echoManager = new EchoManager();

function displayEcho(echo: EchoData): void {
  console.log(`ID: ${echo.id}`);
  console.log(`  Timestamp: ${new Date(echo.timestamp).toLocaleString()}`);
  console.log(`  Description: ${echo.description}`);
  console.log(`  Impact: ${echo.impact}`);
  console.log(`  Status: ${echo.status}`);
  if (echo.status === 'reframed') {
    const reframed = echo as ReframedEcho;
    console.log(`  Reframed On: ${new Date(reframed.reframedTimestamp).toLocaleString()}`);
    console.log(`  Lesson: ${reframed.lesson}`);
    console.log(`  Action: ${reframed.action}`);
  }
  console.log('---');
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'log':
      const description = args[1];
      const impact = args[2];
      if (!description || !impact) {
        console.error('Usage: npm start log \"<description>\" \"<impact>\"');
        process.exit(1);
      }
      const newEcho = echoManager.logEcho(description, impact);
      console.log('Temporal Echo logged successfully:');
      displayEcho(newEcho);
      break;

    case 'reframe':
      const idToReframe = args[1];
      const lesson = args[2];
      const action = args[3];
      if (!idToReframe || !lesson || !action) {
        console.error('Usage: npm start reframe <echo_id> \"<lesson>\" \"<action>\"');
        process.exit(1);
      }
      const reframed = echoManager.reframeEcho(idToReframe, lesson, action);
      if (reframed) {
        console.log('Temporal Echo reframed successfully:');
        displayEcho(reframed);
      } else {
        console.error(`Error: Echo with ID \"${idToReframe}\" not found or already reframed.`);
        process.exit(1);
      }
      break;

    case 'list':
      const filter = args[1] as 'raw' | 'reframed' | undefined;
      const echoes = echoManager.listEchoes(filter);
      if (echoes.length === 0) {
        console.log(`No temporal echoes found${filter ? ` with status \"${filter}\"` : ''}.`);
      } else {
        console.log(`Temporal Echoes (${filter || 'all'}):`);
        echoes.forEach(displayEcho);
      }
      break;

    case 'help':
    default:
      console.log('ApocalypsAI Nightly Echo Reframe CLI');
      console.log('\nCommands:');
      console.log('  log \"<description>\" \"<impact>\"   - Log a new raw temporal echo.');
      console.log('  reframe <echo_id> \"<lesson>\" \"<action>\" - Reframe an existing raw echo.');
      console.log('  list [raw|reframed]            - List all or filtered temporal echoes.');
      console.log('  help                           - Display this help message.');
      break;
  }
}

main();
