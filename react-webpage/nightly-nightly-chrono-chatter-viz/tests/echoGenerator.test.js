import { generateEchoes } from '../src/utils/echoGenerator';

describe('generateEchoes', () => {
  it('should return an empty array for an empty message', () => {
    expect(generateEchoes('')).toEqual([]);
    expect(generateEchoes('   ')).toEqual([]);
  });

  it('should generate echoes for a simple message across all factions', () => {
    const message = 'The supplies are low.';
    const echoes = generateEchoes(message);

    expect(echoes).toHaveLength(4); // Assuming 4 factions
    expect(echoes[0].factionName).toBe("Wasteland Scavengers");
    expect(echoes[0].originalMessage).toBe(message);
    expect(echoes[0].echoMessage).toContain("scraps");
    expect(echoes[0].echoMessage).toContain("scarce");
    expect(echoes[0].echoMessage).toContain("Gotta have grit.");

    expect(echoes[1].factionName).toBe("Vault Dwellers (Overseer's Log)");
    expect(echoes[1].originalMessage).toBe(message);
    expect(echoes[1].echoMessage).toContain("provisions");
    expect(echoes[1].echoMessage).toContain("depleted");
    expect(echoes[1].echoMessage).toContain("Protocol 7-Gamma initiated");

    expect(echoes[2].factionName).toBe("Temporal Anomaly Researchers (Field Report)");
    expect(echoes[2].originalMessage).toBe(message);
    expect(echoes[2].echoMessage).toContain("material resources");
    expect(echoes[2].echoMessage).toContain("sub-optimal");
    expect(echoes[2].echoMessage).toContain("chronal integrity");

    expect(echoes[3].factionName).toBe("Whispering Cultists (Prophecy Fragment)");
    expect(echoes[3].originalMessage).toBe(message);
    expect(echoes[3].echoMessage).toContain("offerings");
    expect(echoes[3].echoMessage).toContain("waning");
    expect(echoes[3].echoMessage).toContain("whispers of the void");
  });

  it('should handle different keywords and transformations', () => {
    const message = 'We need help, danger ahead!';
    const echoes = generateEchoes(message);

    expect(echoes[0].echoMessage).toContain("gotta find a hand"); // Scavengers
    expect(echoes[0].echoMessage).toContain("trouble");

    expect(echoes[1].echoMessage).toContain("require assistance"); // Vault Dwellers
    expect(echoes[1].echoMessage).toContain("potential hazard");

    expect(echoes[2].echoMessage).toContain("necessitate acquisition of interventional support"); // Researchers
    expect(echoes[2].echoMessage).toContain("spatio-temporal flux");

    expect(echoes[3].echoMessage).toContain("crave succor"); // Cultists
    expect(echoes[3].echoMessage).toContain("the void's embrace");
  });
});
