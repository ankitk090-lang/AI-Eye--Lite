#!/usr/bin/env python3
"""
AI-Eye Watcher Native Agent for macOS
Collects system telemetry and executes commands from the Central Server.
"""

import os
import signal
import time
import datetime
import logging
from typing import List, Dict, Any, Optional

import psutil
import requests
import schedule

# Configuration
CENTRAL_SERVER_URL = "http://localhost:9000"
AGENT_HOSTNAME = os.uname().nodename
COLLECTION_INTERVAL = 15  # seconds
COMMAND_POLL_INTERVAL = 60  # seconds

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('agent.log')
    ]
)
logger = logging.getLogger(__name__)


def collect_system_data() -> Dict[str, Any]:
    """
    Collect process and network connection data using psutil.
    Returns data in the format expected by the Central Server.
    """
    try:
        # Collect process information
        processes = []
        for proc in psutil.process_iter(['pid', 'ppid', 'name', 'username', 'cmdline']):
            try:
                proc_info = proc.info
                # Get additional metrics
                cpu_percent = proc.cpu_percent()
                memory_percent = proc.memory_percent()
                
                process_data = {
                    "pid": proc_info['pid'],
                    "name": proc_info['name'] or "unknown",
                    "command_line": ' '.join(proc_info['cmdline']) if proc_info['cmdline'] else None,
                    "user": proc_info['username'],
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory_percent
                }
                processes.append(process_data)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Process disappeared or access denied, skip it
                continue
        
        # Collect network connections (only ESTABLISHED ones)
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == psutil.CONN_ESTABLISHED:
                    connection_data = {
                        "local_address": conn.laddr.ip if conn.laddr else "unknown",
                        "local_port": conn.laddr.port if conn.laddr else 0,
                        "remote_address": conn.raddr.ip if conn.raddr else None,
                        "remote_port": conn.raddr.port if conn.raddr else None,
                        "status": conn.status,
                        "pid": conn.pid
                    }
                    connections.append(connection_data)
        except psutil.AccessDenied:
            logger.warning("Access denied when collecting network connections")
        
        # Collect basic system info
        system_info = {
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "boot_time": psutil.boot_time(),
            "platform": os.uname().sysname
        }
        
        return {
            "hostname": AGENT_HOSTNAME,
            "timestamp": datetime.datetime.now().isoformat(),
            "processes": processes,
            "connections": connections,
            "system_info": system_info
        }
    
    except Exception as e:
        logger.error(f"Error collecting system data: {e}")
        return {
            "hostname": AGENT_HOSTNAME,
            "timestamp": datetime.datetime.now().isoformat(),
            "processes": [],
            "connections": [],
            "system_info": {}
        }


def collect_and_send():
    """
    Collect system telemetry and send it to the Central Server.
    """
    try:
        logger.info("Collecting system telemetry...")
        data = collect_system_data()
        
        # Send data to Central Server
        response = requests.post(
            f"{CENTRAL_SERVER_URL}/api/v1/collect",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Telemetry sent successfully. Server response: {result}")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send telemetry to Central Server: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during telemetry collection: {e}")


def execute_kill_process(pid_str: str) -> bool:
    """
    Execute kill process command for the given PID.
    
    Args:
        pid_str: Process ID as string
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        pid = int(pid_str)
        logger.info(f"Attempting to kill process PID {pid}")
        
        # Check if process exists first
        if not psutil.pid_exists(pid):
            logger.warning(f"Process PID {pid} does not exist")
            return False
        
        # Try to get process info for logging
        try:
            proc = psutil.Process(pid)
            proc_name = proc.name()
            logger.info(f"Killing process: {proc_name} (PID: {pid})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            proc_name = "unknown"
        
        # Send SIGTERM first (graceful termination)
        os.kill(pid, signal.SIGTERM)
        
        # Wait a bit to see if process terminates gracefully
        time.sleep(2)
        
        # Check if process is still running
        if psutil.pid_exists(pid):
            logger.warning(f"Process {pid} still running after SIGTERM, sending SIGKILL")
            os.kill(pid, signal.SIGKILL)
        
        logger.info(f"Successfully killed process {proc_name} (PID: {pid})")
        return True
        
    except ValueError:
        logger.error(f"Invalid PID format: {pid_str}")
        return False
    except ProcessLookupError:
        logger.warning(f"Process PID {pid_str} already terminated")
        return True  # Consider this success since the process is gone
    except PermissionError:
        logger.error(f"Permission denied when trying to kill PID {pid_str}. Try running with sudo.")
        return False
    except Exception as e:
        logger.error(f"Unexpected error killing process PID {pid_str}: {e}")
        return False


def poll_and_execute_commands():
    """
    Poll the Central Server for pending commands and execute them.
    """
    try:
        logger.info("Polling for commands...")
        
        # Get commands from Central Server
        response = requests.get(
            f"{CENTRAL_SERVER_URL}/api/v1/commands",
            params={"host": AGENT_HOSTNAME},
            timeout=10
        )
        response.raise_for_status()
        
        commands = response.json()
        
        if not commands:
            logger.debug("No pending commands")
            return
        
        logger.info(f"Received {len(commands)} command(s)")
        
        # Execute each command
        for command in commands:
            command_id = command.get("command_id", "unknown")
            action = command.get("action")
            target = command.get("target")
            parameters = command.get("parameters", {})
            
            logger.info(f"Executing command {command_id}: {action} on {target}")
            
            if action == "kill_process":
                success = execute_kill_process(target)
                if success:
                    logger.info(f"Command {command_id} executed successfully")
                else:
                    logger.error(f"Command {command_id} failed to execute")
            else:
                logger.warning(f"Unknown command action: {action}")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to poll commands from Central Server: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during command polling: {e}")


def main():
    """
    Main agent loop with scheduled tasks.
    """
    logger.info(f"AI-Eye Watcher Agent starting on {AGENT_HOSTNAME}")
    logger.info(f"Central Server URL: {CENTRAL_SERVER_URL}")
    logger.info(f"Collection interval: {COLLECTION_INTERVAL}s")
    logger.info(f"Command poll interval: {COMMAND_POLL_INTERVAL}s")
    
    # Schedule periodic tasks
    schedule.every(COLLECTION_INTERVAL).seconds.do(collect_and_send)
    schedule.every(COMMAND_POLL_INTERVAL).seconds.do(poll_and_execute_commands)
    
    # Run initial collection immediately
    logger.info("Running initial telemetry collection...")
    collect_and_send()
    
    # Main loop
    logger.info("Agent started successfully. Press Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Agent stopped by user")
    except Exception as e:
        logger.error(f"Agent crashed: {e}")
        raise


if __name__ == "__main__":
    main()