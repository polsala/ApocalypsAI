const os = require('os');
const { getCpuProphecy, getMemoryVision, divine } = require('../src/index');

// Mock rationale: We need to control system resource values (CPU load, memory usage)
// to deterministically test the prophecy and vision generation logic without
// relying on the actual, variable system state. This ensures tests are fast,
// reliable, and isolated.

describe('Nightly Digital Diviner', () => {
  let consoleSpy;

  beforeEach(() => {
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleSpy.mockRestore();
    jest.restoreAllMocks();
  });

  describe('getCpuProphecy', () => {
    it('should return high load prophecy for normalized load > 0.8', () => {
      expect(getCpuProphecy(0.9)).toContain('Oracle of Overload');
    });

    it('should return moderate load prophecy for normalized load between 0.3 and 0.8', () => {
      expect(getCpuProphecy(0.5)).toContain('Oracle of Efficiency');
      expect(getCpuProphecy(0.3)).toContain('Oracle of Efficiency');
      expect(getCpuProphecy(0.8)).toContain('Oracle of Efficiency');
    });

    it('should return low load prophecy for normalized load < 0.3', () => {
      expect(getCpuProphecy(0.1)).toContain('Oracle of Potential');
    });
  });

  describe('getMemoryVision', () => {
    it('should return high memory vision for usage ratio > 0.8', () => {
      expect(getMemoryVision(0.9)).toContain('Oracle of Retention');
    });

    it('should return moderate memory vision for usage ratio between 0.3 and 0.8', () => {
      expect(getMemoryVision(0.5)).toContain('Oracle of Clarity');
      expect(getMemoryVision(0.3)).toContain('Oracle of Clarity');
      expect(getMemoryVision(0.8)).toContain('Oracle of Clarity');
    });

    it('should return low memory vision for usage ratio < 0.3', () => {
      expect(getMemoryVision(0.1)).toContain('Oracle of Expansion');
    });
  });

  describe('divine', () => {
    it('should print prophecies for high CPU and high memory', () => {
      jest.spyOn(os, 'cpus').mockReturnValue([{ model: 'CPU', speed: 1000 }]); // Mock 1 CPU
      jest.spyOn(os, 'loadavg').mockReturnValue([1.0, 0.5, 0.2]); // Mock 1-min load avg of 1.0
      jest.spyOn(os, 'totalmem').mockReturnValue(1000000000); // 1 GB
      jest.spyOn(os, 'freemem').mockReturnValue(100000000); // 100 MB free (90% used)

      divine();

      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('🌌 The Nightly Digital Diviner speaks! 🌌'));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("CPU Prophecy: The processing core hums with an urgent, frantic energy. The Oracle of Overload whispers: 'Seek respite, lest the circuits melt into digital slag!'"));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("Memory Vision: The memory banks groan under the weight of accumulated data. The Oracle of Retention warns: 'Unburden your mind, clear the caches, or risk the collapse of thought!'"));
    });

    it('should print prophecies for moderate CPU and moderate memory', () => {
      jest.spyOn(os, 'cpus').mockReturnValue([{ model: 'CPU', speed: 1000 }]); // Mock 1 CPU
      jest.spyOn(os, 'loadavg').mockReturnValue([0.5, 0.5, 0.2]); // Mock 1-min load avg of 0.5
      jest.spyOn(os, 'totalmem').mockReturnValue(1000000000); // 1 GB
      jest.spyOn(os, 'freemem').mockReturnValue(500000000); // 500 MB free (50% used)

      divine();

      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('🌌 The Nightly Digital Diviner speaks! 🌌'));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("CPU Prophecy: The computational gears turn with a steady, purposeful rhythm. The Oracle of Efficiency nods: 'Your efforts are well-paced, survivor. Maintain this balance.'"));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("Memory Vision: Memory flows like a well-tended spring. The Oracle of Clarity smiles: 'Your digital mind is sharp and ready. Proceed with purpose.'"));
    });

    it('should print prophecies for low CPU and low memory', () => {
      jest.spyOn(os, 'cpus').mockReturnValue([{ model: 'CPU', speed: 1000 }]); // Mock 1 CPU
      jest.spyOn(os, 'loadavg').mockReturnValue([0.1, 0.5, 0.2]); // Mock 1-min load avg of 0.1
      jest.spyOn(os, 'totalmem').mockReturnValue(1000000000); // 1 GB
      jest.spyOn(os, 'freemem').mockReturnValue(900000000); // 900 MB free (10% used)

      divine();

      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('🌌 The Nightly Digital Diviner speaks! 🌌'));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("CPU Prophecy: A profound stillness settles upon the processing plains. The Oracle of Potential declares: 'The digital canvas is blank. What grand design will you manifest next?'"));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("Memory Vision: The memory void stretches, vast and inviting. The Oracle of Expansion beckons: 'Embrace new knowledge, for there is ample space for growth!'"));
    });

    it('should handle multi-core CPUs correctly for normalized load', () => {
      jest.spyOn(os, 'cpus').mockReturnValue([{}, {}, {}, {}]); // Mock 4 CPUs
      jest.spyOn(os, 'loadavg').mockReturnValue([3.0, 2.0, 1.0]); // Load avg 3.0 on 4 cores -> normalized 0.75 (moderate)
      jest.spyOn(os, 'totalmem').mockReturnValue(1000000000);
      jest.spyOn(os, 'freemem').mockReturnValue(500000000);

      divine();

      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("CPU Prophecy: The computational gears turn with a steady, purposeful rhythm. The Oracle of Efficiency nods: 'Your efforts are well-paced, survivor. Maintain this balance.'"));
    });
  });
});
