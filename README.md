# AI-Eye Watcher - Native Development Environment

A lightweight, native security monitoring system for macOS that provides real-time threat detection and automated response capabilities.

## 🚀 Quick Start

### Prerequisites
- **macOS** (tested on macOS 14+)
- **Python 3.9+** with pip
- **Node.js 18+** with npm
- **Git**

### One-Command Setup & Launch

```bash
# Clone and start everything
git clone https://github.com/ankitk090-lang/AI_Eye_watcher.git
cd AI_Eye_watcher
./start-dev.sh
```

That's it! The script will:
- ✅ Start the Backend Server (Python/FastAPI)
- ✅ Start the Frontend UI (React/Vite)
- ✅ Start the AI Agent (Python monitoring)

### Access the Application

- **🌐 Web UI**: http://localhost:5173
- **🔧 Backend API**: http://localhost:9000
- **📊 API Docs**: http://localhost:9000/docs

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │  Backend Server │    │   AI Agent      │
│   (React/Vite)  │◄──►│  (FastAPI)      │◄──►│   (Python)      │
│   Port: 5173    │    │   Port: 9000    │    │   Native macOS  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
   Dashboard &              Event Storage           System Monitor
   Alert Views             Threat Analysis         Process Control
```

## 🎯 Features

### ✅ **Real-Time Monitoring**
- Process monitoring (247+ processes tracked)
- Network connection analysis
- System resource monitoring
- 15-second telemetry collection

### ✅ **Threat Detection**
- Known bad process detection
- Anomaly detection for new processes
- Automated threat intelligence matching
- Real-time alert generation

### ✅ **Automated Response**
- Process termination commands
- Graceful SIGTERM → SIGKILL escalation
- Command execution logging
- 60-second command polling

### ✅ **Modern Web Interface**
- Live dashboard with real-time stats
- Comprehensive alerts table
- Material-UI design system
- Responsive mobile-friendly layout

## 📁 Project Structure

```
aAI_Eye_watcher/
├── 🚀 start-dev.sh              # One-command launcher
├── 🛑 stop-dev.sh               # Stop all services
├── 📖 README.md                 # This file
│
├── 🖥️  ai-eye-watcher-backend/   # Python Backend
│   ├── central_server.py        # FastAPI server
│   ├── agent.py                 # Native monitoring agent
│   ├── test_agent.py            # Comprehensive test suite
│   ├── requirements.txt         # Backend dependencies
│   ├── agent_requirements.txt   # Agent dependencies
│   └── AGENT_README.md          # Detailed agent docs
│
└── 🎨 ai-eye-watcher-ui/        # React Frontend
    ├── src/
    │   ├── pages/
    │   │   ├── DashboardPage.jsx # Live stats dashboard
    │   │   └── AlertsPage.jsx    # Threat alerts table
    │   ├── components/
    │   │   ├── Layout.jsx        # App layout & navigation
    │   │   └── StatCard.jsx      # Dashboard stat cards
    │   └── App.jsx               # Main app & routing
    └── package.json              # Frontend dependencies
```

## 🔧 Manual Setup (Alternative)

If you prefer to set up components individually:

### Backend Setup
```bash
cd ai-eye-watcher-backend

# Setup server environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup agent environment
python3 -m venv agent_venv
source agent_venv/bin/activate
pip install -r agent_requirements.txt
```

### Frontend Setup
```bash
cd ai-eye-watcher-ui
npm install
```

### Manual Launch
```bash
# Terminal 1: Backend Server
cd ai-eye-watcher-backend
source venv/bin/activate
python3 central_server.py

# Terminal 2: Frontend UI
cd ai-eye-watcher-ui
npm run dev

# Terminal 3: AI Agent
cd ai-eye-watcher-backend
source agent_venv/bin/activate
python3 agent.py  # or sudo python3 agent.py for full capabilities
```

## 🧪 Testing

### Test the Agent
```bash
cd ai-eye-watcher-backend
source agent_venv/bin/activate
python3 test_agent.py
```

### Test Threat Detection
```bash
# Create a test malicious process
cp /bin/sleep /tmp/evil.sh
/tmp/evil.sh 3000 &

# Watch the logs - the process should be detected and killed within 60 seconds
tail -f agent.log
```

### API Testing
```bash
# Check dashboard stats
curl http://localhost:9000/api/v1/dashboard/stats

# Check alerts
curl http://localhost:9000/api/v1/alerts

# Check system health
curl http://localhost:9000/health
```

## 📊 Dashboard Features

### Live Statistics
- **Connected Hosts**: Number of monitored systems
- **Active Alerts**: Current threat count with severity breakdown
- **Total Events**: Real-time event collection counter
- **Pending Commands**: Automated response queue

### Alerts Management
- **Real-time Updates**: 30-second refresh cycle
- **Severity Filtering**: HIGH/MEDIUM/LOW classification
- **Process Details**: PID, name, and command line info
- **Timestamp Tracking**: Precise alert timing

## 🛡️ Security Considerations

### Permissions
- **Basic Operation**: Standard user permissions sufficient
- **Process Killing**: Requires `sudo` for cross-user process termination
- **Network Monitoring**: Some data requires elevated privileges

### Network Security
- **Local Only**: All communication on localhost
- **No Authentication**: Development environment only
- **HTTP Protocol**: Consider HTTPS for production

## 🔍 Troubleshooting

### Common Issues

**"Connection refused" errors:**
```bash
# Check if backend is running
curl http://localhost:9000/health

# Restart backend
./stop-dev.sh && ./start-dev.sh
```

**Agent permission errors:**
```bash
# Run agent with elevated privileges
sudo python3 agent.py
```

**Frontend not loading:**
```bash
# Check if frontend is running
curl http://localhost:5173

# Reinstall dependencies
cd ai-eye-watcher-ui && npm install
```

### Log Files
```bash
# View real-time logs
tail -f backend.log    # Backend server logs
tail -f frontend.log   # Frontend build logs
tail -f agent.log      # Agent monitoring logs
```

### Process Management
```bash
# Check running processes
ps aux | grep -E "(central_server|agent\.py|npm run dev)"

# Manual cleanup
pkill -f "python3 central_server.py"
pkill -f "python3 agent.py"
pkill -f "npm run dev"
```

## 🚦 System Status

The system provides real-time status indicators:

- **🟢 Online**: All services running normally
- **🟡 Warning**: Some services degraded
- **🔴 Offline**: Critical services down

## 📈 Performance

### Resource Usage
- **Backend**: ~50MB RAM, minimal CPU
- **Frontend**: ~100MB RAM during development
- **Agent**: ~30MB RAM, periodic CPU spikes during collection

### Data Collection
- **Frequency**: Every 15 seconds
- **Process Count**: 200-300 processes typical
- **Network Connections**: ESTABLISHED only
- **Storage**: In-memory (1000 events, 100 alerts)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test your changes with `python3 test_agent.py`
4. Submit a pull request

## 📄 License

This project is part of the AI-Eye Watcher security monitoring system.

---

**🎉 Happy Monitoring!** 

For questions or issues, check the logs first, then create an issue with the relevant log output.
