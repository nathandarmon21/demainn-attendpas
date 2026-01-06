"""
Video/Audio transcription using OpenAI Whisper
"""
import os
from openai import OpenAI
import tempfile


class Transcriber:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file")
        self.client = OpenAI(api_key=self.api_key)

    def transcribe_audio(self, audio_path, language="fr"):
        """
        Transcribe audio/video file using Whisper
        Returns transcript with timestamps
        """
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"]
                )
            return transcript
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")

    def transcribe_with_timestamps(self, audio_path, language="fr"):
        """
        Returns a formatted transcript with timestamps for each segment
        """
        transcript = self.transcribe_audio(audio_path, language)

        formatted_segments = []
        for segment in transcript.segments:
            formatted_segments.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'],
                'duration': segment['end'] - segment['start']
            })

        return {
            'full_text': transcript.text,
            'segments': formatted_segments
        }
