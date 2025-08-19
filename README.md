# 📚 Tiny HTTP Server - Educational Project

> **🎯 Learning Focus**: This is a strictly educational project designed to understand HTTP protocols, socket programming, and web server fundamentals from first principles.

## 📖 Overview

A minimal HTTP server implementation in Python that demonstrates core web server concepts without external frameworks. Built entirely with Python's standard library to showcase low-level network programming and HTTP protocol handling.

**🚨 Important**: This is for learning purposes only

## 🎓 Educational Features

### 📝 Extensive Documentation
- **Detailed docstrings** in every function explaining line-by-line logic
- **Inline comments** breaking down complex operations
- **Step-by-step explanations** for socket operations and HTTP parsing
- **[NOTEBOOK.md](NOTEBOOK.md)** - Comprehensive teaching reference covering:
  - HTTP content types and response structures
  - Request parsing and routing concepts
  - Python context managers (beginner-friendly)
  - Line-by-line server loop analysis
  - Network programming gotchas and best practices

### 🔍 Learning-Oriented Code Structure
- Clear separation of concerns (response building, request handling, socket management)
- Extensive error handling with educational comments
- Timeout management and connection lifecycle examples
- Platform compatibility handling (Windows/Linux socket options)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Basic understanding of HTTP concepts (helpful but not required)

### Running the Server

```bash
# Clone and navigate to project
git clone <your-repo-url>
cd tiny_HTTP_server

# Install dependencies (minimal)
pip install -r requirements.txt

# Run the server
python server.py
```

Visit: `http://localhost:5073`

### Docker Deployment

```bash
# Build image
docker build -t tiny-http-server .

# Run container
docker run -p 5073:5073 tiny-http-server
```

## 🏗️ Project Structure

```
tiny_HTTP_server/
├── server.py          # Main server implementation with extensive docs
├── index.html         # Landing page (Tailwind CSS from CDN)
├── tests/             # Test framework setup
│   └── test_api.py
├── NOTEBOOK.md        # 📚 Comprehensive learning reference
├── TODO.md            # Development checklist (learning milestones)
├── Dockerfile         # Container deployment
└── requirements.txt   # Minimal dependencies
```

## 🎯 What I learned from this experience

### 1. **HTTP Protocol Fundamentals**
- Request/response cycle
- Headers, status codes, content types
- HTTP methods and routing

### 2. **Socket Programming**
- TCP socket creation and binding
- Connection acceptance and management
- Blocking vs non-blocking I/O
- Connection timeouts and error handling

### 3. **Python Network Programming**
- Context managers for resource cleanup
- Bytes vs strings in network programming
- Error handling in network applications
- Platform-specific socket options

### 4. **Web Server Architecture**
- Single-threaded vs multi-threaded servers
- Request parsing and validation
- Static file serving concepts
- Security considerations (basic)

## 📋 Supported Features

✅ **HTTP GET requests**
✅ **Static HTML serving**
✅ **JSON API endpoint** (`/api/hello`)
✅ **Error handling** (400, 404, 405 responses)
✅ **Connection timeouts**
✅ **Graceful connection cleanup**
✅ **Docker deployment**
✅ **Responsive HTML** (Tailwind CSS)

## 🚧 Educational Limitations

This server intentionally omits production features to focus on core concepts:

- ❌ No HTTPS/TLS support
- ❌ No request body parsing (POST data)
- ❌ No session management
- ❌ No authentication
- ❌ No concurrent connection handling
- ❌ No static file serving middleware
- ❌ No request logging
- ❌ No configuration management

## 📚 Learning Resources

### Primary Documentation
- **[NOTEBOOK.md](NOTEBOOK.md)** - Main reference
- **[TODO.md](TODO.md)** - Development checklist
- **Inline code comments** - Step-by-step explanations

### Key Learning Sections
1. **HTTP Content Types Reference** - Understanding MIME types
2. **Request Handling Deep Dive** - Parsing and routing
3. **Python Context Managers** - Resource management patterns
4. **Server Accept Loop** - Connection lifecycle management

## 🛠️ Development Setup

```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run with detailed output
python server.py
```

## 🧪 Testing

```bash
# Basic functionality test
curl http://localhost:5073/

# API endpoint test
curl http://localhost:5073/api/hello

# Test with verbose output
curl -v http://localhost:5073/
```

## 📄 License

[MIT License](LICENSE) - Free for educational use

---