from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from scraper import EventScraper
import getpass

console = Console()

def get_credentials():
    console.print("\n[bold blue]Please enter your credentials[/bold blue]")
    
    meetup_email = Prompt.ask("Meetup.com email")
    meetup_password = getpass.getpass("Meetup.com password: ")
    
    luma_email = Prompt.ask("Lu.ma email")
    luma_password = getpass.getpass("Lu.ma password: ")
    
    return {
        'meetup': (meetup_email, meetup_password),
        'luma': (luma_email, luma_password)
    }

def display_events(events):
    if not events:
        console.print("[yellow]No events found[/yellow]")
        return
        
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
    
    console.print(table)
    return table

def main():
    console.print("[bold green]Welcome to the Event RSVP Assistant![/bold green]")
    
    # Get credentials
    creds = get_credentials()
    
    # Initialize scraper
    scraper = EventScraper()
    scraper.setup_driver()
    
    # Login to platforms
    console.print("\n[bold]Logging in to platforms...[/bold]")
    
    meetup_success = scraper.login_meetup(*creds['meetup'])
    if meetup_success:
        console.print("[green]✓[/green] Logged in to Meetup.com")
    else:
        console.print("[red]✗[/red] Failed to log in to Meetup.com")
        
    luma_success = scraper.login_luma(*creds['luma'])
    if luma_success:
        console.print("[green]✓[/green] Logged in to Lu.ma")
    else:
        console.print("[red]✗[/red] Failed to log in to Lu.ma")
    
    # Fetch events
    console.print("\n[bold]Fetching events...[/bold]")
    all_events = []
    
    if meetup_success:
        meetup_events = scraper.get_meetup_events()
        all_events.extend(meetup_events)
        
    if luma_success:
        luma_events = scraper.get_luma_events()
        all_events.extend(luma_events)
    
    # Display events
    console.print("\n[bold]Available Events:[/bold]")
    display_events(all_events)
    
    # RSVP flow
    while True:
        choice = Prompt.ask(
            "\nEnter event number to RSVP (or 'q' to quit)",
            default="q"
        )
        
        if choice.lower() == 'q':
            break
            
        try:
            event_idx = int(choice) - 1
            if 0 <= event_idx < len(all_events):
                event = all_events[event_idx]
                console.print(f"\nRSVPing to: {event['title']}")
                
                if scraper.rsvp_event(event):
                    console.print("[green]Successfully RSVP'd![/green]")
                else:
                    console.print("[red]Failed to RSVP[/red]")
            else:
                console.print("[red]Invalid event number[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")
    
    # Cleanup
    scraper.cleanup()
    console.print("\n[bold green]Thank you for using Event RSVP Assistant![/bold green]")

if __name__ == "__main__":
    main()