const { generateForecast, main } = require('../src/main');
const fs = require('fs').promises;
const path = require('path');

// Mock rationale: We need to ensure tests are deterministic and offline.
// Mocking `fs.promises.readFile` allows us to control the input environmental data
// without relying on actual file system operations or external resources.
jest.mock('fs', () => ({
    promises: {
        readFile: jest.fn(),
    },
}));

describe('Whisperwind Weather Vane', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        // Mock console.log to prevent actual output during tests
        jest.spyOn(console, 'log').mockImplementation(() => {});
        jest.spyOn(console, 'error').mockImplementation(() => {});
        jest.spyOn(process, 'exit').mockImplementation(() => {
            throw new Error('process.exit was called'); // Throw to stop execution flow in test
        });
    });

    afterEach(() => {
        jest.restoreAllMocks();
    });

    describe('generateForecast', () => {
        test('should generate a forecast for mild, stable conditions', () => {
            const envData = {
                temperature: 20,
                radiation_level: 0.05,
                anomaly_index: 0.1,
                wind_speed: 10,
                temporal_stability: 0.9
            };
            const forecast = generateForecast(envData);
            expect(forecast).toContain("Mild currents drift across the wasteland.");
            expect(forecast).toContain("Radiation levels are stable, offering clear skies (of sorts).");
            expect(forecast).toContain("Temporal currents are unusually calm.");
            expect(forecast).toContain("Gentle breezes stir the dust.");
            expect(forecast).toContain("The timeline holds firm, for now.");
        });

        test('should generate a forecast for harsh, unstable conditions', () => {
            const envData = {
                temperature: 40,
                radiation_level: 0.6,
                anomaly_index: 0.8,
                wind_speed: 50,
                temporal_stability: 0.2
            };
            const forecast = generateForecast(envData);
            expect(forecast).toContain("A Scorching Aura permeates the atmosphere.");
            expect(forecast).toContain("High radiation levels suggest a Blight Bloom on the horizon.");
            expect(forecast).toContain("Expect significant Temporal Distortions and reality ripples.");
            expect(forecast).toContain("Beware the Gale-Force Whispers, they carry dust and secrets.");
            expect(forecast).toContain("The fabric of time feels thin; prepare for unexpected echoes.");
        });

        test('should generate a forecast for cold, moderate conditions', () => {
            const envData = {
                temperature: -5,
                radiation_level: 0.2,
                anomaly_index: 0.4,
                wind_speed: 25,
                temporal_stability: 0.5
            };
            const forecast = generateForecast(envData);
            expect(forecast).toContain("The air bites with a Frost-Kissed Chill.");
            expect(forecast).toContain("A faint, shimmering Radiant Haze is present.");
            expect(forecast).toContain("Minor Chrono-Flickers might be observed.");
            expect(forecast).toContain("A brisk Wind-Scour sweeps across the plains.");
            expect(forecast).toContain("Temporal eddies are active, causing minor temporal drizzle.");
        });
    });

    describe('main', () => {
        const mockEnvData = {
            temperature: 15,
            radiation_level: 0.01,
            anomaly_index: 0.02,
            wind_speed: 5,
            temporal_stability: 0.95
        };

        test('should read default file and log forecast', async () => {
            fs.promises.readFile.mockResolvedValueOnce(JSON.stringify(mockEnvData));

            await main();

            expect(fs.promises.readFile).toHaveBeenCalledWith(path.join(__dirname, '..', 'data', 'environment.json'), 'utf8');
            expect(console.log).toHaveBeenCalledWith("Whisperwind Weather Vane Forecast:");
            expect(console.log).toHaveBeenCalledWith(expect.stringContaining("Mild currents drift across the wasteland."));
        });

        test('should read specified file and log forecast', async () => {
            const customPath = '/tmp/custom_env.json';
            fs.promises.readFile.mockResolvedValueOnce(JSON.stringify(mockEnvData));

            await main(customPath);

            expect(fs.promises.readFile).toHaveBeenCalledWith(customPath, 'utf8');
            expect(console.log).toHaveBeenCalledWith(expect.stringContaining("Mild currents drift across the wasteland."));
        });

        test('should log error and exit if file not found', async () => {
            const errorMessage = 'File not found';
            fs.promises.readFile.mockRejectedValueOnce(new Error(errorMessage));

            await expect(main('nonexistent.json')).rejects.toThrow('process.exit was called');
            expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Error reading or parsing environment data'), expect.stringContaining(errorMessage));
            expect(process.exit).toHaveBeenCalledWith(1);
        });

        test('should log error and exit if JSON is invalid', async () => {
            const invalidJson = '{ "temperature": 20, "radiation_level": }';
            fs.promises.readFile.mockResolvedValueOnce(invalidJson);

            await expect(main()).rejects.toThrow('process.exit was called');
            expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Error reading or parsing environment data'), expect.stringContaining('Unexpected token } in JSON at position'));
            expect(process.exit).toHaveBeenCalledWith(1);
        });
    });
});
