import { render, screen } from '@testing-library/react';
import ChronoCompass from '../src/ChronoCompass';

describe('ChronoCompass', () => {
  test('renders the compass face and needle', () => {
    render(
      <ChronoCompass
        temporalStability={75}
        resourceAbundance={60}
        communityMorale={85}
        weatherAnomaly={20}
      />
    );
    expect(screen.getByText(/STABLE/i)).toBeInTheDocument();
    expect(screen.getByText(/CHAOS/i)).toBeInTheDocument();
    expect(screen.getByText(/ABUNDANCE/i)).toBeInTheDocument();
    expect(screen.getByText(/SCARCITY/i)).toBeInTheDocument();
    // The needle is a div with a specific class and style, not directly accessible by text or role without specific ARIA attributes.
    // We can target it by its class and check its style attribute.
    const needle = screen.getByRole('presentation', { name: '' }); // Using presentation role as it's purely decorative
    expect(needle).toHaveClass('compass-needle');
  });

  test('needle rotation reflects high stability (good score)', () => {
    // # Mock rationale: Direct prop passing for deterministic testing of visual output.
    // High scores should result in a positive rotation (pointing towards STABLE/ABUNDANCE).
    render(
      <ChronoCompass
        temporalStability={90}
        resourceAbundance={90}
        communityMorale={90}
        weatherAnomaly={10} // Normalized to 90
      />
    );
    const needle = screen.getByRole('presentation', { name: '' });
    // Average score: (90+90+90+90)/4 = 90. Rotation: (90-50)*1.8 = 40*1.8 = 72deg
    expect(needle).toHaveStyle('transform: translate(-50%, -100%) rotate(72deg)');
  });

  test('needle rotation reflects low stability (bad score)', () => {
    // # Mock rationale: Direct prop passing for deterministic testing of visual output.
    // Low scores should result in a negative rotation (pointing towards CHAOS/SCARCITY).
    render(
      <ChronoCompass
        temporalStability={10}
        resourceAbundance={10}
        communityMorale={10}
        weatherAnomaly={90} // Normalized to 10
      />
    );
    const needle = screen.getByRole('presentation', { name: '' });
    // Average score: (10+10+10+10)/4 = 10. Rotation: (10-50)*1.8 = -40*1.8 = -72deg
    expect(needle).toHaveStyle('transform: translate(-50%, -100%) rotate(-72deg)');
  });

  test('needle rotation reflects neutral stability (mid score)', () => {
    // # Mock rationale: Direct prop passing for deterministic testing of visual output.
    // Mid scores should result in a rotation close to 0deg (pointing upwards).
    render(
      <ChronoCompass
        temporalStability={50}
        resourceAbundance={50}
        communityMorale={50}
        weatherAnomaly={50} // Normalized to 50
      />
    );
    const needle = screen.getByRole('presentation', { name: '' });
    // Average score: (50+50+50+50)/4 = 50. Rotation: (50-50)*1.8 = 0deg
    expect(needle).toHaveStyle('transform: translate(-50%, -100%) rotate(0deg)');
  });
});
