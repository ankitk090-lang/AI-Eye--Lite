#!/bin/bash

# AI-Eye Watcher Development Environment Launcher
# This script starts the Backend Server, Frontend UI, and Agent in the background

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$SCRIPT_DIR"

# Log files
BACKEND_LOG="$BASE_DIR/backend.log"
FRONTEND_LOG="$BASE_DIR/frontend.log"
AGENT_LOG="$BASE_DIR/agent.log"

# PID files for tracking processes
BACKEND_PID_FILE="$BASE_DIR/.backend.pid"
FRONTEND_PID_FILE="$BASE_DIR/.frontend.pid"
AGENT_PID_FILE="$BASE_DIR/.agent.pid"

echo -e "${BLUE}🚀 AI-Eye Watcher Development Environment${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# Function to check if a process is running
check_process() {
    local pid_file=$1
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0  # Process is running
        else
            rm -f "$pid_file"  # Clean up stale PID file
            return 1  # Process is not running
        fi
    fi
    return 1  # PID file doesn't exist
}

# Function to start backend
start_backend() {
    echo -e "${YELLOW}📡 Starting Backend Server...${NC}"
    
    cd "$BASE_DIR/ai-eye-watcher-backend" || {
        echo -e "${RED}❌ Backend directory not found!${NC}"
        return 1
    }
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo -e "${RED}❌ Backend virtual environment not found! Run setup first.${NC}"
        return 1
    fi
    
    # Activate virtual environment and start server
    source venv/bin/activate
    python3 central_server.py > "$BACKEND_LOG" 2>&1 &
    local backend_pid=$!
    echo "$backend_pid" > "$BACKEND_PID_FILE"
    
    echo -e "${GREEN}✅ Backend Server started (PID: $backend_pid)${NC}"
    echo -e "   📋 Logs: tail -f $BACKEND_LOG"
    
    cd "$BASE_DIR"
}

# Function to start frontend
start_frontend() {
    echo -e "${YELLOW}🎨 Starting Frontend UI...${NC}"
    
    cd "$BASE_DIR/ai-eye-watcher-ui" || {
        echo -e "${RED}❌ Frontend directory not found!${NC}"
        return 1
    }
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
        npm install
    fi
    
    # Start frontend development server
    npm run dev > "$FRONTEND_LOG" 2>&1 &
    local frontend_pid=$!
    echo "$frontend_pid" > "$FRONTEND_PID_FILE"
    
    echo -e "${GREEN}✅ Frontend UI started (PID: $frontend_pid)${NC}"
    echo -e "   📋 Logs: tail -f $FRONTEND_LOG"
    
    cd "$BASE_DIR"
}

# Function to start agent
start_agent() {
    echo -e "${YELLOW}🤖 Starting AI Agent...${NC}"
    
    cd "$BASE_DIR/ai-eye-watcher-backend" || {
        echo -e "${RED}❌ Backend directory not found!${NC}"
        return 1
    }
    
    # Check if agent virtual environment exists
    if [ ! -d "agent_venv" ]; then
        echo -e "${RED}❌ Agent virtual environment not found! Run setup first.${NC}"
        return 1
    fi
    
    # Activate virtual environment and start agent
    source agent_venv/bin/activate
    python3 agent.py > "$AGENT_LOG" 2>&1 &
    local agent_pid=$!
    echo "$agent_pid" > "$AGENT_PID_FILE"
    
    echo -e "${GREEN}✅ AI Agent started (PID: $agent_pid)${NC}"
    echo -e "   📋 Logs: tail -f $AGENT_LOG"
    echo -e "${YELLOW}   ⚠️  Note: Agent may need sudo for full functionality${NC}"
    
    cd "$BASE_DIR"
}

# Check if any processes are already running
echo -e "${BLUE}🔍 Checking for existing processes...${NC}"

if check_process "$BACKEND_PID_FILE"; then
    echo -e "${YELLOW}⚠️  Backend Server is already running${NC}"
else
    start_backend
fi

if check_process "$FRONTEND_PID_FILE"; then
    echo -e "${YELLOW}⚠️  Frontend UI is already running${NC}"
else
    start_frontend
fi

if check_process "$AGENT_PID_FILE"; then
    echo -e "${YELLOW}⚠️  AI Agent is already running${NC}"
else
    start_agent
fi

echo ""
echo -e "${GREEN}🎉 AI-Eye Watcher Development Environment Started!${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""
echo -e "${GREEN}📱 Web UI:${NC}      http://localhost:5173"
echo -e "${GREEN}🔧 Backend API:${NC} http://localhost:9000"
echo ""
echo -e "${BLUE}📋 View Logs:${NC}"
echo -e "   Backend:  tail -f $BACKEND_LOG"
echo -e "   Frontend: tail -f $FRONTEND_LOG"
echo -e "   Agent:    tail -f $AGENT_LOG"
echo ""
echo -e "${BLUE}🛑 Stop Services:${NC}"
echo -e "   Run: ./stop-dev.sh"
echo -e "   Or:  pkill -f 'python3 central_server.py'"
echo -e "        pkill -f 'npm run dev'"
echo -e "        pkill -f 'python3 agent.py'"
echo ""
echo -e "${YELLOW}💡 Tip: Wait 10-15 seconds for all services to fully start${NC}"