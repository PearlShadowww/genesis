# Genesis Backend

Rust Actix-web API server for the Genesis AI-powered software generator.

## Features
- REST API endpoints for project generation
- Health check and monitoring
- Project history management
- Integration with Python AI core
- CORS support for frontend communication
- Async project generation with status tracking

## API Endpoints

### Health Check
- `GET /health` - Returns backend and AI core health status

### Project Generation
- `POST /generate` - Start a new project generation
  - Body: `{ "prompt": "string", "backend": "string" }`
  - Returns: Project ID for tracking

### Project Management
- `GET /projects` - List all generated projects
- `GET /projects/{id}` - Get specific project details

## Setup
```bash
cd backend
cargo build
cargo run
```

## Configuration
Edit `config.toml` to modify server settings, AI core URL, and CORS policies.

## Testing
```bash
cargo test
```

## Dependencies
- actix-web: Web framework
- serde: Serialization
- reqwest: HTTP client
- tokio: Async runtime
- chrono: DateTime handling
- uuid: Unique ID generation 