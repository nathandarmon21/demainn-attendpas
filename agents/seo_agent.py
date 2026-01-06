"""
SEO Agent - Optimizes episode metadata for maximum discoverability
"""
import os
import json
from utils.claude_client import ClaudeClient
from utils.transcription import Transcriber


class SEOAgent:
    def __init__(self, claude_api_key=None, openai_api_key=None):
        self.claude = ClaudeClient(claude_api_key)
        self.transcriber = Transcriber(openai_api_key)

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
