from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from collections import deque
import datetime

# Initialize FastAPI app
app = FastAPI(title="AI-Eye Watcher Central Server", version="1.0.0")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global in-memory data stores
recent_events = deque(maxlen=1000)  # Store last 1000 events
recent_alerts = deque(maxlen=100)   # Store last 100 alerts
pending_commands: Dict[str, List[Dict[str, Any]]] = {}  # Commands keyed by hostname

# Known bad processes for threat intel matching
KNOWN_BAD_PROCESSES = {'nc.exe', 'mimikatz.exe', 'evil.sh', 'netcat', 'ncat'}

# Pydantic Models
class ProcessEvent(BaseModel):
    pid: int
    name: str
    command_line: Optional[str] = None
    user: Optional[str] = None
    cpu_percent: Optional[float] = None
    memory_percent: Optional[float] = None

class ConnectionEvent(BaseModel):
    local_address: str
    local_port: int
    remote_address: Optional[str] = None
    remote_port: Optional[int] = None
    status: str
    pid: Optional[int] = None

class TelemetryPayload(BaseModel):
    hostname: str
    timestamp: str
    processes: List[ProcessEvent]
    connections: Optional[List[ConnectionEvent]] = []
    system_info: Optional[Dict[str, Any]] = {}

class Command(BaseModel):
    command_id: str
    action: str
    target: str
    parameters: Optional[Dict[str, Any]] = {}

# API Endpoints
@app.post("/api/v1/collect")
async def collect_telemetry(payload: TelemetryPayload):
    """
    Ingestion endpoint for telemetry data.
    Stores events, performs threat intel checks, and generates alerts/commands.
    """
    # Store the event
    event_data = payload.model_dump()
    event_data["received_at"] = datetime.datetime.now().isoformat()
    recent_events.append(event_data)
    
    # Basic threat intel check on processes
    for process in payload.processes:
        if process.name.lower() in KNOWN_BAD_PROCESSES:
            # Create alert
            alert = {
                "finding_type": "threat_intel_match_process",
                "severity": "HIGH",
                "timestamp": datetime.datetime.now().isoformat(),
                "details": f"Known bad process '{process.name}' detected.",
                "host": payload.hostname,
                "process_pid": process.pid,
                "process_name": process.name,
                "original_event": payload.model_dump()
            }
            recent_alerts.append(alert)
            
            # Generate kill command
            host_cmds = pending_commands.setdefault(payload.hostname, [])
            command = {
                "command_id": f"cmd_{datetime.datetime.now().timestamp()}",
                "action": "kill_process",
                "target": str(process.pid),
                "parameters": {
                    "process_name": process.name,
                    "reason": "threat_intel_match"
                }
            }
            host_cmds.append(command)
    
    # Basic anomaly check (placeholder)
    # Check for processes not seen recently
    recent_process_names = set()
    for event in list(recent_events)[-50:]:  # Check last 50 events
        if "processes" in event:
            for proc in event["processes"]:
                recent_process_names.add(proc.get("name", "").lower())
    
    for process in payload.processes:
        if process.name.lower() not in recent_process_names and len(recent_events) > 10:
            alert = {
                "finding_type": "anomaly_new_process",
                "severity": "LOW",
                "timestamp": datetime.datetime.now().isoformat(),
                "details": f"New/unusual process '{process.name}' detected.",
                "host": payload.hostname,
                "process_pid": process.pid,
                "process_name": process.name
            }
            recent_alerts.append(alert)
    
    return {"status": "processed", "events_stored": len(recent_events)}

@app.get("/api/v1/commands")
async def get_commands(host: str = Query(..., description="Hostname to get commands for")):
    """
    Command polling endpoint for agents.
    Returns pending commands for the specified host.
    """
    if host in pending_commands and pending_commands[host]:
        commands_to_send = pending_commands[host].copy()
        pending_commands[host] = []  # Clear commands after sending
        return commands_to_send
    
    return []

@app.get("/api/v1/dashboard/stats")
async def get_dashboard_stats():
    """
    Dashboard statistics endpoint.
    Returns basic counts and metrics for the UI.
    """
    # Calculate unique hosts
    unique_hosts = set()
    for event in recent_events:
        if "hostname" in event:
            unique_hosts.add(event["hostname"])
    
    # Calculate alert severity breakdown
    alert_severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for alert in recent_alerts:
        severity = alert.get("severity", "LOW")
        alert_severity_counts[severity] = alert_severity_counts.get(severity, 0) + 1
    
    return {
        "event_count": len(recent_events),
        "alert_count": len(recent_alerts),
        "unique_hosts": len(unique_hosts),
        "pending_command_hosts": len([h for h, cmds in pending_commands.items() if cmds]),
        "alert_severity_breakdown": alert_severity_counts
    }

@app.get("/api/v1/alerts")
async def get_alerts():
    """
    Alerts endpoint for the UI.
    Returns recent alerts in reverse chronological order.
    """
    alerts_list = list(recent_alerts)
    alerts_list.reverse()  # Most recent first
    return alerts_list

@app.get("/api/v1/events")
async def get_events(limit: int = Query(50, description="Number of recent events to return")):
    """
    Events endpoint for debugging/monitoring.
    Returns recent events.
    """
    events_list = list(recent_events)
    events_list.reverse()  # Most recent first
    return events_list[:limit]

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic info."""
    return {
        "name": "AI-Eye Watcher Central Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "dashboard_stats": "/api/v1/dashboard/stats",
            "alerts": "/api/v1/alerts",
            "events": "/api/v1/events",
            "commands": "/api/v1/commands",
            "health": "/health",
            "docs": "/docs"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)