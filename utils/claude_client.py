"""
Claude API client for intelligent analysis
"""
import os
from anthropic import Anthropic


class ClaudeClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found. Please set it in your .env file")
        self.client = Anthropic(api_key=self.api_key)

    def analyze(self, prompt, system_prompt=None, max_tokens=4096, model="claude-sonnet-4-20250514"):
        """Send a prompt to Claude and get analysis"""
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    def analyze_with_context(self, prompt, context, system_prompt=None, max_tokens=4096):
        """Analyze with additional context"""
        full_prompt = f"""Context:
{context}

Task:
{prompt}"""
        return self.analyze(full_prompt, system_prompt, max_tokens)
