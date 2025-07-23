# Genesis Validation Script for Windows
# This script checks all prerequisites and validates the Genesis setup

param(
    [switch]$Verbose,
    [switch]$SkipOllama
)

# Colors for output
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Blue = "Blue"

function Write-Status {
    param(
        [string]$Message,
        [string]$Status,
        [string]$Color = "White"
    )
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    $statusSymbol = switch ($Status) {
        "OK" { "✅" }
        "ERROR" { "❌" }
        "WARNING" { "⚠️" }
        "INFO" { "ℹ️" }
        default { "•" }
    }
    
    Write-Host "[$timestamp] $statusSymbol $Message" -ForegroundColor $Color
}

function Test-Command {
    param([string]$Command)
    
    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    }
    catch {
        return $false
    }
}

function Test-NodeJS {
    Write-Status "Checking Node.js installation..." "INFO" $Blue
    
    if (Test-Command "node") {
        $version = node --version
        Write-Status "Node.js found: $version" "OK" $Green
        return $true
    }
    else {
        Write-Status "Node.js not found. Install from https://nodejs.org/" "ERROR" $Red
        return $false
    }
}

function Test-Rust {
    Write-Status "Checking Rust installation..." "INFO" $Blue
    
    if (Test-Command "cargo") {
        $version = cargo --version
        Write-Status "Rust found: $version" "OK" $Green
        return $true
    }
    else {
        Write-Status "Rust not found. Install from https://rustup.rs/" "ERROR" $Red
        return $false
    }
}

function Test-Python {
    Write-Status "Checking Python installation..." "INFO" $Blue
    
    if (Test-Command "python") {
        $version = python --version
        Write-Status "Python found: $version" "OK" $Green
        return $true
    }
    elseif (Test-Command "python3") {
        $version = python3 --version
        Write-Status "Python found: $version" "OK" $Green
        return $true
    }
    else {
        Write-Status "Python not found. Install from https://python.org/" "ERROR" $Red
        return $false
    }
}

function Test-Git {
    Write-Status "Checking Git installation..." "INFO" $Blue
    
    if (Test-Command "git") {
        $version = git --version
        Write-Status "Git found: $version" "OK" $Green
        return $true
    }
    else {
        Write-Status "Git not found. Install from https://git-scm.com/" "ERROR" $Red
        return $false
    }
}

function Test-Ollama {
    if ($SkipOllama) {
        Write-Status "Skipping Ollama check (--SkipOllama specified)" "WARNING" $Yellow
        return $true
    }
    
    Write-Status "Checking Ollama installation..." "INFO" $Blue
    
    if (Test-Command "ollama") {
        try {
            $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 5
            $models = $response.models.Count
            Write-Status "Ollama running with $models models" "OK" $Green
            return $true
        }
        catch {
            Write-Status "Ollama not running. Start with: ollama serve" "WARNING" $Yellow
            return $false
        }
    }
    else {
        Write-Status "Ollama not found. Install from https://ollama.ai/" "ERROR" $Red
        return $false
    }
}

function Test-PythonPackages {
    Write-Status "Checking Python packages..." "INFO" $Blue
    
    $requiredPackages = @(
        "fastapi",
        "pydantic", 
        "crewai",
        "uvicorn",
        "requests"
    )
    
    $missingPackages = @()
    
    foreach ($package in $requiredPackages) {
        try {
            python -c "import $package" 2>$null
            Write-Status "  $package - OK" "OK" $Green
        }
        catch {
            Write-Status "  $package - Missing" "ERROR" $Red
            $missingPackages += $package
        }
    }
    
    if ($missingPackages.Count -gt 0) {
        Write-Status "Missing packages: $($missingPackages -join ', ')" "ERROR" $Red
        Write-Status "Install with: pip install -r ai_core/requirements.txt" "INFO" $Blue
        return $false
    }
    
    return $true
}

function Test-ProjectStructure {
    Write-Status "Checking project structure..." "INFO" $Blue
    
    $requiredDirs = @(
        "ai_core",
        "backend", 
        "tree_sitter",
        "genesis-frontend"
    )
    
    $requiredFiles = @(
        "ai_core/main.py",
        "ai_core/requirements.txt",
        "backend/Cargo.toml",
        "backend/src/main.rs",
        "tree_sitter/package.json",
        "tree_sitter/validate.js",
        "genesis-frontend/package.json"
    )
    
    $missingItems = @()
    
    foreach ($dir in $requiredDirs) {
        if (Test-Path $dir) {
            Write-Status "  Directory $dir - OK" "OK" $Green
        }
        else {
            Write-Status "  Directory $dir - Missing" "ERROR" $Red
            $missingItems += $dir
        }
    }
    
    foreach ($file in $requiredFiles) {
        if (Test-Path $file) {
            Write-Status "  File $file - OK" "OK" $Green
        }
        else {
            Write-Status "  File $file - Missing" "ERROR" $Red
            $missingItems += $file
        }
    }
    
    if ($missingItems.Count -gt 0) {
        Write-Status "Missing items: $($missingItems.Count)" "ERROR" $Red
        return $false
    }
    
    return $true
}

function Test-Services {
    Write-Status "Testing service connectivity..." "INFO" $Blue
    
    $services = @(
        @{Name="AI Core"; URL="http://127.0.0.1:8000/health"},
        @{Name="Rust Backend"; URL="http://127.0.0.1:8080/health"}
    )
    
    $runningServices = 0
    
    foreach ($service in $services) {
        try {
            $response = Invoke-RestMethod -Uri $service.URL -TimeoutSec 5
            Write-Status "  $($service.Name) - Running" "OK" $Green
            $runningServices++
        }
        catch {
            Write-Status "  $($service.Name) - Not running" "WARNING" $Yellow
        }
    }
    
    if ($runningServices -eq 0) {
        Write-Status "No services are running" "WARNING" $Yellow
        Write-Status "Start services with the provided startup scripts" "INFO" $Blue
        return $false
    }
    
    return $true
}

function Show-SetupInstructions {
    Write-Host "`n�� Setup Instructions:" -ForegroundColor $Blue
    Write-Host "=" * 50 -ForegroundColor $Blue
    
    Write-Host "1. Install Prerequisites:" -ForegroundColor $Yellow
    Write-Host "   - Node.js: https://nodejs.org/" -ForegroundColor $White
    Write-Host "   - Rust: https://rustup.rs/" -ForegroundColor $White
    Write-Host "   - Python: https://python.org/" -ForegroundColor $White
    Write-Host "   - Git: https://git-scm.com/" -ForegroundColor $White
    Write-Host "   - Ollama: https://ollama.ai/" -ForegroundColor $White
    
    Write-Host "`n2. Install Dependencies:" -ForegroundColor $Yellow
    Write-Host "   cd ai_core && pip install -r requirements.txt" -ForegroundColor $White
    Write-Host "   cd backend && cargo build" -ForegroundColor $White
    Write-Host "   cd tree_sitter && npm install" -ForegroundColor $White
    Write-Host "   cd genesis-frontend && npm install" -ForegroundColor $White
    
    Write-Host "`n3. Start Services:" -ForegroundColor $Yellow
    Write-Host "   ollama serve" -ForegroundColor $White
    Write-Host "   cd ai_core && python start_ai_core.py" -ForegroundColor $White
    Write-Host "   cd backend && cargo run" -ForegroundColor $White
    Write-Host "   cd genesis-frontend && npm run tauri dev" -ForegroundColor $White
    
    Write-Host "`n4. Run Tests:" -ForegroundColor $Yellow
    Write-Host "   python ai_core/test_ollama.py" -ForegroundColor $White
    Write-Host "   python ai_core/test_api.py" -ForegroundColor $White
}

# Main validation function
function Start-Validation {
    Write-Host "�� Genesis Validation Script" -ForegroundColor $Blue
    Write-Host "=" * 50 -ForegroundColor $Blue
    
    $results = @{
        "NodeJS" = Test-NodeJS
        "Rust" = Test-Rust
        "Python" = Test-Python
        "Git" = Test-Git
        "Ollama" = Test-Ollama
        "PythonPackages" = Test-PythonPackages
        "ProjectStructure" = Test-ProjectStructure
        "Services" = Test-Services
    }
    
    $passed = ($results.Values | Where-Object { $_ -eq $true }).Count
    $total = $results.Count
    
    Write-Host "`n�� Validation Results:" -ForegroundColor $Blue
    Write-Host "=" * 30 -ForegroundColor $Blue
    Write-Host "Passed: $passed/$total" -ForegroundColor $(if ($passed -eq $total) { $Green } else { $Yellow })
    
    foreach ($check in $results.GetEnumerator()) {
        $status = if ($check.Value) { "✅ PASS" } else { "❌ FAIL" }
        $color = if ($check.Value) { $Green } else { $Red }
        Write-Host "  $($check.Key): $status" -ForegroundColor $color
    }
    
    if ($passed -eq $total) {
        Write-Host "`n�� All checks passed! Genesis is ready to use." -ForegroundColor $Green
        return 0
    }
    else {
        Write-Host "`n⚠️  Some checks failed. See setup instructions below." -ForegroundColor $Yellow
        Show-SetupInstructions
        return 1
    }
}

# Run validation
if ($MyInvocation.InvocationName -ne '.') {
    exit (Start-Validation)
} 