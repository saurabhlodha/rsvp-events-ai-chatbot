import os
import streamlit as st

class ChatWindow:
    def __init__(self):
        st.session_state.scraper = None
        st.session_state.events = []
        st.session_state.logged_in = False

    def display_welcome(self):
        with st.sidebar:
            openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
            "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
            "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

        welcome_text = """
                # 🎉 AI Event Assistant
                
                Welcome! I'll help you find and RSVP to events on Meetup.com and Lu.ma.
                I can:
                - Find events based on your interests
                - Analyze events and make recommendations
                - Help you RSVP to events you like
                
                Let's start by getting to know your interests!
        """

        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": welcome_text}]

        # with st.chat_message('user', avatar=None):
        #     st.write("Hello 👋")

        user_input = st.chat_input(placeholder="Add your response")
        st.session_state.messages.append({"role": "user", "content": user_input})
        print(st.session_state.messages)

        for msg in st.session_state.messages:
            if msg["content"]: st.chat_message(msg["role"]).write(msg["content"])
            # st.chat_message("user").write(user_input)
            # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
            # msg = response.choices[0].message.content
            # st.session_state.messages.append({"role": "assistant", "content": msg})
            # st.chat_message("assistant").write(msg)
