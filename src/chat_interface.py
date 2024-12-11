from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

class ChatInterface:
    def __init__(self):
        self.console = Console()

    def display_welcome(self):
        welcome_text = """
# 🎉 AI Event Assistant

Welcome! I'll help you find and RSVP to events on Meetup.com and Lu.ma.
I can:
- Find events based on your interests
- Analyze events and make recommendations
- Help you RSVP to events you like

Let's start by getting to know your interests!
        """
        self.console.print(Markdown(welcome_text))

    def get_user_input(self, prompt_text="What would you like to do?"):
        return Prompt.ask(prompt_text)

    def display_message(self, message, style="info"):
        if style == "info":
            self.console.print(Panel(message, style="blue"))
        elif style == "success":
            self.console.print(Panel(message, style="green"))
        elif style == "error":
            self.console.print(Panel(message, style="red"))
        else:
            self.console.print(message)

    def display_events(self, events, ai_analysis=None):
        if not events:
            self.display_message("No events found", style="error")
            return

        # Display events in a table
        from rich.table import Table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim")
        table.add_column("Platform")
        table.add_column("Title")
        table.add_column("Date")
        
        for idx, event in enumerate(events, 1):
            table.add_row(
                str(idx),
                event['platform'],
                event['title'],
                event['date']
            )
        
        self.console.print("\n[bold]Available Events:[/bold]")
        self.console.print(table)
        
        if ai_analysis:
            self.console.print("\n[bold]AI Analysis:[/bold]")
            self.console.print(Panel(ai_analysis, style="cyan"))