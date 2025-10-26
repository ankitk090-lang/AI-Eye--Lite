#!/bin/bash

# AI-Eye Watcher Development Environment Stopper
# This script stops all AI-Eye Watcher services

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$SCRIPT_DIR"

# PID files for tracking processes
BACKEND_PID_FILE="$BASE_DIR/.backend.pid"
FRONTEND_PID_FILE="$BASE_DIR/.frontend.pid"
AGENT_PID_FILE="$BASE_DIR/.agent.pid"

echo -e "${BLUE}🛑 Stopping AI-Eye Watcher Development Environment${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""

# Function to stop a process by PID file
stop_process_by_pid() {
    local pid_file=$1
    local service_name=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            echo -e "${YELLOW}🔄 Stopping $service_name (PID: $pid)...${NC}"
            kill "$pid" 2>/dev/null
            
            # Wait up to 5 seconds for graceful shutdown
            local count=0
            while ps -p "$pid" > /dev/null 2>&1 && [ $count -lt 5 ]; do
                sleep 1
                count=$((count + 1))
            done
            
            # Force kill if still running
            if ps -p "$pid" > /dev/null 2>&1; then
                echo -e "${YELLOW}⚡ Force stopping $service_name...${NC}"
                kill -9 "$pid" 2>/dev/null
            fi
            
            echo -e "${GREEN}✅ $service_name stopped${NC}"
        else
            echo -e "${YELLOW}⚠️  $service_name was not running${NC}"
        fi
        rm -f "$pid_file"
    else
        echo -e "${YELLOW}⚠️  No PID file found for $service_name${NC}"
    fi
}

# Function to stop processes by pattern matching
stop_process_by_pattern() {
    local pattern=$1
    local service_name=$2
    
    local pids=$(pgrep -f "$pattern" 2>/dev/null)
    if [ -n "$pids" ]; then
        echo -e "${YELLOW}🔄 Stopping $service_name processes...${NC}"
        pkill -f "$pattern" 2>/dev/null
        sleep 2
        
        # Force kill if still running
        local remaining_pids=$(pgrep -f "$pattern" 2>/dev/null)
        if [ -n "$remaining_pids" ]; then
            echo -e "${YELLOW}⚡ Force stopping $service_name...${NC}"
            pkill -9 -f "$pattern" 2>/dev/null
        fi
        
        echo -e "${GREEN}✅ $service_name stopped${NC}"
    else
        echo -e "${YELLOW}⚠️  No $service_name processes found${NC}"
    fi
}

# Stop services using PID files first
stop_process_by_pid "$BACKEND_PID_FILE" "Backend Server"
stop_process_by_pid "$FRONTEND_PID_FILE" "Frontend UI"
stop_process_by_pid "$AGENT_PID_FILE" "AI Agent"

echo ""
echo -e "${BLUE}🔍 Checking for any remaining processes...${NC}"

# Fallback: stop by process pattern matching
stop_process_by_pattern "python3 central_server.py" "Backend Server"
stop_process_by_pattern "npm run dev" "Frontend UI"
stop_process_by_pattern "python3 agent.py" "AI Agent"

# Clean up log files (optional)
echo ""
read -p "$(echo -e ${YELLOW}🗑️  Delete log files? [y/N]: ${NC})" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f "$BASE_DIR/backend.log" "$BASE_DIR/frontend.log" "$BASE_DIR/agent.log"
    echo -e "${GREEN}✅ Log files deleted${NC}"
fi

echo ""
echo -e "${GREEN}🎉 AI-Eye Watcher Development Environment Stopped!${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${BLUE}💡 To start again, run: ./start-dev.sh${NC}"