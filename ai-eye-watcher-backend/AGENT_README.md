# AI-Eye Watcher Native Agent

A lightweight Python agent that runs natively on macOS to collect system telemetry and execute security commands from the Central Server.

## Features

- **System Telemetry Collection**: Gathers process and network connection data every 15 seconds
- **Command Execution**: Polls for and executes security commands (like process termination) every 60 seconds
- **Native macOS Support**: Uses standard Python libraries compatible with macOS
- **Robust Error Handling**: Graceful handling of permission errors and process lifecycle issues
- **Comprehensive Logging**: Detailed logging to both console and file

## Architecture

```
Agent (agent.py) <---> Central Server (port 9000)
     |                        |
     |-- Collects telemetry   |-- Stores events
     |-- Sends via POST       |-- Analyzes threats
     |-- Polls for commands   |-- Generates commands
     |-- Executes actions     |-- Serves dashboard
```

## Quick Start

### 1. Setup

```bash
# Navigate to the backend directory
cd ai-eye-watcher-backend

# Run the setup script
./setup_agent.sh
```

### 2. Start the Central Server

In one terminal:
```bash
# Activate the server environment
source venv/bin/activate

# Start the Central Server
python3 central_server.py
```

### 3. Run the Agent

In another terminal:
```bash
# Activate the agent environment
source agent_venv/bin/activate

# Run the agent (may need sudo for process killing)
python3 agent.py

# Or with sudo for full capabilities
sudo ./agent_venv/bin/python agent.py
```

## Testing

### Run the Test Suite

```bash
# Activate the agent environment
source agent_venv/bin/activate

# Run comprehensive tests
python3 test_agent.py
```

The test suite will verify:
- Data collection functionality
- Central Server connectivity
- Telemetry transmission
- Command polling
- Process killing capabilities

### Manual Testing

1. **Verify Telemetry Collection**:
   - Check Central Server logs for incoming data every 15 seconds
   - Visit `http://localhost:9000/api/v1/events` to see collected events

2. **Test Command Execution**:
   ```bash
   # Start a test process
   sleep 1000 &
   echo $!  # Note the PID
   
   # Use curl to send a kill command (replace YOUR_PID)
   curl -X POST -H "Content-Type: application/json" \
     -d '{
       "hostname": "'$(hostname)'",
       "timestamp": "'$(date -Iseconds)'",
       "processes": [{"pid": YOUR_PID, "name": "sleep"}],
       "connections": []
     }' \
     http://localhost:9000/api/v1/collect
   
   # The agent should kill the process within 60 seconds
   ```

## Configuration

### Environment Variables

You can customize the agent behavior by modifying these constants in `agent.py`:

```python
CENTRAL_SERVER_URL = "http://localhost:9000"  # Central Server endpoint
COLLECTION_INTERVAL = 15  # Telemetry collection interval (seconds)
COMMAND_POLL_INTERVAL = 60  # Command polling interval (seconds)
```

### Logging

Logs are written to:
- **Console**: Real-time output with timestamps
- **File**: `agent.log` in the current directory

Log levels can be adjusted by modifying the `logging.basicConfig()` call in `agent.py`.

## Data Format

### Telemetry Payload

The agent sends this JSON structure to `/api/v1/collect`:

```json
{
  "hostname": "your-hostname.local",
  "timestamp": "2024-01-15T10:30:00",
  "processes": [
    {
      "pid": 1234,
      "name": "python3",
      "command_line": "python3 agent.py",
      "user": "username",
      "cpu_percent": 2.5,
      "memory_percent": 1.2
    }
  ],
  "connections": [
    {
      "local_address": "127.0.0.1",
      "local_port": 8080,
      "remote_address": "192.168.1.100",
      "remote_port": 443,
      "status": "ESTABLISHED",
      "pid": 1234
    }
  ],
  "system_info": {
    "cpu_count": 8,
    "memory_total": 17179869184,
    "memory_available": 8589934592,
    "boot_time": 1705123456.0,
    "platform": "Darwin"
  }
}
```

### Command Format

The agent receives commands from `/api/v1/commands`:

```json
[
  {
    "command_id": "cmd_1705123456.789",
    "action": "kill_process",
    "target": "1234",
    "parameters": {
      "process_name": "malicious_app",
      "reason": "threat_intel_match"
    }
  }
]
```

## Security Considerations

### Permissions

- **Basic Operation**: The agent can collect most telemetry data with standard user permissions
- **Process Killing**: Requires elevated privileges (sudo) to kill processes owned by other users
- **Network Connections**: Some network data may require elevated privileges on macOS

### Running with Sudo

For full functionality, run the agent with sudo:

```bash
sudo ./agent_venv/bin/python agent.py
```

This ensures the agent can:
- Kill processes owned by any user
- Access all network connection information
- Collect comprehensive process details

### Network Security

- The agent communicates with the Central Server over HTTP (localhost only)
- For production deployments, consider HTTPS and authentication
- Firewall rules should restrict access to the Central Server port (9000)

## Troubleshooting

### Common Issues

1. **"Permission denied" when killing processes**:
   - Run the agent with `sudo`
   - Check that the target process exists and is owned by the current user

2. **"Connection refused" to Central Server**:
   - Ensure the Central Server is running on port 9000
   - Check firewall settings
   - Verify the `CENTRAL_SERVER_URL` configuration

3. **High CPU usage**:
   - Increase the `COLLECTION_INTERVAL` to reduce frequency
   - Check for processes with high CPU that might be causing psutil to work harder

4. **Missing process information**:
   - Some processes may be protected by macOS security features
   - Run with elevated privileges for more complete data

### Debug Mode

Enable debug logging by modifying the logging level in `agent.py`:

```python
logging.basicConfig(level=logging.DEBUG, ...)
```

### Log Analysis

Check the agent logs for detailed information:

```bash
tail -f agent.log
```

## Dependencies

- **psutil**: System and process utilities
- **requests**: HTTP client for API communication
- **schedule**: Simple job scheduling

All dependencies are automatically installed by the setup script.

## Development

### Adding New Commands

To add support for new command types:

1. Add the command logic to the `poll_and_execute_commands()` function
2. Create a new execution function (similar to `execute_kill_process()`)
3. Update the Central Server to generate the new command type

### Extending Telemetry

To collect additional system data:

1. Modify the `collect_system_data()` function
2. Update the data structure sent to the Central Server
3. Ensure the Central Server can handle the new data fields

## License

This project is part of the AI-Eye Watcher security monitoring system.