"""
Short Video Agent - Identifies and creates viral clips from full episodes
"""
import os
import json
from utils.claude_client import ClaudeClient
from utils.transcription import Transcriber
from utils.video_processing import VideoProcessor


class ShortVideoAgent:
    def __init__(self, claude_api_key=None, openai_api_key=None):
        self.claude = ClaudeClient(claude_api_key)
        self.transcriber = Transcriber(openai_api_key)
        self.video_processor = VideoProcessor()

    def analyze_and_identify_clips(self, video_path, num_clips=6):
        """
        Step 1: Transcribe video and identify best moments for short clips
        Returns: List of clip suggestions with timestamps
        """
        print("🎬 Transcribing video... This may take a few minutes.")
        transcript_data = self.transcriber.transcribe_with_timestamps(video_path)

        print("🤔 Analyzing transcript with Claude to identify viral moments...")

        # Create a detailed context for Claude
        segments_text = "\n".join([
            f"[{self._format_timestamp(seg['start'])} - {self._format_timestamp(seg['end'])}] {seg['text']}"
            for seg in transcript_data['segments']
        ])

        analysis_prompt = f"""You are analyzing a French podcast episode for "Demain N'attend Pas" to identify the best moments for viral short-form content (YouTube Shorts, Instagram Reels).

TRANSCRIPT WITH TIMESTAMPS:
{segments_text}

TASK:
Identify the {num_clips} best 10-15 second clips that would work well as social media shorts. For each clip, you must:

1. Select moments that are:
   - Self-contained and make sense without additional context
   - Attention-grabbing in the first 2 seconds
   - A mix of: provocative statements, profound insights, emotionally resonant moments, surprising facts, or controversial takes
   - Engaging for the French intellectual/cultural audience

2. Each clip should be 10-15 seconds (no longer, no shorter)

3. For EACH clip provide:
   - Start timestamp (in seconds)
   - End timestamp (in seconds)
   - Exact quote/transcript excerpt
   - Clip type (provocative/insightful/emotional/surprising)
   - Suggested title (compelling, in French, max 100 characters)
   - Caption text to overlay on video (French, max 50 characters, punchy)
   - 3-5 hashtags in French and English
   - Brief explanation (1 sentence) of why this will perform well

Return ONLY a valid JSON array with this exact structure:
[
  {{
    "start_time": 123.5,
    "end_time": 138.2,
    "quote": "exact transcript excerpt",
    "type": "provocative",
    "title": "Titre accrocheur",
    "caption": "Texte court et percutant",
    "hashtags": ["#DemainNAttendPas", "#Philosophy", "#DeepThoughts"],
    "reasoning": "Why this clip will perform well"
  }}
]

IMPORTANT: Return ONLY the JSON array, nothing else. Ensure all {num_clips} clips are different and compelling."""

        response = self.claude.analyze(
            analysis_prompt,
            max_tokens=4096
        )

        # Parse Claude's response
        try:
            # Extract JSON from response (in case Claude adds explanation)
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            json_str = response[json_start:json_end]
            clips = json.loads(json_str)
            return clips
        except json.JSONDecodeError as e:
            print(f"Error parsing Claude's response: {e}")
            print(f"Response was: {response}")
            return []

    def generate_clips(self, video_path, clip_suggestions, output_dir="outputs/short_videos"):
        """
        Step 2: Generate actual video clips from suggestions
        """
        os.makedirs(output_dir, exist_ok=True)
        generated_clips = []

        for i, clip in enumerate(clip_suggestions):
            print(f"\n🎥 Generating clip {i+1}/{len(clip_suggestions)}: {clip.get('title', 'Untitled')}")

            output_filename = f"clip_{i+1}_{clip.get('type', 'clip')}.mp4"
            output_path = os.path.join(output_dir, output_filename)

            success = self.video_processor.create_clip_with_captions(
                video_path=video_path,
                start_time=clip.get('start_time', 0),
                end_time=clip.get('end_time', 10),
                caption_text=clip.get('caption', ''),
                output_path=output_path
            )

            if success:
                generated_clips.append({
                    'file_path': output_path,
                    'clip_info': clip
                })
                print(f"✅ Saved to: {output_path}")
            else:
                print(f"❌ Failed to generate clip {i+1}")

        return generated_clips

    def create_posting_instructions(self, generated_clips):
        """
        Step 3: Create ready-to-post package with all metadata
        """
        instructions = []

        for i, clip_data in enumerate(generated_clips):
            clip = clip_data.get('clip_info', {})

            post_instruction = f"""
═══════════════════════════════════════════
CLIP {i+1}: {clip.get('title', 'Untitled')}
═══════════════════════════════════════════

📁 FILE: {clip_data.get('file_path', 'N/A')}
🎯 TYPE: {clip.get('type', 'N/A')}

💬 QUOTE:
"{clip.get('quote', 'N/A')}"

📱 YOUTUBE SHORTS TITLE:
{clip.get('title', 'Untitled')}

📝 YOUTUBE DESCRIPTION:
{clip.get('title', 'Untitled')}

{' '.join(clip.get('hashtags', []))}

Écoutez l'épisode complet sur toutes les plateformes de podcast 🎧
#DemainNAttendPas #Podcast #PodcastFrançais

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 INSTAGRAM REEL CAPTION:
{clip.get('caption', 'N/A')}

{' '.join(clip.get('hashtags', []))}

Épisode complet disponible sur toutes les plateformes 🎧
#DemainNAttendPas #PodcastFrançais #Reels

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 WHY THIS WORKS:
{clip.get('reasoning', 'N/A')}

"""
            instructions.append(post_instruction)

        return "\n".join(instructions)

    def run_full_pipeline(self, video_path, num_clips=6):
        """
        Complete pipeline: Analyze -> Generate -> Package for posting
        Returns: (generated_clips, posting_instructions)
        """
        print("🚀 Starting Short Video Agent Pipeline...\n")

        # Step 1: Analyze and identify clips
        clip_suggestions = self.analyze_and_identify_clips(video_path, num_clips)

        if not clip_suggestions:
            print("❌ No clips identified. Check the transcript analysis.")
            return [], ""

        print(f"\n✅ Identified {len(clip_suggestions)} potential clips")

        # Step 2: Generate video clips
        generated_clips = self.generate_clips(video_path, clip_suggestions)

        print(f"\n✅ Successfully generated {len(generated_clips)} video clips")

        # Step 3: Create posting instructions
        posting_instructions = self.create_posting_instructions(generated_clips)

        return generated_clips, posting_instructions

    def _format_timestamp(self, seconds):
        """Convert seconds to MM:SS format"""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"
