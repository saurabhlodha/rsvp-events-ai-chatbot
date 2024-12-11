import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Prompts for the AI
SYSTEM_PROMPT = """You are an AI assistant that helps users find and RSVP to events on Meetup.com and Lu.ma. 
Your role is to understand the user's preferences and help them make decisions about which events to attend.
Be friendly, concise, and helpful."""

EVENT_ANALYSIS_PROMPT = """Analyze these events and provide personalized recommendations based on the user's interests.
Consider factors like:
1. Event topic and relevance
2. Date and time
3. Location (if available)
4. Any special requirements

Format your response in a conversational way, highlighting the most relevant events first."""