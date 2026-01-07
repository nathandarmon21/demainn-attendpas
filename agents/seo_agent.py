"""
SEO Agent - Optimizes episode metadata for maximum discoverability
"""
import os
import json
from utils.claude_client import ClaudeClient
from utils.transcription import Transcriber
from utils.video_processing import VideoProcessor


class SEOAgent:
    def __init__(self, claude_api_key=None, openai_api_key=None):
        self.claude = ClaudeClient(claude_api_key)
        self.transcriber = Transcriber(openai_api_key)
        self.video_processor = VideoProcessor()

    def suggest_thumbnails(self, video_path, transcript_data, guest_name=None):
        """
        Suggest thumbnail moments from the video
        """
        print("🖼️ Analyzing video for thumbnail suggestions...")

        # Get video duration
        duration = self.video_processor.get_video_duration(video_path)

        # Analyze transcript to find impactful moments
        thumbnail_prompt = f"""Based on this podcast transcript for "Demain N'Attend Pas", suggest 2-3 specific moments that would make compelling YouTube thumbnails.

TRANSCRIPT:
{transcript_data['full_text'][:10000]}

GUEST: {guest_name if guest_name else "Unknown"}
VIDEO DURATION: {duration} seconds

For each thumbnail suggestion, identify:
1. The timestamp (in seconds) of the most visually compelling moment
2. What the person is likely doing/expressing at that moment
3. A suggested text overlay for the thumbnail (short, punchy, French)
4. Why this moment would grab attention

Look for moments of:
- Strong emotion or passion
- Surprise or revelation
- Emphasis on key points
- Expressive gestures (if you can infer from speech patterns)

Return as JSON:
{{
  "thumbnails": [
    {{
      "timestamp": 123.5,
      "description": "Description of the moment",
      "text_overlay": "Texte court et percutant",
      "why_compelling": "Explanation"
    }}
  ]
}}

Return ONLY valid JSON."""

        response = self.claude.analyze(thumbnail_prompt, max_tokens=2048)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            thumbnail_data = json.loads(json_str)
            return thumbnail_data.get('thumbnails', [])
        except json.JSONDecodeError as e:
            print(f"Error parsing thumbnail suggestions: {e}")
            return []

    def generate_linkedin_post(self, transcript_data, seo_package, guest_name=None):
        """
        Generate LinkedIn post based on Delphine Darmon's style
        """
        print("📱 Generating LinkedIn post in Delphine Darmon's style...")

        linkedin_prompt = f"""You are drafting a LinkedIn post for Delphine Darmon about a new episode of "Demain N'Attend Pas".

EPISODE INFORMATION:
Guest: {guest_name if guest_name else "Special guest"}
Titles: {', '.join(seo_package.get('titles', []))}
Key Topics: {', '.join(seo_package.get('keywords_fr', [])[:5])}

TRANSCRIPT EXCERPT:
{transcript_data['full_text'][:5000]}

DELPHINE DARMON'S LINKEDIN STYLE:
- Professional but warm and authentic
- French language
- Personal reflection mixed with the guest's insights
- Often starts with a question or provocative statement
- 3-5 short paragraphs
- Highlights what she learned or found fascinating
- Includes call to action to listen
- Uses 3-5 relevant hashtags at the end
- Conversational yet intellectual tone

TASK:
Write a LinkedIn post (300-500 words) announcing this episode in Delphine's style.

Structure:
1. Hook - provocative question or personal reflection
2. Brief introduction of guest and topic
3. Key insight or moment from conversation
4. Personal takeaway or why this matters
5. Call to action
6. Hashtags (3-5)

Return as JSON:
{{
  "linkedin_post": "Full post text here...",
  "alternative_hook": "Alternative first line if she wants variety",
  "suggested_hashtags": ["#hashtag1", "#hashtag2", ...]
}}

Return ONLY valid JSON."""

        response = self.claude.analyze(linkedin_prompt, max_tokens=2048)

        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            linkedin_data = json.loads(json_str)
            return linkedin_data
        except json.JSONDecodeError as e:
            print(f"Error parsing LinkedIn post: {e}")
            return None

    def analyze_episode(self, video_path, guest_name=None, episode_topic=None):
        """
        Analyze episode content and generate comprehensive SEO strategy
        """
        print("🎬 Transcribing episode for SEO analysis...")
        transcript_data = self.transcriber.transcribe_with_timestamps(video_path)

        print("🔍 Analyzing with Claude to generate SEO strategy...")

        # Build context
        context = f"""Episode Transcript:
{transcript_data['full_text'][:15000]}  # Use first 15k chars to stay within limits
"""

        if guest_name:
            context = f"Guest: {guest_name}\n" + context
        if episode_topic:
            context = f"Topic: {episode_topic}\n" + context

        seo_prompt = f"""You are an SEO expert for "Demain N'attend Pas", a French intellectual podcast. Analyze this episode and create a comprehensive SEO strategy.

{context}

TASK:
Generate a complete SEO package including:

1. EPISODE TITLES (2-3 options):
   - Attention-grabbing titles that would make people click
   - Optimized for French and international audiences
   - Include key themes/guest name
   - 60-80 characters max

2. KEYWORDS & TAGS:
   - 15-20 highly relevant keywords in French
   - 10-15 keywords in English
   - Mix of broad and specific terms
   - Consider what people would search for

3. HASHTAGS:
   - 10-15 hashtags for Instagram/social media
   - Mix of French and English
   - Include trending and niche tags

4. PLATFORM-SPECIFIC DESCRIPTIONS:
   Generate optimized descriptions for each platform:

   a) SPOTIFY (max 400 chars, French):
      - Hook in first line
      - Key topics covered
      - Include keywords naturally

   b) APPLE PODCASTS (similar to Spotify, French)

   c) YOUTUBE (detailed, French):
      - Longer description (500-800 chars)
      - Timestamps of key moments
      - Call to action
      - Keywords integrated naturally

   d) INSTAGRAM (short, punchy, French):
      - 150-200 chars
      - Hook + call to action
      - Hashtags separate

5. SEARCH ENGINE OPTIMIZATION:
   - Blog post title suggestion (if creating episode page)
   - Meta description (160 chars)
   - Additional SEO recommendations

Return your response as a JSON object with this structure:
{{
  "titles": ["Option 1", "Option 2", "Option 3"],
  "keywords_fr": ["mot-clé 1", "mot-clé 2", ...],
  "keywords_en": ["keyword 1", "keyword 2", ...],
  "hashtags": ["#tag1", "#tag2", ...],
  "descriptions": {{
    "spotify": "description text...",
    "apple_podcasts": "description text...",
    "youtube": "description text...",
    "instagram": "description text..."
  }},
  "seo_extras": {{
    "blog_title": "title",
    "meta_description": "description",
    "recommendations": ["recommendation 1", "recommendation 2", ...]
  }}
}}

Return ONLY valid JSON, no additional text."""

        response = self.claude.analyze(seo_prompt, max_tokens=4096)

        # Parse response
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            seo_package = json.loads(json_str)

            # Add thumbnail suggestions
            thumbnails = self.suggest_thumbnails(video_path, transcript_data, guest_name)
            seo_package['thumbnails'] = thumbnails

            # Add LinkedIn post
            linkedin_data = self.generate_linkedin_post(transcript_data, seo_package, guest_name)
            if linkedin_data:
                seo_package['linkedin'] = linkedin_data

            return seo_package
        except json.JSONDecodeError as e:
            print(f"Error parsing Claude's response: {e}")
            return None

    def format_seo_package(self, seo_package):
        """
        Format SEO package into readable output
        """
        if not seo_package:
            return "Error: Could not generate SEO package"

        output = """
╔════════════════════════════════════════════════════════════════╗
║                   SEO OPTIMIZATION PACKAGE                      ║
║                    Demain N'Attend Pas                         ║
╚════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 EPISODE TITLE OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, title in enumerate(seo_package['titles'], 1):
            output += f"{i}. {title}\n"

        output += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 KEYWORDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🇫🇷 Français:
{', '.join(seo_package['keywords_fr'])}

🇬🇧 English:
{', '.join(seo_package['keywords_en'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HASHTAGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{' '.join(seo_package['hashtags'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 PLATFORM-SPECIFIC DESCRIPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎵 SPOTIFY:
{seo_package['descriptions']['spotify']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎧 APPLE PODCASTS:
{seo_package['descriptions']['apple_podcasts']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📺 YOUTUBE:
{seo_package['descriptions']['youtube']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📸 INSTAGRAM:
{seo_package['descriptions']['instagram']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🖼️ THUMBNAIL SUGGESTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, thumb in enumerate(seo_package.get('thumbnails', []), 1):
            mins = int(thumb['timestamp'] // 60)
            secs = int(thumb['timestamp'] % 60)
            output += f"{i}. Timestamp: {mins}:{secs:02d}\n"
            output += f"   Description: {thumb['description']}\n"
            output += f"   Text Overlay: \"{thumb['text_overlay']}\"\n"
            output += f"   Why: {thumb['why_compelling']}\n\n"

        output += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 LINKEDIN POST (Delphine Darmon Style)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{seo_package.get('linkedin', {}).get('linkedin_post', 'N/A')}

Alternative Hook:
{seo_package.get('linkedin', {}).get('alternative_hook', 'N/A')}

Hashtags: {' '.join(seo_package.get('linkedin', {}).get('suggested_hashtags', []))}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 SEO EXTRAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Blog Post Title:
{seo_package['seo_extras']['blog_title']}

Meta Description:
{seo_package['seo_extras']['meta_description']}

Additional Recommendations:
"""
        for rec in seo_package['seo_extras']['recommendations']:
            output += f"• {rec}\n"

        output += "\n" + "="*70 + "\n"

        return output

    def run_full_analysis(self, video_path, guest_name=None, episode_topic=None):
        """
        Complete SEO analysis pipeline
        """
        print("🚀 Starting SEO Agent Analysis...\n")

        seo_package = self.analyze_episode(video_path, guest_name, episode_topic)

        if not seo_package:
            return "❌ SEO analysis failed. Please try again."

        formatted_output = self.format_seo_package(seo_package)

        print("✅ SEO package generated successfully!\n")

        return formatted_output, seo_package
