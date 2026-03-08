import React from 'react';
import styled from 'styled-components';
import { Affirmation } from '../types';

interface Props {
  affirmations: Affirmation[];
  onToggleFavorite: (id: string) => void;
}

const ListContainer = styled.div`
  margin-top: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
`;

const AffirmationCard = styled.div<{ favorited: boolean }> `
  background: ${(props) => (props.favorited ? '#4b3fa1' : '#333')};
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
  &:hover {
    transform: translateY(-5px);
  }
`;

const FavoriteButton = styled.button`
  background: none;
  border: none;
  color: gold;
  cursor: pointer;
  font-size: 1.2rem;
`;

const AffirmationList: React.FC<Props> = ({ affirmations, onToggleFavorite }) => {
  return (
    <ListContainer>
      {affirmations.map((affirmation) => (
        <AffirmationCard key={affirmation.id} favorited={affirmation.favorited}>
          <p>{affirmation.text}</p>
          <FavoriteButton onClick={() => onToggleFavorite(affirmation.id)}>
            {affirmation.favorited ? '★' : '☆'}
          </FavoriteButton>
        </AffirmationCard>
      ))}
    </ListContainer>
  );
};

export default AffirmationList;
