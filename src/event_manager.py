from .scraper import EventScraper
from .ai_agent import AIEventAgent
from .chat_interface import ChatInterface

class EventManager:
    def __init__(self):
        self.scraper = EventScraper()
        self.ai_agent = AIEventAgent()
        self.chat_interface = ChatInterface()
        self.events = []
        self.user_interests = None

    def initialize(self):
        self.chat_interface.display_welcome()
        self.get_user_interests()
        self.setup_scraper()

    def get_user_interests(self):
        self.user_interests = self.chat_interface.get_user_input(
            "Tell me about your interests (e.g., technology, art, sports):"
        )
        response = self.ai_agent.get_response(
            f"User interests: {self.user_interests}. Acknowledge and suggest what kinds of events they might like."
        )
        self.chat_interface.display_message(response)

    def setup_scraper(self):
        self.scraper.setup_driver()
        self._handle_login()

    def _handle_login(self):
        self.chat_interface.display_message("Let's log in to your accounts.")
        
        # Meetup login
        meetup_email = self.chat_interface.get_user_input("Meetup.com email:")
        meetup_password = self.chat_interface.get_user_input("Meetup.com password:")
        
        if self.scraper.login_meetup(meetup_email, meetup_password):
            self.chat_interface.display_message("✓ Logged in to Meetup.com", "success")
        else:
            self.chat_interface.display_message("✗ Failed to log in to Meetup.com", "error")

        # Lu.ma login
        luma_email = self.chat_interface.get_user_input("Lu.ma email:")
        luma_password = self.chat_interface.get_user_input("Lu.ma password:")
        
        if self.scraper.login_luma(luma_email, luma_password):
            self.chat_interface.display_message("✓ Logged in to Lu.ma", "success")
        else:
            self.chat_interface.display_message("✗ Failed to log in to Lu.ma", "error")

    def fetch_and_analyze_events(self):
        self.chat_interface.display_message("Fetching events...")
        
        meetup_events = self.scraper.get_meetup_events()
        luma_events = self.scraper.get_luma_events()
        self.events = meetup_events + luma_events
        
        # Get AI analysis of events
        analysis = self.ai_agent.analyze_events(self.events, self.user_interests)
        self.chat_interface.display_events(self.events, analysis)

    def handle_rsvp(self, event_idx):
        if 0 <= event_idx < len(self.events):
            event = self.events[event_idx]
            
            # Get AI opinion about the event
            opinion = self.ai_agent.get_response(
                f"Should I attend this event: {event['title']} on {event['date']}? "
                f"Consider my interests: {self.user_interests}"
            )
            self.chat_interface.display_message(f"AI Opinion: {opinion}")
            
            if self.chat_interface.get_user_input("Would you like to RSVP? (y/n)").lower() == 'y':
                if self.scraper.rsvp_event(event):
                    self.chat_interface.display_message("Successfully RSVP'd!", "success")
                else:
                    self.chat_interface.display_message("Failed to RSVP", "error")
        else:
            self.chat_interface.display_message("Invalid event number", "error")

    def cleanup(self):
        self.scraper.cleanup()

    def run(self):
        try:
            self.initialize()
            
            while True:
                self.chat_interface.display_message("\nWhat would you like to do?")
                self.chat_interface.display_message("""
1. Fetch and analyze events
2. RSVP to an event
3. Chat about events
4. Exit
                """)
                
                choice = self.chat_interface.get_user_input("Enter your choice (1-4):")
                
                if choice == '1':
                    self.fetch_and_analyze_events()
                elif choice == '2':
                    event_num = self.chat_interface.get_user_input("Enter event number:")
                    try:
                        self.handle_rsvp(int(event_num) - 1)
                    except ValueError:
                        self.chat_interface.display_message("Please enter a valid number", "error")
                elif choice == '3':
                    user_input = self.chat_interface.get_user_input("What would you like to know?")
                    response = self.ai_agent.get_response(user_input)
                    self.chat_interface.display_message(response)
                elif choice == '4':
                    break
                else:
                    self.chat_interface.display_message("Invalid choice", "error")
                    
        finally:
            self.cleanup()