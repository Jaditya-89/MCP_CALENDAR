import json
import os
from datetime import datetime
from mcp.server.mcpserver import MCPServer

# Initialize MCPServer (Updated for MCP 2.x)
mcp = MCPServer("Local Calendar Manager")
CALENDAR_FILE = "calendar.json"

def _load_calendar() -> list:
    """Helper to load events from the local JSON file."""
    if not os.path.exists(CALENDAR_FILE):
        return []
    try:
        with open(CALENDAR_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def _save_calendar(events: list):
    """Helper to save events to the local JSON file."""
    with open(CALENDAR_FILE, "w") as f:
        json.dump(events, f, indent=2)

@mcp.tool()
def list_events() -> str:
    """
    Retrieve all scheduled calendar events. 
    Use this to check the user's availability or read their itinerary.
    """
    events = _load_calendar()
    if not events:
        return "Your calendar is completely empty."
    
    output = "Current Calendar Events:\n"
    for i, event in enumerate(events, 1):
        output += f"{i}. [{event['date']} {event['time']}] {event['title']}"
        if event.get('description'):
            output += f" - {event['description']}"
        output += "\n"
    return output

@mcp.tool()
def add_event(title: str, date: str, time: str, description: str = "") -> str:
    """
    Add a new event to the calendar.
    
    Args:
        title: The name/summary of the event (e.g., "Dentist Appointment").
        date: The date in YYYY-MM-DD format (e.g., "2026-10-15").
        time: The time in HH:MM format (e.g., "14:30").
        description: Optional extra details or notes about the event.
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(time, "%H:%M")
    except ValueError:
        return "Error: Date must be YYYY-MM-DD and time must be HH:MM."

    events = _load_calendar()
    new_event = {
        "title": title,
        "date": date,
        "time": time,
        "description": description
    }
    events.append(new_event)
    
    events.sort(key=lambda x: (x['date'], x['time']))
    _save_calendar(events)
    
    return f"Successfully added event: '{title}' on {date} at {time}."

@mcp.tool()
def clear_calendar() -> str:
    """Wipe out all events from the calendar file."""
    _save_calendar([])
    return "Calendar cleared successfully."

if __name__ == "__main__":
    mcp.run()
