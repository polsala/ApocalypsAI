export interface Whisper {
  id: string;
  content: string;
  tags: string[];
  timestamp: string;
}

export interface WhisperArchive {
  whispers: Whisper[];
}
