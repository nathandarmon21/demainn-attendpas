"""
Prep Agent - Helps prepare for upcoming guest interviews
"""
import json
import requests
from bs4 import BeautifulSoup
from utils.claude_client import ClaudeClient


class PrepAgent:
    def __init__(self, claude_api_key=None):
        self.claude = ClaudeClient(claude_api_key)

    def research_guest(self, guest_name, additional_context=None):
        """
        Research a guest and identify best preparation materials
        """
        print(f"🔍 Researching {guest_name}...")

        # Build research prompt
        context = f"Guest Name: {guest_name}"
        if additional_context:
            context += f"\nAdditional Context: {additional_context}"

        research_prompt = f"""{context}

You are helping to prepare for an interview on "Demain N'Attend Pas", a French intellectual podcast that explores important ideas, thinkers, and contemporary issues.

Your task is to identify the MOST VALUABLE preparation materials for interviewing this guest. Assume the interviewer will do extensive preparation and wants to be as informed as possible, but time is limited so prioritization is key.

Create a comprehensive, prioritized list of preparation materials across these categories:

1. BOOKS (if guest is an author):
   - Which books to read first (in order of priority)
   - For each: Why it's essential for the interview

2. KEY ESSAYS/ARTICLES:
   - Most important written work
   - Where to find them
   - Why they matter for the interview

3. PREVIOUS INTERVIEWS/TALKS:
   - Most revealing interviews they've done
   - Important debates or public appearances
   - What makes each one valuable

4. VIDEOS/DOCUMENTARIES:
   - Key video content featuring the guest
   - Why each is worth watching

5. PODCASTS/AUDIO:
   - Notable podcast appearances
   - Radio interviews or audio content

6. BACKGROUND RESEARCH:
   - Key topics/concepts to understand before the interview
   - Important context about their work or field
   - Controversies or debates they're involved in

7. QUESTIONS TO EXPLORE:
   - Suggested angles for the interview
   - Underexplored topics that would be interesting
   - Questions that might lead to the best conversation

For EACH resource you recommend:
- Provide the specific title/name
- Explain WHY it's valuable for interview prep
- Estimate time commitment (e.g., "2 hours", "15 min read")
- Priority level: ESSENTIAL, HIGH, MEDIUM

Format your response as JSON:
{{
  "guest_overview": "Brief 2-3 sentence overview of who they are and why they matter",
  "books": [
    {{
      "title": "Book title",
      "priority": "ESSENTIAL",
      "time_commitment": "X hours",
      "why_read": "Explanation of value",
      "language": "French/English"
    }}
  ],
  "essays_articles": [...],
  "interviews_talks": [...],
  "videos": [...],
  "podcasts": [...],
  "background_research": [...],
  "interview_angles": [
    {{
      "topic": "Topic/angle",
      "why_interesting": "Why this would make a good conversation"
    }}
  ]
}}

Be specific with titles, URLs where possible, and prioritize ruthlessly. The interviewer wants the HIGHEST value materials, not an exhaustive list.

Return ONLY valid JSON."""

        response = self.claude.analyze(
            research_prompt,
            max_tokens=4096,
            model="claude-sonnet-4-20250514"
        )

        # Parse response
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            prep_package = json.loads(json_str)
            return prep_package
        except json.JSONDecodeError as e:
            print(f"Error parsing response: {e}")
            return None

    def format_prep_guide(self, prep_package, guest_name):
        """
        Format preparation guide into readable output
        """
        if not prep_package:
            return "Error: Could not generate prep guide"

        output = f"""
╔════════════════════════════════════════════════════════════════╗
║              INTERVIEW PREPARATION GUIDE                        ║
║                  {guest_name.center(50)}                ║
╚════════════════════════════════════════════════════════════════╝

{prep_package.get('guest_overview', '')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 BOOKS TO READ (in priority order)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, book in enumerate(prep_package.get('books', []), 1):
            priority_emoji = "🔴" if book['priority'] == "ESSENTIAL" else "🟡" if book['priority'] == "HIGH" else "🟢"
            output += f"{i}. {priority_emoji} {book['title']} ({book.get('language', 'N/A')})\n"
            output += f"   ⏱️  Time: {book['time_commitment']}\n"
            output += f"   💡 Why: {book['why_read']}\n\n"

        output += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 KEY ESSAYS & ARTICLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, article in enumerate(prep_package.get('essays_articles', []), 1):
            priority_emoji = "🔴" if article['priority'] == "ESSENTIAL" else "🟡" if article['priority'] == "HIGH" else "🟢"
            output += f"{i}. {priority_emoji} {article['title']}\n"
            output += f"   ⏱️  Time: {article['time_commitment']}\n"
            output += f"   💡 Why: {article['why_read']}\n\n"

        output += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎤 PREVIOUS INTERVIEWS & TALKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, interview in enumerate(prep_package.get('interviews_talks', []), 1):
            priority_emoji = "🔴" if interview['priority'] == "ESSENTIAL" else "🟡" if interview['priority'] == "HIGH" else "🟢"
            output += f"{i}. {priority_emoji} {interview['title']}\n"
            output += f"   ⏱️  Time: {interview['time_commitment']}\n"
            output += f"   💡 Why: {interview['why_read']}\n\n"

        output += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎥 VIDEOS & DOCUMENTARIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, video in enumerate(prep_package.get('videos', []), 1):
            priority_emoji = "🔴" if video['priority'] == "ESSENTIAL" else "🟡" if video['priority'] == "HIGH" else "🟢"
            output += f"{i}. {priority_emoji} {video['title']}\n"
            output += f"   ⏱️  Time: {video['time_commitment']}\n"
            output += f"   💡 Why: {video['why_read']}\n\n"

        output += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎧 PODCASTS & AUDIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, podcast in enumerate(prep_package.get('podcasts', []), 1):
            priority_emoji = "🔴" if podcast['priority'] == "ESSENTIAL" else "🟡" if podcast['priority'] == "HIGH" else "🟢"
            output += f"{i}. {priority_emoji} {podcast['title']}\n"
            output += f"   ⏱️  Time: {podcast['time_commitment']}\n"
            output += f"   💡 Why: {podcast['why_read']}\n\n"

        output += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 BACKGROUND RESEARCH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, bg in enumerate(prep_package.get('background_research', []), 1):
            priority_emoji = "🔴" if bg['priority'] == "ESSENTIAL" else "🟡" if bg['priority'] == "HIGH" else "🟢"
            output += f"{i}. {priority_emoji} {bg['title']}\n"
            output += f"   ⏱️  Time: {bg['time_commitment']}\n"
            output += f"   💡 Why: {bg['why_read']}\n\n"

        output += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 SUGGESTED INTERVIEW ANGLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, angle in enumerate(prep_package.get('interview_angles', []), 1):
            output += f"{i}. {angle['topic']}\n"
            output += f"   💭 {angle['why_interesting']}\n\n"

        output += "="*70 + "\n"
        output += "\n🔴 ESSENTIAL  🟡 HIGH PRIORITY  🟢 MEDIUM PRIORITY\n"

        return output

    def run_prep_analysis(self, guest_name, additional_context=None):
        """
        Complete preparation analysis pipeline
        """
        print("🚀 Starting Prep Agent Analysis...\n")

        prep_package = self.research_guest(guest_name, additional_context)

        if not prep_package:
            return "❌ Research failed. Please try again."

        formatted_guide = self.format_prep_guide(prep_package, guest_name)

        print("✅ Prep guide generated successfully!\n")

        return formatted_guide, prep_package
