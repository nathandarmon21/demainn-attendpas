"""
Analytics Agent - Analyzes episode performance and identifies patterns
"""
import json
import pandas as pd
from utils.claude_client import ClaudeClient


class AnalyticsAgent:
    def __init__(self, claude_api_key=None):
        self.claude = ClaudeClient(claude_api_key)

    def load_analytics_data(self, file_path=None, data_dict=None):
        """
        Load analytics data from file or dictionary
        Supports CSV, JSON, or direct dictionary input
        """
        if data_dict:
            return pd.DataFrame(data_dict)

        if file_path:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                return pd.DataFrame(data)

        return None

    def analyze_episodes(self, analytics_data, episode_selection="all", specific_episodes=None):
        """
        Analyze episode performance using Claude

        episode_selection: "all", "last", "topic", "manual"
        specific_episodes: list of episode identifiers if manual selection
        """
        if analytics_data is None or len(analytics_data) == 0:
            return "No analytics data available"

        # Filter data based on selection
        filtered_data = self._filter_episodes(analytics_data, episode_selection, specific_episodes)

        if filtered_data is None or len(filtered_data) == 0:
            return "No episodes match the selection criteria"

        print(f"📊 Analyzing {len(filtered_data)} episode(s)...")

        # Prepare data summary for Claude
        data_summary = self._prepare_data_summary(filtered_data)

        analysis_prompt = f"""You are analyzing podcast analytics for "Demain N'Attend Pas", a French intellectual podcast.

ANALYTICS DATA:
{data_summary}

Your task is to conduct a comprehensive performance analysis and identify actionable insights.

Analyze the data to answer:

1. PERFORMANCE PATTERNS:
   - Which episodes performed best? Why?
   - Which episodes underperformed? Why?
   - What patterns emerge in successful episodes?

2. ENGAGEMENT METRICS:
   - What drives higher completion rates?
   - What correlates with more shares/saves?
   - Which topics generate most engagement?

3. AUDIENCE INSIGHTS:
   - What types of content resonate most?
   - Are there topic/format patterns in top performers?
   - Platform-specific insights (if data available)

4. CONTENT RECOMMENDATIONS:
   - What topics should be covered more?
   - What guest types work best?
   - What episode lengths are optimal?
   - What posting times/days perform better?

5. OPTIMIZATION OPPORTUNITIES:
   - Specific, actionable recommendations
   - What to do more of
   - What to change or avoid
   - Testing suggestions

6. SEO & DISCOVERY:
   - Which keywords/tags drove most traffic?
   - What titles performed best?
   - Discovery pattern insights

Return your analysis as a structured JSON:
{{
  "executive_summary": "2-3 sentence overview of key findings",
  "top_performers": [
    {{
      "episode": "Episode identifier",
      "metrics": "Key performance metrics",
      "why_successful": "Explanation"
    }}
  ],
  "underperformers": [...],
  "engagement_insights": [
    {{
      "pattern": "What you observed",
      "evidence": "Data supporting this",
      "implication": "What this means"
    }}
  ],
  "audience_insights": [...],
  "content_recommendations": [
    {{
      "recommendation": "Specific action",
      "rationale": "Why this will help",
      "priority": "HIGH/MEDIUM/LOW"
    }}
  ],
  "optimization_opportunities": [...],
  "seo_insights": [...]
}}

Be specific, data-driven, and actionable. Focus on insights that can improve future episodes.

Return ONLY valid JSON."""

        response = self.claude.analyze(analysis_prompt, max_tokens=4096)

        # Parse response
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            analysis = json.loads(json_str)
            return analysis
        except json.JSONDecodeError as e:
            print(f"Error parsing analysis: {e}")
            return None

    def _filter_episodes(self, data, selection, specific_episodes):
        """Filter episodes based on selection criteria"""
        if selection == "all":
            return data
        elif selection == "last":
            return data.tail(1)
        elif selection == "manual" and specific_episodes:
            # Assume specific_episodes is list of indices or identifiers
            return data[data.index.isin(specific_episodes)]
        # For "topic", would need topic column - implement if data has it
        return data

    def _prepare_data_summary(self, data):
        """Prepare a summary of analytics data for Claude"""
        summary = f"Total Episodes Analyzed: {len(data)}\n\n"

        # Basic statistics
        summary += "COLUMN OVERVIEW:\n"
        for col in data.columns:
            summary += f"- {col}\n"

        summary += f"\nDATA SAMPLE (first 5 rows):\n"
        summary += data.head().to_string()

        summary += f"\n\nSTATISTICAL SUMMARY:\n"
        summary += data.describe().to_string()

        # If data is not too large, include all rows
        if len(data) <= 20:
            summary += f"\n\nFULL DATA:\n"
            summary += data.to_string()

        return summary

    def format_analysis_report(self, analysis):
        """Format analysis into readable report"""
        if not analysis:
            return "Error: Could not generate analysis"

        output = """
╔════════════════════════════════════════════════════════════════╗
║                  ANALYTICS INSIGHTS REPORT                      ║
║                    Demain N'Attend Pas                         ║
╚════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 EXECUTIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        output += analysis.get('executive_summary', 'No summary available') + "\n"

        output += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 TOP PERFORMING EPISODES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, ep in enumerate(analysis.get('top_performers', []), 1):
            output += f"{i}. {ep.get('episode', 'Unknown episode')}\n"
            output += f"   📊 Metrics: {ep.get('metrics', 'N/A')}\n"
            output += f"   💡 Why: {ep.get('why_successful', 'No description')}\n\n"

        output += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📉 UNDERPERFORMING EPISODES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, ep in enumerate(analysis.get('underperformers', []), 1):
            output += f"{i}. {ep.get('episode', 'Unknown episode')}\n"
            output += f"   📊 Metrics: {ep.get('metrics', 'N/A')}\n"
            output += f"   💡 Why: {ep.get('why_successful', 'No description')}\n\n"

        output += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 ENGAGEMENT INSIGHTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, insight in enumerate(analysis.get('engagement_insights', []), 1):
            output += f"{i}. {insight.get('pattern', 'Pattern')}\n"
            output += f"   📊 Evidence: {insight.get('evidence', 'N/A')}\n"
            output += f"   💡 Implication: {insight.get('implication', 'No description')}\n\n"

        output += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 AUDIENCE INSIGHTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, insight in enumerate(analysis.get('audience_insights', []), 1):
            output += f"{i}. {insight.get('pattern', 'Pattern')}\n"
            output += f"   📊 Evidence: {insight.get('evidence', 'N/A')}\n"
            output += f"   💡 Implication: {insight.get('implication', 'No description')}\n\n"

        output += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 CONTENT RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, rec in enumerate(analysis.get('content_recommendations', []), 1):
            priority_emoji = "🔴" if rec.get('priority') == "HIGH" else "🟡" if rec.get('priority') == "MEDIUM" else "🟢"
            output += f"{i}. {priority_emoji} {rec.get('recommendation', 'Recommendation')}\n"
            output += f"   💡 Rationale: {rec.get('rationale', 'No description')}\n\n"

        output += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ OPTIMIZATION OPPORTUNITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, opp in enumerate(analysis.get('optimization_opportunities', []), 1):
            priority_emoji = "🔴" if opp.get('priority') == "HIGH" else "🟡" if opp.get('priority') == "MEDIUM" else "🟢"
            output += f"{i}. {priority_emoji} {opp.get('recommendation', 'Recommendation')}\n"
            output += f"   💡 Rationale: {opp.get('rationale', 'No description')}\n\n"

        output += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 SEO & DISCOVERY INSIGHTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        for i, seo in enumerate(analysis.get('seo_insights', []), 1):
            output += f"{i}. {seo.get('pattern', 'Pattern')}\n"
            output += f"   📊 Evidence: {seo.get('evidence', 'N/A')}\n"
            output += f"   💡 Implication: {seo.get('implication', 'No description')}\n\n"

        output += "="*70 + "\n"
        output += "\n🔴 HIGH PRIORITY  🟡 MEDIUM PRIORITY  🟢 LOW PRIORITY\n"

        return output

    def run_analysis(self, analytics_data, episode_selection="all", specific_episodes=None):
        """
        Complete analytics pipeline
        """
        print("🚀 Starting Analytics Agent Analysis...\n")

        analysis = self.analyze_episodes(analytics_data, episode_selection, specific_episodes)

        if not analysis:
            return "❌ Analysis failed. Please check your data and try again."

        formatted_report = self.format_analysis_report(analysis)

        print("✅ Analytics report generated successfully!\n")

        return formatted_report, analysis
