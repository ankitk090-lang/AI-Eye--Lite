# AI-Eye Watcher Backend

A lightweight FastAPI-based central server for the AI-Eye watcher system. This server acts as the ingestion point for telemetry data, performs real-time threat analysis, manages commands, and serves data to the UI.

## Features

- **Telemetry Ingestion**: Receives process and connection data from agents
- **Threat Intelligence**: Matches against known bad processes
- **Real-time Alerts**: Generates alerts for suspicious activities
- **Command Management**: Issues commands to agents (e.g., kill processes)
- **Dashboard API**: Provides statistics and data for the UI
- **In-Memory Storage**: Uses Python collections for fast, lightweight operation

## Quick Start

### 1. Setup Environment

```bash
# Run the setup script
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start Server

```bash
# Activate virtual environment
source venv/bin/activate

# Start server with auto-reload
uvicorn central_server:app --reload --port 9000

# Or run directly
python central_server.py
```

The server will start on `http://localhost:9000`

### 3. View API Documentation

Visit `http://localhost:9000/docs` for interactive API documentation.

## API Endpoints

### Core Endpoints

- `POST /api/v1/collect` - Ingest telemetry data
- `GET /api/v1/commands?host=<hostname>` - Poll for commands
- `GET /api/v1/dashboard/stats` - Dashboard statistics
- `GET /api/v1/alerts` - Recent alerts
- `GET /health` - Health check

### Data Models

**TelemetryPayload**:
```json
{
  "hostname": "host-01",
  "timestamp": "2024-01-01T12:00:00",
  "processes": [
    {
      "pid": 1234,
      "name": "chrome",
      "command_line": "/Applications/Chrome.app/Contents/MacOS/Chrome",
      "user": "user",
      "cpu_percent": 5.2,
      "memory_percent": 12.1
    }
  ],
  "connections": [
    {
      "local_address": "127.0.0.1",
      "local_port": 9000,
      "status": "LISTEN",
      "pid": 1234
    }
  ]
}
```

## Testing

### Automated Tests

```bash
# Start the server first
uvicorn central_server:app --port 9000

# In another terminal, run tests
python test_server.py
```

### Manual Testing with curl

```bash
# Test health
curl http://localhost:9000/health

# Send normal telemetry
curl -X POST http://localhost:9000/api/v1/collect \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "test-host",
    "timestamp": "2024-01-01T12:00:00",
    "processes": [
      {"pid": 1234, "name": "chrome", "user": "testuser"}
    ]
  }'

# Send malicious telemetry (triggers alerts)
curl -X POST http://localhost:9000/api/v1/collect \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "test-host",
    "timestamp": "2024-01-01T12:00:00",
    "processes": [
      {"pid": 9999, "name": "nc.exe", "user": "attacker"}
    ]
  }'

# Check alerts
curl http://localhost:9000/api/v1/alerts

# Check commands
curl "http://localhost:9000/api/v1/commands?host=test-host"

# Check stats
curl http://localhost:9000/api/v1/dashboard/stats
```

## Threat Intelligence

The server includes basic threat intelligence matching against known bad processes:

- `nc.exe` - Netcat
- `mimikatz.exe` - Credential dumping tool
- `evil.sh` - Generic malicious script
- `netcat` - Netcat variants
- `ncat` - Nmap's netcat

When a match is found:
1. A HIGH severity alert is generated
2. A `kill_process` command is queued for the host
3. The event is stored for analysis

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Agent/UI      │───▶│  Central Server  │───▶│  In-Memory      │
│                 │    │  (FastAPI)       │    │  Storage        │
│ - Sends data    │    │                  │    │                 │
│ - Polls commands│    │ - Ingests data   │    │ - recent_events │
│ - Gets alerts   │    │ - Analyzes       │    │ - recent_alerts │
│                 │    │ - Generates cmds │    │ - pending_cmds  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Development

### Adding New Threat Intelligence

Edit the `KNOWN_BAD_PROCESSES` set in `central_server.py`:

```python
KNOWN_BAD_PROCESSES = {
    'nc.exe', 'mimikatz.exe', 'evil.sh',
    'your_new_bad_process.exe'
}
```

### Adding New Alert Types

Create new alert logic in the `/api/v1/collect` endpoint:

```python
# Example: Detect high CPU usage
if process.cpu_percent and process.cpu_percent > 90:
    alert = {
        "finding_type": "high_cpu_usage",
        "severity": "MEDIUM",
        "timestamp": datetime.datetime.now().isoformat(),
        "details": f"Process '{process.name}' using {process.cpu_percent}% CPU",
        "host": payload.hostname,
        "process_pid": process.pid
    }
    recent_alerts.append(alert)
```

## Production Considerations

For production deployment, consider:

- Replace in-memory storage with persistent databases
- Add authentication and authorization
- Implement rate limiting
- Add logging and monitoring
- Use proper configuration management
- Add data retention policies
- Implement backup and recovery