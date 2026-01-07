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

CONTEXT ABOUT "DEMAIN N'ATTEND PAS" THUMBNAIL STYLE:
This podcast focuses on climate change, biodiversity loss, and social inequalities with engaged entrepreneurs, activist artists, impact investors, and NGO founders. The thumbnails should reflect:
- Authentic, intimate conversation aesthetic
- Professional yet approachable visual style
- Focus on the guest and their impact/message
- Clean, readable text overlays in French
- Emphasis on thought-provoking ideas and inspiration
- Colors and style that align with the podcast's pastel beige branding (#FAF7F2)

TRANSCRIPT:
{transcript_data['full_text'][:10000]}

GUEST: {guest_name if guest_name else "Unknown"}
VIDEO DURATION: {duration} seconds

For each thumbnail suggestion, identify:
1. The timestamp (in seconds) of the most visually compelling moment
2. What the person is likely doing/expressing at that moment (authentic, engaged in conversation)
3. A suggested text overlay for the thumbnail (short, punchy, French, max 6-8 words)
4. Design notes (colors, layout suggestions that match existing style)
5. Why this moment would grab attention while staying true to the authentic, impact-focused brand

Look for moments of:
- Strong emotion or passion about impact/change
- Surprise or revelation about social/environmental issues
- Emphasis on solutions and positive action
- Authentic, intimate conversation moments
- Expressive engagement with important ideas

Return as JSON:
{{
  "thumbnails": [
    {{
      "timestamp": 123.5,
      "description": "Description of the moment",
      "text_overlay": "Texte court et percutant",
      "design_notes": "Color palette suggestions, layout ideas, visual style notes",
      "why_compelling": "Explanation of why this grabs attention while matching brand"
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

DELPHINE DARMON'S EXACT LINKEDIN STYLE (IMPORTANT - MATCH THIS CLOSELY):
- Always in French
- HEAVY use of emojis throughout: 🔥, 🎤, 🎧, 🌟, 💪, ➡, 👇, 🙌, and topic-relevant emojis
- Starts with "Nouvel épisode du podcast Demain n'attend pas" or similar announcement
- Personal, enthusiastic tone ("Grande joie d'interviewer", "Je suis une fan inconditionnelle")
- Multiple short paragraphs (3-5 lines each)
- Uses 🎤 emoji before key talking points the guest shares
- Emphasizes giving "un haut-parleur à celles et ceux qui s'engagent" (a megaphone to engaged people)
- Ends with acknowledgments/thanks ("Merci à...")
- Multiple 👇 emojis before link direction ("👇👇👇Lien vers l'épisode en commentaire 👇👇👇")
- Uses relevant hashtags at the very end
- Inspirational and impact-focused language
- Mix of facts/credentials AND emotional connection to the guest's work

TASK:
Write a LinkedIn post (350-500 words) announcing this episode in Delphine's EXACT style.

Structure (MUST FOLLOW):
1. Opening: "Nouvel épisode du podcast Demain n'attend pas 🔥" or variation
2. Personal intro: Why she's excited/honored to interview this guest
3. Guest introduction: Their credentials, impact, and what makes them special
4. Key talking points: 2-3 bullet points with 🎤 emoji of what the guest shares
5. Personal reflection: What she learned or found fascinating
6. Link direction: "👇👇👇Lien vers l'épisode en commentaire 👇👇👇" (or similar)
7. Acknowledgments: "Merci à [guest]" or "Merci à tous ceux qui..."
8. Hashtags: 3-6 relevant hashtags

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

        seo_prompt = f"""You are an SEO expert for "Demain N'attend Pas", a French podcast by Delphine Darmon focusing on climate change, biodiversity loss, and social inequalities. The podcast interviews engaged entrepreneurs, activist artists, impact investors, and NGO founders.

BRAND VOICE & STYLE:
- Authentic, inspiring, and thought-provoking
- Impact-focused: giving a voice to those working to improve the world
- Professional yet warm and accessible
- French-first content with international appeal
- Emphasizes solutions and positive action alongside challenges

{context}

TASK:
Generate a complete SEO package that MATCHES the existing "Demain N'Attend Pas" content style across all platforms:

1. EPISODE TITLES (2-3 options):
   - Attention-grabbing titles that would make people click
   - Match the authentic, impact-focused tone of existing episodes
   - Optimized for French and international audiences
   - Include key themes/guest name
   - 60-80 characters max

2. KEYWORDS & TAGS:
   - 15-20 highly relevant keywords in French (focus: climate, biodiversity, social impact, entrepreneurship, innovation)
   - 10-15 keywords in English
   - Mix of broad and specific terms
   - Consider what people interested in impact/sustainability would search for

3. HASHTAGS:
   - 10-15 hashtags for Instagram/social media
   - Mix of French and English
   - Include: #DemainNAttendPas and other impact/sustainability trending tags
   - Match existing podcast hashtag style

4. PLATFORM-SPECIFIC DESCRIPTIONS (IMPORTANT: Base these on the existing style used by Demain N'Attend Pas on each platform):

   a) SPOTIFY (max 400 chars, French):
      - Match existing Spotify description style for this podcast
      - Hook in first line about the guest's impact/mission
      - Key topics covered
      - Include keywords naturally
      - Warm, inviting tone

   b) APPLE PODCASTS (similar to Spotify, French):
      - Professional yet accessible
      - Focus on guest's credentials and impact
      - What listeners will learn/discover

   c) YOUTUBE (detailed, French):
      - Match the existing YouTube description style
      - Longer description (500-800 chars)
      - Guest introduction and their impact work
      - Key topics and insights discussed
      - Timestamps of key moments (if applicable)
      - Call to action to subscribe/listen on other platforms
      - Keywords integrated naturally
      - Links to podcast platforms

   d) INSTAGRAM (short, punchy, French):
      - 150-200 chars
      - Match existing Instagram caption style
      - Emotional hook about the guest or topic
      - Call to action (listen link in bio)
      - Hashtags separate (will be added automatically)

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
            timestamp = thumb.get('timestamp', 0)
            mins = int(timestamp // 60)
            secs = int(timestamp % 60)
            output += f"{i}. Timestamp: {mins}:{secs:02d}\n"
            output += f"   Description: {thumb.get('description', 'N/A')}\n"
            output += f"   Text Overlay: \"{thumb.get('text_overlay', 'N/A')}\"\n"
            output += f"   Design Notes: {thumb.get('design_notes', 'N/A')}\n"
            output += f"   Why: {thumb.get('why_compelling', 'N/A')}\n\n"

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
