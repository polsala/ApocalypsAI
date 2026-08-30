import { render, screen, fireEvent } from '@testing-library/react';
import App, { generateConfluenceData } from '../src/App';
import '@testing-library/jest-dom';

describe('generateConfluenceData', () => {
  test('should generate deterministic data for a given keyword', () => {
    const data1 = generateConfluenceData('apocalypse');
    const data2 = generateConfluenceData('apocalypse');
    const data3 = generateConfluenceData('future');

    expect(data1).toEqual(data2); // Same keyword, same data
    expect(data1).not.toEqual(data3); // Different keyword, different data

    expect(data1.nodes.length).toBeGreaterThan(1);
    expect(data1.links.length).toBeGreaterThan(0);
    expect(data1.nodes[0].id).toBe('apocalypse');
  });

  test('should return empty data for an empty keyword', () => {
    const data = generateConfluenceData('');
    expect(data.nodes).toEqual([]);
    expect(data.links).toEqual([]);
  });
});

describe('App', () => {
  test('renders input and button', () => {
    render(<App />);
    expect(screen.getByPlaceholderText(/Enter a concept/i)).toBeInTheDocument();
    expect(screen.getByText(/Generate Confluence/i)).toBeInTheDocument();
  });

  test('generates and displays graph on button click', () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/Enter a concept/i);
    const button = screen.getByText(/Generate Confluence/i);

    fireEvent.change(input, { target: { value: 'echo' } });
    fireEvent.click(button);

    // Mock rationale: The generateConfluenceData function is deterministic and tested separately.
    // Here, we verify that the UI correctly renders elements based on the output of that function.
    // We expect the main node and its echoes to be present as SVG circles and text.
    expect(screen.getByText('echo')).toBeInTheDocument();
    expect(screen.getByText(/echo Echo 1/i)).toBeInTheDocument();
    expect(screen.getAllByTestId('node-circle').length).toBeGreaterThan(1); // Check for multiple nodes
    expect(screen.getAllByTestId('link-line').length).toBeGreaterThan(0); // Check for links
  });

  test('clears graph when input is empty and button is clicked', () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/Enter a concept/i);
    const button = screen.getByText(/Generate Confluence/i);

    fireEvent.change(input, { target: { value: 'test' } });
    fireEvent.click(button);
    expect(screen.getByText('test')).toBeInTheDocument();

    fireEvent.change(input, { target: { value: '' } });
    fireEvent.click(button);

    expect(screen.queryByText('test')).not.toBeInTheDocument();
    expect(screen.queryAllByTestId('node-circle').length).toBe(0);
    expect(screen.queryAllByTestId('link-line').length).toBe(0);
  });

  test('generates graph on Enter key press', () => {
    render(<App />);
    const input = screen.getByPlaceholderText(/Enter a concept/i);

    fireEvent.change(input, { target: { value: 'keyboard' } });
    fireEvent.keyPress(input, { key: 'Enter', code: 13, charCode: 13 });

    expect(screen.getByText('keyboard')).toBeInTheDocument();
    expect(screen.getByText(/keyboard Echo 1/i)).toBeInTheDocument();
  });
});
