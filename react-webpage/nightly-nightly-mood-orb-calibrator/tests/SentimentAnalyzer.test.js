import { analyzeSentiment } from '../src/SentimentAnalyzer';

describe('analyzeSentiment', () => {
  test('identifies positive sentiment', () => {
    expect(analyzeSentiment('I feel great and full of hope for the future.')).toEqual({ score: 2, label: 'positive' });
    expect(analyzeSentiment('This is a good day for progress.')).toEqual({ score: 2, label: 'positive' });
    expect(analyzeSentiment('Love and joy abound!')).toEqual({ score: 2, label: 'positive' });
    expect(analyzeSentiment('We are safe and secure.')).toEqual({ score: 2, label: 'positive' });
  });

  test('identifies negative sentiment', () => {
    expect(analyzeSentiment('There is danger and fear in the air.')).toEqual({ score: 2, label: 'negative' });
    expect(analyzeSentiment('This is a bad situation, full of despair.')).toEqual({ score: 2, label: 'negative' });
    expect(analyzeSentiment('Lost and broken, a struggle.')).toEqual({ score: 3, label: 'negative' });
    expect(analyzeSentiment('The pain of failure is awful.')).toEqual({ score: 3, label: 'negative' });
  });

  test('identifies neutral sentiment', () => {
    expect(analyzeSentiment('The quick brown fox jumps over the lazy dog.')).toEqual({ score: 0, label: 'neutral' });
    expect(analyzeSentiment('The machine is running.')).toEqual({ score: 0, label: 'neutral' });
    expect(analyzeSentiment('It is cloudy today.')).toEqual({ score: 0, label: 'neutral' });
    expect(analyzeSentiment('A mix of good and bad words, but balanced.')).toEqual({ score: 0, label: 'neutral' }); // 'good' and 'bad' cancel out
  });

  test('handles mixed sentiment, prioritizing stronger count', () => {
    expect(analyzeSentiment('It was a good day, but there was some pain.')).toEqual({ score: 0, label: 'neutral' }); // good (1) vs pain (1)
    expect(analyzeSentiment('Despite the struggle, there is hope for success.')).toEqual({ score: 1, label: 'positive' }); // hope, success (2) vs struggle (1)
    expect(analyzeSentiment('A great victory, but the danger is still present.')).toEqual({ score: 1, label: 'positive' }); // great, victory (2) vs danger (1)
  });

  test('handles empty string', () => {
    expect(analyzeSentiment('')).toEqual({ score: 0, label: 'neutral' });
  });

  test('is case-insensitive', () => {
    expect(analyzeSentiment('HoPe Is HeRe')).toEqual({ score: 1, label: 'positive' });
    expect(analyzeSentiment('FeAr NoT')).toEqual({ score: 1, label: 'negative' }); // 'fear' is negative, 'not' is not a keyword
  });
});
