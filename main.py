from src.event_manager import EventManager
import os

def main():
    if not os.getenv('GEMINI_API_KEY'):
        print("Please set your GEMINI_API_KEY environment variable")
        return
        
    manager = EventManager()
    manager.run()

if __name__ == "__main__":
    main()