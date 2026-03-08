import React, { useState } from 'react';
import styled from 'styled-components';

interface Props {
  onSubmit: (text: string) => void;
}

const FormContainer = styled.form`
  margin: 2rem auto;
  max-width: 500px;
  display: flex;
  gap: 0.5rem;
`;

const Input = styled.input`
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
`;

const Button = styled.button`
  padding: 0.75rem 1.5rem;
  background-color: #6c5ce7;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  &:hover {
    background-color: #5d4de0;
  }
`;

const WhisperForm: React.FC<Props> = ({ onSubmit }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input);
      setInput('');
    }
  };

  return (
    <FormContainer onSubmit={handleSubmit}>
      <Input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Whisper something to the void..."
      />
      <Button type="submit">Send</Button>
    </FormContainer>
  );
};

export default WhisperForm;
