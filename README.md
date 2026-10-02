# Local Calendar Manager (MCP Server)

A small [Model Context Protocol](https://modelcontextprotocol.io) server that gives AI assistants (such as GitHub Copilot in VS Code) a simple local calendar. Events are stored in a plain JSON file on your machine.

## Features

The server exposes three **tools**:

| Tool | Parameters | Description |
|---|---|---|
| `list_events` | — | Returns all scheduled events, sorted by date and time. |
| `add_event` | `title`, `date` (`YYYY-MM-DD`), `time` (`HH:MM`, 24h), `description` *(optional)* | Validates the input and adds a new event. |
| `clear_calendar` | — | Removes all events. |

No resources or prompts are defined.

## Requirements

- Python 3.10+
- [`mcp`](https://pypi.org/project/mcp/) Python SDK 2.x (uses `mcp.server.mcpserver.MCPServer`)

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "mcp>=2"
```

## Usage

### VS Code (Copilot Chat)

The repository includes [.vscode/mcp.json](.vscode/mcp.json), which registers the server as `calendar`:

```json
{
  "servers": {
    "calendar": {
      "type": "stdio",
      "command": "${workspaceFolder}/.venv/bin/python",
      "args": ["${workspaceFolder}/server.py"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

1. Open the folder in VS Code.
2. Start the `calendar` server (from `mcp.json` or the **MCP: List Servers** command).
3. In Copilot Chat (Agent mode), ask things like:
   - "What is on my calendar?"
   - "Add an event called *Team sync* on 2026-10-05 at 10:30."
   - "Clear my calendar."

### Run standalone

```bash
.venv/bin/python server.py
```

The server communicates over stdio, so it is normally launched by an MCP client rather than used directly.

## Data storage

Events are saved to `calendar.json` in the server's working directory:

```json
[
  {
    "title": "event 1",
    "date": "2026-10-02",
    "time": "16:00",
    "description": ""
  }
]
```

The file is created automatically when the first event is added. If it is missing or contains invalid JSON, the calendar is treated as empty.

## Project structure

```
.
├── .vscode/
│   └── mcp.json      # VS Code MCP server configuration
├── calendar.json     # Event storage (auto-created)
├── server.py         # MCP server implementation
└── README.md
```
