import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { fetchAuthSession } from 'aws-amplify/auth';

async function getTextToSpeechFile(text) {
  try {
    const token = (await fetchAuthSession()).tokens.idToken;
    const response = await fetch('https://0y2e52zyqa.execute-api.us-east-1.amazonaws.com/prod/tts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        "text": text
      })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    return data["audio-base64"];
  } catch (error) {
    console.error('Error fetching text-to-speech:', error);
    throw error;
  }
}

export default function TextToSpeechBtn({ text }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [error, setError] = useState(null);
  const audioRef = useRef(null);

  async function handlePlay() {
    try {
      setError(null);
      setIsPlaying(true);

      const base64Audio = await getTextToSpeechFile(text);

      const binaryString = atob(base64Audio);
      const bytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      const blob = new Blob([bytes], { type: 'audio/mpeg' });

      const audioUrl = URL.createObjectURL(blob);
      
      if (!audioRef.current) {
        audioRef.current = new Audio();
      }

      audioRef.current.src = audioUrl;
      audioRef.current.play();

      audioRef.current.onended = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };

    } catch (err) {
      setError('Failed to play audio');
      setIsPlaying(false);
      console.error('Error playing audio:', err);
    }
  }

  function handleStop() {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    setIsPlaying(false);
  }

  return (
    <div>
      <Button
        onClick={isPlaying ? handleStop : handlePlay}
        disabled={!text}
        className="text-white font-semibold py-2 px-6 rounded-lg
                    transform transition duration-300 ease-in-out
                    hover:bg-amber-500 hover:scale-105 hover:shadow-lg
                    active:scale-95 active:bg-amber-700 cusror-pointer"
      >
        {isPlaying ? 'Stop' : 'Listen'}
      </Button>
      {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
    </div>
  );
}