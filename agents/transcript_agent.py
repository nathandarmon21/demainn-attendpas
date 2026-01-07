"""
Transcript Agent - Creates clean, publishable transcripts
"""
import os
from utils.claude_client import ClaudeClient
from utils.transcription import Transcriber


class TranscriptAgent:
    def __init__(self, claude_api_key=None, openai_api_key=None):
        self.claude = ClaudeClient(claude_api_key)
        self.transcriber = Transcriber(openai_api_key)

    def generate_clean_transcript(self, video_path):
        """
        Generate a cleaned transcript ready for newsletter publication
        """
        print("🎬 Transcribing video...")
        transcript_data = self.transcriber.transcribe_with_timestamps(video_path)

        print("✨ Cleaning transcript with Claude...")

        # Get raw transcript
        raw_transcript = transcript_data['full_text']

        cleaning_prompt = f"""You are cleaning a French podcast transcript for "Demain N'Attend Pas" to make it publication-ready for a newsletter.

RAW TRANSCRIPT:
{raw_transcript}

TASK:
Clean this transcript by:

1. **Remove speech disfluencies:**
   - Remove "euh", "uhm", "uh", "hum", etc.
   - Remove repeated words (e.g., "je je je pense" → "je pense")
   - Remove false starts and incomplete sentences
   - Remove filler phrases that add no meaning

2. **Maintain authenticity:**
   - Keep the original language (French)
   - Preserve the speaker's voice and personality
   - Keep meaningful pauses indicated as [pause] if they're significant
   - Maintain the natural flow of conversation

3. **Improve readability:**
   - Add proper punctuation
   - Break into logical paragraphs
   - Add speaker labels if there are multiple speakers (use "Hôte:" and "Invité:" or actual names if clear)
   - Keep the conversational tone

4. **Format for newsletter:**
   - Make it easy to read
   - Professional but authentic
   - Ready to copy-paste into a newsletter

IMPORTANT:
- Do NOT summarize or shorten the content
- Do NOT translate - keep it in the original language
- Do NOT add content that wasn't said
- Just clean and format what's already there

Return the cleaned transcript directly. No introduction, no explanation - just the cleaned transcript."""

        cleaned_transcript = self.claude.analyze(
            cleaning_prompt,
            max_tokens=16000,  # Allow for longer transcripts
            model="claude-sonnet-4-20250514"
        )

        return cleaned_transcript, raw_transcript

    def format_for_export(self, cleaned_transcript, episode_info=None):
        """
        Format the cleaned transcript for export
        """
        output = ""

        if episode_info:
            output += f"""╔════════════════════════════════════════════════════════════════╗
║                   TRANSCRIPT - DEMAIN N'ATTEND PAS              ║
╚════════════════════════════════════════════════════════════════╝

"""
            if episode_info.get('title'):
                output += f"ÉPISODE: {episode_info['title']}\n"
            if episode_info.get('guest'):
                output += f"INVITÉ(E): {episode_info['guest']}\n"
            if episode_info.get('date'):
                output += f"DATE: {episode_info['date']}\n"

            output += "\n" + "="*70 + "\n\n"

        output += cleaned_transcript

        output += "\n\n" + "="*70 + "\n"
        output += "Transcript nettoyé et formaté pour publication\n"
        output += "Demain N'Attend Pas - https://demain-nattend-pas.fr\n"

        return output

    def run_full_pipeline(self, video_path, episode_info=None):
        """
        Complete pipeline: Transcribe -> Clean -> Format
        """
        print("🚀 Starting Transcript Agent Pipeline...\n")

        # Generate cleaned transcript
        cleaned_transcript, raw_transcript = self.generate_clean_transcript(video_path)

        print("✅ Transcript cleaned successfully!\n")

        # Format for export
        formatted_output = self.format_for_export(cleaned_transcript, episode_info)

        return formatted_output, cleaned_transcript, raw_transcript
