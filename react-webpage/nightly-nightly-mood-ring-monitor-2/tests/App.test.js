import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../src/App';
import moodData from '../src/moodData'; // Import actual mood data for assertions

describe('App', () => {
  test('renders the main title', () => {
    render(<App />);
    expect(screen.getByText(/Nightly Mood Ring Monitor/i)).toBeInTheDocument();
  });

  test('initial mood is neutral and ring color matches', () => {
    render(<App />);
    const moodRing = screen.getByLabelText('Mood Ring');
    expect(moodRing).toHaveStyle(`background-color: ${moodData.neutral.color}`);
    expect(screen.getByText(`Current Mood: Neutral`)).toBeInTheDocument();
    expect(screen.getByText(moodData.neutral.affirmation)).toBeInTheDocument();
  });

  test('typing "happy" changes mood to happy and updates ring color and affirmation', () => {
    render(<App />);
    const moodInput = screen.getByLabelText('Mood input');
    fireEvent.change(moodInput, { target: { value: 'I feel happy today!' } });

    const moodRing = screen.getByLabelText('Mood Ring');
    expect(moodRing).toHaveStyle(`background-color: ${moodData.happy.color}`);
    expect(screen.getByText(`Current Mood: Happy`)).toBeInTheDocument();
    expect(screen.getByText(moodData.happy.affirmation)).toBeInTheDocument();
  });

  test('typing "anxious" changes mood to anxious and updates ring color and affirmation', () => {
    render(<App />);
    const moodInput = screen.getByLabelText('Mood input');
    fireEvent.change(moodInput, { target: { value: 'Feeling a bit anxious about the future.' } });

    const moodRing = screen.getByLabelText('Mood Ring');
    expect(moodRing).toHaveStyle(`background-color: ${moodData.anxious.color}`);
    expect(screen.getByText(`Current Mood: Anxious`)).toBeInTheDocument();
    expect(screen.getByText(moodData.anxious.affirmation)).toBeInTheDocument();
  });

  test('typing "calm" changes mood to calm and updates ring color and affirmation', () => {
    render(<App />);
    const moodInput = screen.getByLabelText('Mood input');
    fireEvent.change(moodInput, { target: { value: 'All is calm.' } });

    const moodRing = screen.getByLabelText('Mood Ring');
    expect(moodRing).toHaveStyle(`background-color: ${moodData.calm.color}`);
    expect(screen.getByText(`Current Mood: Calm`)).toBeInTheDocument();
    expect(screen.getByText(moodData.calm.affirmation)).toBeInTheDocument();
  });

  test('typing unknown keywords defaults to neutral', () => {
    render(<App />);
    const moodInput = screen.getByLabelText('Mood input');
    fireEvent.change(moodInput, { target: { value: 'I am just existing.' } });

    const moodRing = screen.getByLabelText('Mood Ring');
    expect(moodRing).toHaveStyle(`background-color: ${moodData.neutral.color}`);
    expect(screen.getByText(`Current Mood: Neutral`)).toBeInTheDocument();
    expect(screen.getByText(moodData.neutral.affirmation)).toBeInTheDocument();
  });
});
