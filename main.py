from src.event_manager import EventManager
import os
import streamlit as st
from src.chat_window import ChatWindow

def main():
    if not os.getenv('GEMINI_API_KEY'):
        print("Please set your GEMINI_API_KEY environment variable")
        return
    st.title("Meetup Event Assistant")
    chat_interface = ChatWindow()
    chat_interface.display_welcome()

    # manager = EventManager()
    # manager.run()

if __name__ == "__main__":
    main()