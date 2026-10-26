import { render, screen } from '@testing-library/react';
import FactionEcho from '../src/FactionEcho';

describe('FactionEcho', () => {
  it('renders faction name, original message, and echo message', () => {
    const factionName = 'Test Faction';
    const originalMessage = 'Hello world';
    const echoMessage = 'Greetings, sentient entity';

    render(
      <FactionEcho
        factionName={factionName}
        originalMessage={originalMessage}
        echoMessage={echoMessage}
      />
    );

    expect(screen.getByText(factionName)).toBeInTheDocument();
    expect(screen.getByText(`Original: ${originalMessage}`)).toBeInTheDocument();
    expect(screen.getByText(`Echo: "${echoMessage}"`)).toBeInTheDocument();
  });

  it('renders correctly with different content', () => {
    const factionName = 'Another Faction';
    const originalMessage = 'Urgent: supplies needed.';
    const echoMessage = 'Immediate resource acquisition imperative.';

    render(
      <FactionEcho
        factionName={factionName}
        originalMessage={originalMessage}
        echoMessage={echoMessage}
      />
    );

    expect(screen.getByText(factionName)).toBeInTheDocument();
    expect(screen.getByText(`Original: ${originalMessage}`)).toBeInTheDocument();
    expect(screen.getByText(`Echo: "${echoMessage}"`)).toBeInTheDocument();
  });
});
