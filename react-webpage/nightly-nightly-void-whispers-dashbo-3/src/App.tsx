import React, { useState } from 'react';
import styled, { keyframes } from 'styled-components';
import AffirmationList from './components/AffirmationList';
import WhisperForm from './components/WhisperForm';
import { Affirmation } from './types';

const AppContainer = styled.div`
  text-align: center;
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #1e1e2f, #2d1b69);
  color: white;
  min-height: 100vh;
`;

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

const Title = styled.h1`
  animation: ${pulse} 2s infinite;
`;

const App: React.FC = () => {
  const [affirmations, setAffirmations] = useState<Affirmation[]>([
    { id: '1', text: 'The void whispers: You are enough.', favorited: false },
    { id: '2', text: 'Chaos breeds creativity.', favorited: true },
    { id: '3', text: 'Embrace the unknown—it knows you better than you know yourself.', favorited: false },
  ]);

  const handleAddAffirmation = (text: string) => {
    const newAffirmation: Affirmation = {
      id: Date.now().toString(),
      text,
      favorited: false,
    };
    setAffirmations([newAffirmation, ...affirmations]);
  };

  const toggleFavorite = (id: string) => {
    setAffirmations(
      affirmations.map((a) =>
        a.id === id ? { ...a, favorited: !a.favorited } : a
      )
    );
  };

  return (
    <AppContainer>
      <Title>🌌 Void Whispers Dashboard</Title>
      <WhisperForm onSubmit={handleAddAffirmation} />
      <AffirmationList
        affirmations={affirmations}
        onToggleFavorite={toggleFavorite}
      />
    </AppContainer>
  );
};

export default App;
