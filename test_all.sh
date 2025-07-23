#!/bin/bash

# Genesis Comprehensive Test Script
# Tests all components of the Genesis system

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
PASSED=0
TOTAL=0

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((PASSED++))
    ((TOTAL++))
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
    ((TOTAL++))
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Test functions
test_prerequisites() {
    log_info "Testing prerequisites..."
    
    # Test Node.js
    if command -v node &> /dev/null; then
        VERSION=$(node --version)
        log_success "Node.js found: $VERSION"
    else
        log_error "Node.js not found"
    fi
    
    # Test Rust
    if command -v cargo &> /dev/null; then
        VERSION=$(cargo --version)
        log_success "Rust found: $VERSION"
    else
        log_error "Rust not found"
    fi
    
    # Test Python
    if command -v python3 &> /dev/null; then
        VERSION=$(python3 --version)
        log_success "Python found: $VERSION"
    elif command -v python &> /dev/null; then
        VERSION=$(python --version)
        log_success "Python found: $VERSION"
    else
        log_error "Python not found"
    fi
    
    # Test Git
    if command -v git &> /dev/null; then
        VERSION=$(git --version)
        log_success "Git found: $VERSION"
    else
        log_error "Git not found"
    fi
}

test_ollama() {
    log_info "Testing Ollama..."
    
    if command -v ollama &> /dev/null; then
        log_success "Ollama found"
        
        # Test if Ollama is running
        if curl -s http://localhost:11434/api/tags &> /dev/null; then
            log_success "Ollama is running"
            
            # Check for required models
            MODELS=$(curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null || echo "")
            if echo "$MODELS" | grep -q "qwen2.5-coder"; then
                log_success "Required model qwen2.5-coder found"
            else
                log_warning "Required model qwen2.5-coder not found"
            fi
        else
            log_warning "Ollama is not running (start with: ollama serve)"
        fi
    else
        log_error "Ollama not found"
    fi
}

test_python_dependencies() {
    log_info "Testing Python dependencies..."
    
    cd ai_core
    
    # Test if virtual environment exists
    if [ -d "venv" ]; then
        log_success "Python virtual environment found"
    else
        log_warning "Python virtual environment not found"
    fi
    
    # Test required packages
    REQUIRED_PACKAGES=("fastapi" "pydantic" "crewai" "uvicorn" "requests")
    
    for package in "${REQUIRED_PACKAGES[@]}"; do
        if python -c "import $package" 2>/dev/null; then
            log_success "Package $package found"
        else
            log_error "Package $package not found"
        fi
    done
    
    cd ..
}

test_rust_backend() {
    log_info "Testing Rust backend..."
    
    cd backend
    
    # Test if Cargo.toml exists
    if [ -f "Cargo.toml" ]; then
        log_success "Cargo.toml found"
    else
        log_error "Cargo.toml not found"
    fi
    
    # Test if main.rs exists
    if [ -f "src/main.rs" ]; then
        log_success "main.rs found"
    else
        log_error "main.rs not found"
    fi
    
    # Test compilation
    if cargo check --quiet; then
        log_success "Rust code compiles successfully"
    else
        log_error "Rust code compilation failed"
    fi
    
    cd ..
}

test_tree_sitter() {
    log_info "Testing Tree-Sitter..."
    
    cd tree_sitter
    
    # Test if package.json exists
    if [ -f "package.json" ]; then
        log_success "package.json found"
    else
        log_error "package.json not found"
    fi
    
    # Test if validate.js exists
    if [ -f "validate.js" ]; then
        log_success "validate.js found"
    else
        log_error "validate.js not found"
    fi
    
    # Test if node_modules exists
    if [ -d "node_modules" ]; then
        log_success "Node.js dependencies installed"
    else
        log_warning "Node.js dependencies not installed (run: npm install)"
    fi
    
    cd ..
}

test_frontend() {
    log_info "Testing Tauri frontend..."
    
    cd genesis-frontend
    
    # Test if package.json exists
    if [ -f "package.json" ]; then
        log_success "package.json found"
    else
        log_error "package.json not found"
    fi
    
    # Test if main App.tsx exists
    if [ -f "src/App.tsx" ]; then
        log_success "App.tsx found"
    else
        log_error "App.tsx not found"
    fi
    
    # Test if node_modules exists
    if [ -d "node_modules" ]; then
        log_success "Node.js dependencies installed"
    else
        log_warning "Node.js dependencies not installed (run: npm install)"
    fi
    
    cd ..
}

test_services() {
    log_info "Testing service connectivity..."
    
    # Test AI Core
    if curl -s http://127.0.0.1:8000/health &> /dev/null; then
        log_success "AI Core service is running"
    else
        log_warning "AI Core service is not running"
    fi
    
    # Test Rust Backend
    if curl -s http://127.0.0.1:8080/health &> /dev/null; then
        log_success "Rust Backend service is running"
    else
        log_warning "Rust Backend service is not running"
    fi
}

test_integration() {
    log_info "Testing integration..."
    
    # Test if all required files exist
    REQUIRED_FILES=(
        "README.md"
        ".gitignore"
        "ai_core/main.py"
        "backend/src/main.rs"
        "tree_sitter/validate.js"
        "genesis-frontend/src/App.tsx"
    )
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [ -f "$file" ]; then
            log_success "File $file found"
        else
            log_error "File $file not found"
        fi
    done
}

show_setup_instructions() {
    echo -e "\n${BLUE}�� Setup Instructions:${NC}"
    echo "=================================================="
    echo -e "${YELLOW}1. Install Prerequisites:${NC}"
    echo "   - Node.js: https://nodejs.org/"
    echo "   - Rust: https://rustup.rs/"
    echo "   - Python: https://python.org/"
    echo "   - Git: https://git-scm.com/"
    echo "   - Ollama: https://ollama.ai/"
    echo ""
    echo -e "${YELLOW}2. Install Dependencies:${NC}"
    echo "   cd ai_core && pip install -r requirements.txt"
    echo "   cd backend && cargo build"
    echo "   cd tree_sitter && npm install"
    echo "   cd genesis-frontend && npm install"
    echo ""
    echo -e "${YELLOW}3. Start Services:${NC}"
    echo "   ollama serve"
    echo "   cd ai_core && python start_ai_core.py"
    echo "   cd backend && cargo run"
    echo "   cd genesis-frontend && npm run tauri dev"
    echo ""
    echo -e "${YELLOW}4. Run Tests:${NC}"
    echo "   python ai_core/test_ollama.py"
    echo "   python ai_core/test_api.py"
    echo "   ./test_all.sh"
}

# Main test execution
main() {
    echo -e "${BLUE}🧪 Genesis Comprehensive Test Suite${NC}"
    echo "=================================================="
    
    test_prerequisites
    test_ollama
    test_python_dependencies
    test_rust_backend
    test_tree_sitter
    test_frontend
    test_services
    test_integration
    
    echo -e "\n${BLUE}📊 Test Results:${NC}"
    echo "=================================================="
    echo -e "Passed: ${GREEN}$PASSED${NC}/${TOTAL}"
    echo -e "Success Rate: ${GREEN}$((PASSED * 100 / TOTAL))%${NC}"
    
    if [ $PASSED -eq $TOTAL ]; then
        echo -e "\n${GREEN}🎉 All tests passed! Genesis is ready to use.${NC}"
        exit 0
    else
        echo -e "\n${YELLOW}⚠️  Some tests failed. See setup instructions below.${NC}"
        show_setup_instructions
        exit 1
    fi
}

# Run main function
main "$@"