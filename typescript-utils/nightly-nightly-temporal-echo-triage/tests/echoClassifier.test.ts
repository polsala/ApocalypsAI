import { triageTemporalEcho } from '../src/echoClassifier';
import { TemporalEcho, EchoCategory } from '../src/types';

describe('triageTemporalEcho', () => {
  // Mock rationale: The triageTemporalEcho function is pure and deterministic.
  // It does not interact with external systems, files, or network.
  // Therefore, no explicit mocking is required beyond providing various string inputs.

  it('should correctly classify a "Minor Glitch" echo', () => {
    const echoMessage = "I'm experiencing a slight lag in my perception.";
    const expected: TemporalEcho = {
      message: echoMessage,
      category: "Minor Glitch",
      stabilizationProtocol: "Recalibrate Chronometer: A brief moment of stillness can realign minor temporal discrepancies. Perhaps a cup of 'Temporal Tea'?"
    };
    expect(triageTemporalEcho(echoMessage)).toEqual(expected);
  });

  it('should classify another "Minor Glitch" echo with a different keyword', () => {
    const echoMessage = "There's a noticeable delay in the system response.";
    const expected: TemporalEcho = {
      message: echoMessage,
      category: "Minor Glitch",
      stabilizationProtocol: "Recalibrate Chronometer: A brief moment of stillness can realign minor temporal discrepancies. Perhaps a cup of 'Temporal Tea'?"
    };
    expect(triageTemporalEcho(echoMessage)).toEqual(expected);
  });

  it('should correctly classify a "Chronal Ripple" echo', () => {
    const echoMessage = "This feeling of déjà vu is getting intense.";
    const expected: TemporalEcho = {
      message: echoMessage,
      category: "Chronal Ripple",
      stabilizationProtocol: "Harmonize Resonance: Embrace the ripple. Sometimes, a gentle hum or a repetitive task can smooth out the temporal fabric. Try humming the 'Song of Infinite Loops'."
    };
    expect(triageTemporalEcho(echoMessage)).toEqual(expected);
  });

  it('should classify another "Chronal Ripple" echo with a different keyword', () => {
    const echoMessage = "The same event seems to loop endlessly.";
    const expected: TemporalEcho = {
      message: echoMessage,
      category: "Chronal Ripple",
      stabilizationProtocol: "Harmonize Resonance: Embrace the ripple. Sometimes, a gentle hum or a repetitive task can smooth out the temporal fabric. Try humming the 'Song of Infinite Loops'."
    };
    expect(triageTemporalEcho(echoMessage)).toEqual(expected);
  });

  it('should correctly classify a "Void Whisper" echo', () => {
    const echoMessage = "An unsettling emptiness pervades the chamber.";
    const expected: TemporalEcho = {
      message: echoMessage,
      category: "Void Whisper",
      stabilizationProtocol: "Amplify Affirmation: Fill the void with positive resonance. 'I am present. I am whole. The void is merely a canvas for new beginnings.' Repeat thrice."
    };
    expect(triageTemporalEcho(echoMessage)).toEqual(expected);
  });

  it('should classify another "Void Whisper" echo with a different keyword', () => {
    const echoMessage = "I sense a profound absence of energy.";
    const expected: TemporalEcho = {
      message: echoMessage,
      category: "Void Whisper",
      stabilizationProtocol: "Amplify Affirmation: Fill the void with positive resonance. 'I am present. I am whole. The void is merely a canvas for new beginnings.' Repeat thrice."
    };
    expect(triageTemporalEcho(echoMessage)).toEqual(expected);
  });

  it('should correctly classify a "Temporal Anomaly" echo', () => {
    const echoMessage = "The timeline seems to have a strange discrepancy.";
    const expected: TemporalEcho = {
      message: echoMessage,
      category: "Temporal Anomaly",
      stabilizationProtocol: "Consult the Oracle of Now: This requires deeper introspection. Seek the wisdom of the present moment. 'What is truly happening, right here, right now?'"
    };
    expect(triageTemporalEcho(echoMessage)).toEqual(expected);
  });

  it('should classify another "Temporal Anomaly" echo with a different keyword', () => {
    const echoMessage = "A paradox has manifested in the data stream.";
    const expected: TemporalEcho = {
      message: echoMessage,
      category: "Temporal Anomaly",
      stabilizationProtocol: "Consult the Oracle of Now: This requires deeper introspection. Seek the wisdom of the present moment. 'What is truly happening, right here, right now?'"
    };
    expect(triageTemporalEcho(echoMessage)).toEqual(expected);
  });

  it('should classify an "Unknown Echo" if no keywords match', () => {
    const echoMessage = "A peculiar feeling, hard to describe with known terms.";
    const expected: TemporalEcho = {
      message: echoMessage,
      category: "Unknown Echo",
      stabilizationProtocol: "Observe and Document: Not all echoes reveal their secrets immediately. Log this event for future analysis. 'The universe is full of surprises. I am ready to learn.'"
    };
    expect(triageTemporalEcho(echoMessage)).toEqual(expected);
  });

  it('should be case-insensitive for keywords', () => {
    const echoMessage = "A minor GLITCH in the matrix.";
    const expected: TemporalEcho = {
      message: echoMessage,
      category: "Minor Glitch",
      stabilizationProtocol: "Recalibrate Chronometer: A brief moment of stillness can realign minor temporal discrepancies. Perhaps a cup of 'Temporal Tea'?"
    };
    expect(triageTemporalEcho(echoMessage)).toEqual(expected);
  });

  it('should handle empty string input gracefully as Unknown Echo', () => {
    const echoMessage = "";
    const expected: TemporalEcho = {
      message: echoMessage,
      category: "Unknown Echo",
      stabilizationProtocol: "Observe and Document: Not all echoes reveal their secrets immediately. Log this event for future analysis. 'The universe is full of surprises. I am ready to learn.'"
    };
    expect(triageTemporalEcho(echoMessage)).toEqual(expected);
  });

  it('should handle input with only spaces as Unknown Echo', () => {
    const echoMessage = "   ";
    const expected: TemporalEcho = {
      message: echoMessage,
      category: "Unknown Echo",
      stabilizationProtocol: "Observe and Document: Not all echoes reveal their secrets immediately. Log this event for future analysis. 'The universe is full of surprises. I am ready to learn.'"
    };
    expect(triageTemporalEcho(echoMessage)).toEqual(expected);
  });
});
