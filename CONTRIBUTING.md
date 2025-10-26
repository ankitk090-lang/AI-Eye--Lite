# Contributing to AI-Eye Watcher

Thank you for your interest in contributing to AI-Eye Watcher! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-eye-watcher.git
   cd ai-eye-watcher
   ```
3. **Set up the development environment**:
   ```bash
   ./start-dev.sh
   ```

## 🛠️ Development Setup

### Prerequisites
- **macOS** (primary target platform)
- **Python 3.9+** with pip
- **Node.js 18+** with npm
- **Git**

### Quick Setup
```bash
# Start all services
./start-dev.sh

# Run tests
cd ai-eye-watcher-backend
source agent_venv/bin/activate
python3 test_agent.py

# Stop all services
./stop-dev.sh
```

## 📝 Making Changes

### Code Style
- **Python**: Follow PEP 8 guidelines
- **JavaScript/React**: Use ESLint configuration provided
- **Comments**: Write clear, concise comments for complex logic
- **Logging**: Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)

### Testing
- **Backend**: Run `python3 test_agent.py` before submitting
- **Frontend**: Ensure UI loads and displays live data
- **Integration**: Test the complete system with `./start-dev.sh`

### Commit Messages
Use clear, descriptive commit messages:
```
feat: add real-time alert filtering
fix: resolve CORS issue with frontend API calls
docs: update installation instructions
test: add unit tests for threat detection
```

## 🐛 Bug Reports

When reporting bugs, please include:
- **OS version** (macOS version)
- **Python version** (`python3 --version`)
- **Node.js version** (`node --version`)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Log files** (agent.log, backend.log, frontend.log)

## 💡 Feature Requests

For new features:
- **Describe the use case** and problem it solves
- **Provide examples** of how it would work
- **Consider security implications** for monitoring software
- **Check existing issues** to avoid duplicates

## 🔒 Security Considerations

This is security monitoring software, so:
- **Never commit** real system data or logs
- **Sanitize examples** of hostnames, usernames, process names
- **Test security features** thoroughly
- **Report security issues** privately via GitHub Security tab

## 📋 Pull Request Process

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Test thoroughly**:
   ```bash
   # Test backend
   cd ai-eye-watcher-backend
   python3 test_agent.py
   
   # Test full system
   ./start-dev.sh
   # Verify UI works at http://localhost:5173
   ./stop-dev.sh
   ```

4. **Update documentation** if needed

5. **Submit pull request** with:
   - Clear description of changes
   - Screenshots for UI changes
   - Test results
   - Any breaking changes noted

## 🏗️ Project Structure

```
ai-eye-watcher/
├── 🖥️  ai-eye-watcher-backend/   # Python FastAPI backend
│   ├── central_server.py        # Main API server
│   ├── agent.py                 # System monitoring agent
│   └── test_agent.py            # Test suite
├── 🎨 ai-eye-watcher-ui/        # React frontend
│   ├── src/pages/               # UI pages
│   └── src/components/          # Reusable components
├── 🚀 start-dev.sh              # Development launcher
└── 📖 README.md                 # Main documentation
```

## 🎯 Areas for Contribution

### High Priority
- **Cross-platform support** (Linux, Windows)
- **Additional threat detection** rules
- **Performance optimizations** for large-scale monitoring
- **Enhanced UI features** (charts, filtering, search)

### Medium Priority
- **Configuration management** (YAML/JSON config files)
- **Database persistence** (SQLite, PostgreSQL)
- **Authentication & authorization**
- **API rate limiting**

### Documentation
- **Video tutorials** for setup and usage
- **Architecture diagrams**
- **Deployment guides** for production
- **API documentation** improvements

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check README.md and AGENT_README.md first

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy Contributing!** 🎉