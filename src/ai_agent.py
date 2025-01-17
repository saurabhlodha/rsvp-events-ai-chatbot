from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import GEMINI_API_KEY, SYSTEM_PROMPT, EVENT_ANALYSIS_PROMPT

class AIEventAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=GEMINI_API_KEY,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        self.chat_history = []

    def analyze_events(self, events, user_interests=None):
        events_text = "\n".join([
            f"- {event['title']} ({event['platform']}) on {event['date']}"
            for event in events
        ])
        
        messages = [
            ("system", SYSTEM_PROMPT),
            ("user", f"{EVENT_ANALYSIS_PROMPT}\n\nEvents:\n{events_text}")
        ]

        response = self.llm.invoke(messages)
        return response.content

    def get_response(self, user_input, context=None):
        messages = [("system", SYSTEM_PROMPT)]

        # Add chat history for context
        for msg in self.chat_history[-3:]:  # Keep last 3 messages for context
            messages.append(msg)
            
        # Add current context if available
        if context:
            messages.append(("system", f"Context: {context}"))

        # Add user input
        messages.append(("user", user_input))
        response = self.llm.invoke(messages)
        print(response)

        # Update chat history
        self.chat_history.append(("user", user_input))
        # self.chat_interface.append(("assistant", response.content))

        return response.content
