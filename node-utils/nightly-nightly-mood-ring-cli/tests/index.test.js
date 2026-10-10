const sinon = require('sinon');
const assert = require('assert');
const chalk = require('chalk'); // Import chalk to compare colored output
const { getMood, moodMap, defaultMood } = require('../src/index');

// Mock rationale: We need to control user input for prompts and capture console output
// to make tests deterministic and offline. Sinon.js is used to stub 'prompts' and 'console.log'.
describe('Nightly Mood Ring CLI', () => {
  let promptsStub;
  let consoleLogStub;

  beforeEach(() => {
    // Stub prompts to control user input
    promptsStub = sinon.stub(require('prompts'), 'prompt');
    // Stub console.log to capture output
    consoleLogStub = sinon.stub(console, 'log');
  });

  afterEach(() => {
    promptsStub.restore();
    consoleLogStub.restore();
  });

  it('should display Radiant Ruby for happy input', async () => {
    promptsStub.returns(Promise.resolve({ feeling: 'I am feeling very happy today!' }));
    await getMood();
    assert(consoleLogStub.calledWith(chalk.bold('✨ Nightly Mood Ring ✨')));
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.red('Radiant Ruby (Happy and energetic!)')}`));
  });

  it('should display Melancholy Sapphire for sad input', async () => {
    promptsStub.returns(Promise.resolve({ feeling: 'Feeling a bit sad and blue.' }));
    await getMood();
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.blue('Melancholy Sapphire (Feeling a bit sad or reflective.)')}`));
  });

  it('should display Volatile Vermilion for angry input', async () => {
    promptsStub.returns(Promise.resolve({ feeling: 'I am so frustrated with this situation!' }));
    await getMood();
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.hex('#FF4500')('Volatile Vermilion (Feeling agitated or frustrated.)')}`));
  });

  it('should display Serene Emerald for calm input', async () => {
    promptsStub.returns(Promise.resolve({ feeling: 'Everything is calm and peaceful.' }));
    await getMood();
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.green('Serene Emerald (Feeling peaceful and calm.)')}`));
  });

  it('should display Mystic Amethyst for confused input', async () => {
    promptsStub.returns(Promise.resolve({ feeling: 'I am so confused about what to do.' }));
    await getMood();
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.magenta('Mystic Amethyst (Feeling confused or uncertain.)')}`));
  });

  it('should display Curious Citrine for curious input', async () => {
    promptsStub.returns(Promise.resolve({ feeling: 'I am curious about new things.' }));
    await getMood();
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.yellow('Curious Citrine (Feeling inquisitive and engaged.)')}`));
  });

  it('should display Anxious Garnet for anxious input', async () => {
    promptsStub.returns(Promise.resolve({ feeling: 'Feeling very anxious and stressed.' }));
    await getMood();
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.hex('#8B0000')('Anxious Garnet (Feeling stressed or worried.)')}`));
  });

  it('should display Content Aquamarine for content input', async () => {
    promptsStub.returns(Promise.resolve({ feeling: 'I feel content and satisfied.' }));
    await getMood();
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.cyan('Content Aquamarine (Feeling satisfied and at ease.)')}`));
  });

  it('should display Apathetic Ash for bored input', async () => {
    promptsStub.returns(Promise.resolve({ feeling: 'This is so dull and boring.' }));
    await getMood();
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.grey('Apathetic Ash (Feeling bored or uninspired.)')}`));
  });

  it('should display Loving Rose Quartz for love input', async () => {
    promptsStub.returns(Promise.resolve({ feeling: 'I feel love for everyone.' }));
    await getMood();
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.hex('#FF69B4')('Loving Rose Quartz (Feeling affectionate and warm.)')}`));
  });

  it('should display Shifting Quartz for neutral or unrecognized input', async () => {
    promptsStub.returns(Promise.resolve({ feeling: 'The weather is okay today.' }));
    await getMood();
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.white('Shifting Quartz (Neutral, adaptable, or uncertain.)')}`));
  });

  it('should display Shifting Quartz for empty input', async () => {
    promptsStub.returns(Promise.resolve({ feeling: '' }));
    await getMood();
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.white('Shifting Quartz (Neutral, adaptable, or uncertain.)')}`));
  });

  it('should display Shifting Quartz if prompts returns no feeling', async () => {
    promptsStub.returns(Promise.resolve({})); // Simulate user pressing Ctrl+C or similar
    await getMood();
    assert(consoleLogStub.calledWith(`Your mood is: ${chalk.white('Shifting Quartz (Neutral, adaptable, or uncertain.)')}`));
  });
});
