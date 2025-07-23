# Genesis Technical Architecture

## 🏗️ System Architecture Overview

Genesis is a distributed, multi-service AI-powered software generator designed for scalability, reliability, and maintainability.

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Genesis System                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   Frontend      │    │    Backend      │    │    AI Core      │         │
│  │   (Tauri)       │◄──►│   (Rust)        │◄──►│   (Python)      │         │
│  │   Port 5173     │    │   Port 8080     │    │   Port 8000     │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│           │                       │                       │                 │
│           ▼                       ▼                       ▼                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   File System   │    │   Health        │    │   Ollama        │         │
│  │   Integration   │    │   Monitoring    │    │   Models        │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Service Details

### 1. **Frontend Service (Tauri + React)**

**Technology Stack:**
- **Framework**: Tauri (Rust + WebView)
- **UI**: React + TypeScript + Chakra UI
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **Build Tool**: Vite

**Key Features:**
- Desktop application with native performance
- Real-time project status updates
- File tree visualization
- Terminal output display
- Project history management

**Architecture:**
```typescript
// Core Components
├── App.tsx                 // Main application component
├── components/
│   ├── PromptInput.tsx     // Project description input
│   ├── FileTree.tsx        // Generated files display
│   ├── TerminalOutput.tsx  // Generation logs
│   └── ProjectHistory.tsx  // Past projects
└── services/
    └── api.ts             // Backend communication
```

**Communication:**
- HTTP requests to Backend API
- WebSocket for real-time updates (planned)
- File system access for project downloads

---

### 2. **Backend Service (Rust Actix-web)**

**Technology Stack:**
- **Framework**: Actix-web 4.4
- **Language**: Rust
- **Serialization**: Serde + Serde JSON
- **HTTP Client**: Reqwest
- **Async Runtime**: Tokio

**Key Features:**
- RESTful API endpoints
- Request validation and rate limiting
- Error handling with custom types
- Health monitoring
- Project state management

**API Endpoints:**
```rust
// Health & Status
GET  /health              // Service health check
GET  /status              // Detailed service status

// Project Generation
POST /generate            // Start project generation
GET  /projects/{id}       // Get project status
GET  /projects            // List all projects

// Error Handling
// All endpoints return structured error responses
```

**Architecture:**
```rust
src/
├── main.rs              // Application entry point
├── config.rs            // Configuration management
├── error.rs             // Custom error types
├── health.rs            // Health check endpoints
├── validation.rs        // Request validation
└── models.rs            // Data structures
```

**Error Handling:**
- Custom error types with HTTP status mapping
- Structured JSON error responses
- Comprehensive logging
- Graceful degradation

---

### 3. **AI Core Service (Python FastAPI)**

**Technology Stack:**
- **Framework**: FastAPI
- **AI Framework**: CrewAI
- **LLM Integration**: LangChain + Ollama
- **Validation**: Pydantic
- **Async**: asyncio

**Key Features:**
- Multi-agent AI workflow
- Code generation and validation
- Project planning and architecture
- Error analysis and debugging

**AI Workflow:**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Planner       │    │   Coder         │    │   Debugger      │
│   Agent         │───►│   Agent         │───►│   Agent         │
│                 │    │                 │    │                 │
│ • Project Plan  │    │ • Code Gen      │    │ • Code Review   │
│ • Architecture  │    │ • File Struct   │    │ • Bug Fixes     │
│ • Dependencies  │    │ • Impl Details  │    │ • Optimization  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Architecture:**
```python
ai_core/
├── main.py              # FastAPI application
├── llm.py               # LLM configuration
├── agents.py            # CrewAI agent definitions
├── tasks.py             # CrewAI task definitions
├── models.py            # Pydantic models
├── error_handling.py    # Custom exceptions
├── logging_config.py    # Logging setup
└── tools.py             # Custom tools
```

**Agent Roles:**
1. **Software Architect**: Creates project plans and architecture
2. **Senior Developer**: Generates production-ready code
3. **Code Quality Specialist**: Reviews and improves code

---

## 🔄 Data Flow

### **Project Generation Flow**

```
1. User Input
   └── Frontend (Tauri)
       └── HTTP POST /generate
           └── Backend (Rust)
               └── HTTP POST /run
                   └── AI Core (Python)
                       └── CrewAI Workflow
                           ├── Planner Agent
                           ├── Coder Agent
                           └── Debugger Agent
                               └── Ollama LLM
                                   └── Generated Files
                                       └── Backend
                                           └── Frontend Display
```

### **Error Handling Flow**

```
Error Occurs
    └── Service Layer
        └── Custom Error Type
            └── HTTP Status Mapping
                └── Structured JSON Response
                    └── Client Handling
                        └── User Feedback
```

---

## 🛡️ Security & Validation

### **Input Validation**
- **Frontend**: TypeScript type checking
- **Backend**: Rust validation with custom rules
- **AI Core**: Pydantic model validation

### **Rate Limiting**
- IP-based rate limiting
- Configurable time windows
- Graceful degradation

### **Error Handling**
- Comprehensive error types
- Structured error responses
- Detailed logging
- Graceful fallbacks

---

## 📊 Monitoring & Observability

### **Health Checks**
- Service-level health endpoints
- Dependency monitoring
- Resource usage tracking

### **Logging**
- Structured JSON logging
- Component-specific loggers
- Performance timing
- Error tracking

### **Metrics**
- Response times
- Error rates
- Resource utilization
- Service availability

---

## 🔧 Configuration Management

### **Environment-Based Configuration**
```bash
# Service URLs
AI_CORE_URL=http://127.0.0.1:8000
BACKEND_URL=http://127.0.0.1:8080
OLLAMA_URL=http://localhost:11434

# Service Ports
AI_CORE_PORT=8000
BACKEND_PORT=8080
FRONTEND_PORT=5173

# AI Configuration
OLLAMA_MODEL=qwen2.5-coder:1.5b-base
CREWAI_TEMPERATURE=0.1
```

### **Configuration Hierarchy**
1. Environment variables (highest priority)
2. Configuration files
3. Default values (lowest priority)

---

## 🚀 Performance Characteristics

### **Response Times**
- **Health Checks**: < 100ms
- **LLM Generation**: 2-5 seconds
- **Project Generation**: 30-60 seconds (estimated)
- **File Operations**: < 50ms

### **Resource Usage**
- **Frontend**: ~50MB RAM
- **Backend**: ~20MB RAM
- **AI Core**: ~100MB RAM
- **Ollama**: 2-4GB RAM (model dependent)

### **Scalability**
- **Horizontal**: Service replication
- **Vertical**: Resource scaling
- **Load Balancing**: Future implementation

---

## 🔄 Deployment Architecture

### **Development Environment**
```
Local Machine
├── Ollama (Local)
├── AI Core (Local)
├── Backend (Local)
└── Frontend (Local)
```

### **Production Environment** (Planned)
```
Load Balancer
├── Frontend Cluster
├── Backend Cluster
├── AI Core Cluster
└── Ollama Cluster
```

---

## 🛠️ Development Workflow

### **Local Development**
1. Start Ollama service
2. Start AI Core service
3. Start Backend service
4. Start Frontend service
5. Run integration tests

### **Testing Strategy**
- **Unit Tests**: Individual components
- **Integration Tests**: Service communication
- **End-to-End Tests**: Complete workflows
- **Performance Tests**: Load testing

---

## 🔮 Future Enhancements

### **Planned Features**
- WebSocket real-time updates
- Project templates
- Code validation with Tree-Sitter
- Multi-language support
- Cloud deployment
- User authentication

### **Scalability Improvements**
- Microservices architecture
- Message queues
- Caching layers
- Database integration
- Container orchestration

---

## 📚 Technology Decisions

### **Why These Technologies?**

**Frontend (Tauri):**
- ✅ Native performance
- ✅ Cross-platform compatibility
- ✅ Security benefits
- ✅ Small bundle size

**Backend (Rust):**
- ✅ High performance
- ✅ Memory safety
- ✅ Excellent error handling
- ✅ Strong type system

**AI Core (Python):**
- ✅ Rich AI ecosystem
- ✅ Rapid prototyping
- ✅ Excellent libraries
- ✅ Easy integration

**Ollama:**
- ✅ Local LLM deployment
- ✅ Privacy-focused
- ✅ Cost-effective
- ✅ Multiple model support

---

## 🎯 Architecture Principles

1. **Separation of Concerns**: Each service has a specific responsibility
2. **Loose Coupling**: Services communicate via well-defined APIs
3. **High Cohesion**: Related functionality is grouped together
4. **Fault Tolerance**: Graceful handling of failures
5. **Observability**: Comprehensive monitoring and logging
6. **Security**: Input validation and error handling
7. **Performance**: Optimized for speed and efficiency
8. **Maintainability**: Clean, documented, testable code 