const { getCosmicDirection } = require('../src/index');
const sinon = require('sinon');

describe('Cosmic Compass', () => {
  let clock;

  beforeEach(() => {
    // Mock the Date object to control time for deterministic tests
    const mockDate = new Date('2023-10-27T10:30:00Z'); // 10:30 AM UTC
    clock = sinon.useFakeTimers(mockDate.getTime());
  });

  afterEach(() => {
    clock.restore();
  });

  it('should return a direction string', () => {
    const direction = getCosmicDirection();
    expect(direction).to.be.a('string');
    expect(direction).to.include('Towards the Zenith Sky'); // Based on the mocked time
  });

  it('should include a cosmic event in the direction', () => {
    // Mocking Math.random to ensure a specific event is chosen for this test
    // Mock rationale: To ensure deterministic testing of the event selection.
    const randomStub = sinon.stub(Math, 'random');
    randomStub.onCall(0).returns(0.1); // This should map to 'Nebula Bloom'

    const direction = getCosmicDirection();
    expect(direction).to.include('Nebula Bloom');

    randomStub.restore();
  });

  it('should provide different directions based on time of day (simulated)', () => {
    // Test for morning
    clock.tick(new Date('2023-10-27T04:00:00Z').getTime() - clock.now);
    expect(getCosmicDirection()).to.include('the Dawn Horizon');

    // Test for afternoon
    clock.tick(new Date('2023-10-27T15:00:00Z').getTime() - clock.now);
    expect(getCosmicDirection()).to.include('the Twilight Veil');

    // Test for evening
    clock.tick(new Date('2023-10-27T21:00:00Z').getTime() - clock.now);
    expect(getCosmicDirection()).to.include('the Midnight Expanse');
  });
});
