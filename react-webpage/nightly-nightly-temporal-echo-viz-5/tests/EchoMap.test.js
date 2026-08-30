import { render, screen, fireEvent } from '@testing-library/react';
import EchoMap from '../src/components/EchoMap';
import { mockEchoData } from '../src/data/mockEchoData';

// Mock rationale: We mock react-leaflet components to prevent actual map rendering,
// network requests for tiles, and to ensure deterministic, offline testing.
// This allows us to test the component's logic for rendering markers/circles
// and handling events without a full browser environment.
jest.mock('react-leaflet', () => ({
  MapContainer: ({ children, ...props }) => <div data-testid="mock-map-container" {...props}>{children}</div>,
  TileLayer: (props) => <div data-testid="mock-tile-layer" {...props}></div>,
  Marker: ({ children, eventHandlers, ...props }) => (
    <div data-testid="mock-marker" onClick={eventHandlers?.click} {...props}>{children}</div>
  ),
  Popup: ({ children }) => <div data-testid="mock-popup">{children}</div>,
  Circle: (props) => <div data-testid="mock-circle" onClick={props.eventHandlers?.click} {...props}></div>,
}));

describe('EchoMap', () => {
  const onEchoSelectMock = jest.fn();

  beforeEach(() => {
    onEchoSelectMock.mockClear();
  });

  test('renders MapContainer and TileLayer', () => {
    render(<EchoMap echoes={[]} onEchoSelect={onEchoSelectMock} />);
    expect(screen.getByTestId('mock-map-container')).toBeInTheDocument();
    expect(screen.getByTestId('mock-tile-layer')).toBeInTheDocument();
  });

  test('renders correct number of markers and circles for echoes', () => {
    render(<EchoMap echoes={mockEchoData} onEchoSelect={onEchoSelectMock} />);
    const markers = screen.getAllByTestId('mock-marker');
    const circles = screen.getAllByTestId('mock-circle');
    expect(markers).toHaveLength(mockEchoData.length);
    expect(circles).toHaveLength(mockEchoData.length);
  });

  test('clicking a marker triggers onEchoSelect with correct echo data', () => {
    render(<EchoMap echoes={mockEchoData} onEchoSelect={onEchoSelectMock} />);
    const firstMarker = screen.getAllByTestId('mock-marker')[0];
    fireEvent.click(firstMarker);
    expect(onEchoSelectMock).toHaveBeenCalledTimes(1);
    expect(onEchoSelectMock).toHaveBeenCalledWith(mockEchoData[0]);
  });

  test('clicking a circle triggers onEchoSelect with correct echo data', () => {
    render(<EchoMap echoes={mockEchoData} onEchoSelect={onEchoSelectMock} />);
    const firstCircle = screen.getAllByTestId('mock-circle')[0];
    fireEvent.click(firstCircle);
    expect(onEchoSelectMock).toHaveBeenCalledTimes(1);
    expect(onEchoSelectMock).toHaveBeenCalledWith(mockEchoData[0]);
  });

  test('markers and circles have correct position props (smoke test)', () => {
    render(<EchoMap echoes={[mockEchoData[0]]} onEchoSelect={onEchoSelectMock} />);
    const marker = screen.getByTestId('mock-marker');
    const circle = screen.getByTestId('mock-circle');

    // Check if position/center props are passed, even if mocked component doesn't use them visually.
    // This verifies data flow.
    expect(marker).toHaveProperty('position', [mockEchoData[0].location.lat, mockEchoData[0].location.lng]);
    expect(circle).toHaveProperty('center', [mockEchoData[0].location.lat, mockEchoData[0].location.lng]);
  });
});
