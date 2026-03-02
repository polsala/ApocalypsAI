import { parseScrapedDate, runCli } from '../src/index';
import { ScrapedDate, Confidence } from '../src/types';

// Mock console.log and console.error for CLI tests
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});

describe('parseScrapedDate', () => {
  beforeEach(() => {
    // Reset mocks before each test
    mockConsoleLog.mockClear();
    mockConsoleError.mockClear();
  });

  // # Mock rationale:
  // We are testing the parsing logic and confidence assignment. The `Date` object
  // is a standard built-in, and its behavior for parsing common absolute date formats
  // is generally consistent across Node.js environments. We are not mocking `Date` itself,
  // but rather ensuring our wrapper `isValidDate` and the heuristic confidence assignment
  // work as expected with various inputs that `Date` can or cannot parse. For CLI tests,
  // `console.log` and `console.error` are mocked to capture output without affecting the console.

  it('should parse ISO 8601 date with High confidence (UTC)', () => {
    const dateString = '2023-10-27T10:00:00Z';
    const result = parseScrapedDate(dateString);
    expect(result.original).toBe(dateString);
    expect(result.parsed?.getTime()).toBe(new Date(dateString).getTime());
    expect(result.confidence).toBe('High');
    expect(result.error).toBeUndefined();
  });

  it('should parse YYYY-MM-DD HH:mm:ss with High confidence (Local)', () => {
    const dateString = '2023-10-27 14:30:00';
    const result = parseScrapedDate(dateString);
    expect(result.original).toBe(dateString);
    // Compare getTime() for local dates to avoid timezone display differences
    expect(result.parsed?.getTime()).toBe(new Date(2023, 9, 27, 14, 30, 0).getTime());
    expect(result.confidence).toBe('High');
  });

  it('should parse YYYY/MM/DD with High confidence (Local)', () => {
    const dateString = '2024/01/15';
    const result = parseScrapedDate(dateString);
    expect(result.original).toBe(dateString);
    expect(result.parsed?.getTime()).toBe(new Date(2024, 0, 15).getTime());
    expect(result.confidence).toBe('High');
  });

  it('should parse RFC 2822 format with High confidence (UTC)', () => {
    const dateString = 'Thu, 01 Jan 1970 00:00:00 GMT';
    const result = parseScrapedDate(dateString);
    expect(result.original).toBe(dateString);
    expect(result.parsed?.getTime()).toBe(new Date(dateString).getTime());
    expect(result.confidence).toBe('High');
  });

  it('should parse MM/DD/YYYY with Medium confidence (Local)', () => {
    const dateString = '10/27/2023';
    const result = parseScrapedDate(dateString);
    expect(result.original).toBe(dateString);
    expect(result.parsed?.getTime()).toBe(new Date(2023, 9, 27).getTime());
    expect(result.confidence).toBe('Medium');
  });

  it('should parse Month DD, YYYY with Medium confidence (Local)', () => {
    const dateString = 'October 27, 2023';
    const result = parseScrapedDate(dateString);
    expect(result.original).toBe(dateString);
    expect(result.parsed?.getTime()).toBe(new Date(2023, 9, 27).getTime());
    expect(result.confidence).toBe('Medium');
  });

  it('should parse MM-DD-YY with Medium confidence (ambiguous year, Local)', () => {
    const dateString = '01-02-23'; // Typically resolves to 2023-01-02 in local time
    const result = parseScrapedDate(dateString);
    expect(result.original).toBe(dateString);
    expect(result.parsed?.getTime()).toBe(new Date(2023, 0, 2).getTime());
    expect(result.confidence).toBe('Medium');
  });

  it('should parse a less common but valid date string with Low confidence (Local)', () => {
    const dateString = '27 Oct 2023'; // Not explicitly covered by High/Medium regexes, but Date.parse handles it.
    const result = parseScrapedDate(dateString);
    expect(result.original).toBe(dateString);
    expect(result.parsed?.getTime()).toBe(new Date(2023, 9, 27).getTime());
    expect(result.confidence).toBe('Low');
  });

  it('should return None confidence for an unparseable string', () => {
    const dateString = 'not a date string at all';
    const result = parseScrapedDate(dateString);
    expect(result.original).toBe(dateString);
    expect(result.parsed).toBeNull();
    expect(result.confidence).toBe('None');
    expect(result.error).toBe('Could not parse date string.');
  });

  it('should handle empty string with None confidence', () => {
    const dateString = '';
    const result = parseScrapedDate(dateString);
    expect(result.original).toBe(dateString);
    expect(result.parsed).toBeNull();
    expect(result.confidence).toBe('None');
    expect(result.error).toBe('Could not parse date string.');
  });

  it('should handle whitespace-only string with None confidence', () => {
    const dateString = '   ';
    const result = parseScrapedDate(dateString);
    expect(result.original).toBe(dateString);
    expect(result.parsed).toBeNull();
    expect(result.confidence).toBe('None');
    expect(result.error).toBe('Could not parse date string.');
  });
});

describe('runCli', () => {
  beforeEach(() => {
    mockConsoleLog.mockClear();
    mockConsoleError.mockClear();
  });

  it('should print usage when no arguments are provided', () => {
    runCli([]);
    expect(mockConsoleLog).toHaveBeenCalledWith("Usage: npm start <date_string>");
    expect(mockConsoleLog).toHaveBeenCalledWith("Example: npm start '2023-10-27 14:30:00'");
    expect(mockConsoleLog).toHaveBeenCalledWith("Example: npm start 'Oct 27, 2023'");
    expect(mockConsoleLog).toHaveBeenCalledTimes(3);
    expect(mockConsoleError).not.toHaveBeenCalled();
  });

  it('should parse and print result for a valid date string', () => {
    const dateString = '2023-11-05 10:00:00';
    const expectedDate = new Date(dateString);
    runCli([dateString]);

    expect(mockConsoleLog).toHaveBeenCalledWith(`Original: "${dateString}"`);
    expect(mockConsoleLog).toHaveBeenCalledWith(`Parsed: ${expectedDate.toISOString()}`);
    expect(mockConsoleLog).toHaveBeenCalledWith('Confidence: High');
    expect(mockConsoleLog).toHaveBeenCalledTimes(3);
    expect(mockConsoleError).not.toHaveBeenCalled();
  });

  it('should parse and print result for an unparseable date string', () => {
    const dateString = 'invalid date';
    runCli([dateString]);

    expect(mockConsoleLog).toHaveBeenCalledWith(`Original: "${dateString}"`);
    expect(mockConsoleLog).toHaveBeenCalledWith('Parsed: N/A');
    expect(mockConsoleLog).toHaveBeenCalledWith('Confidence: None');
    expect(mockConsoleError).toHaveBeenCalledWith('Error: Could not parse date string.');
    expect(mockConsoleLog).toHaveBeenCalledTimes(3);
    expect(mockConsoleError).toHaveBeenCalledTimes(1);
  });

  it('should handle multi-word date strings correctly', () => {
    const dateString = 'December 25, 2024 12:00 PM';
    const expectedDate = new Date(dateString);
    runCli(['December', '25,', '2024', '12:00', 'PM']);

    expect(mockConsoleLog).toHaveBeenCalledWith(`Original: "${dateString}"`);
    expect(mockConsoleLog).toHaveBeenCalledWith(`Parsed: ${expectedDate.toISOString()}`);
    expect(mockConsoleLog).toHaveBeenCalledWith('Confidence: Medium');
    expect(mockConsoleLog).toHaveBeenCalledTimes(3);
    expect(mockConsoleError).not.toHaveBeenCalled();
  });
});
