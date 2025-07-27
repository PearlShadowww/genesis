# Genesis Folder System

## Overview

The Genesis system now automatically creates a `genesis` folder in your Documents directory and generates prompt-specific projects in separate folders. The LLM orchestrates the entire process, deciding what files are needed based on your prompt.

## How It Works

### 1. **Automatic Folder Creation**
- Creates `Documents/genesis/` folder automatically
- Each project gets its own subfolder with a descriptive name
- LLM generates project names based on the prompt content

### 2. **LLM Orchestration**
- **Project Naming**: LLM suggests descriptive project names (e.g., "react-todo-app", "python-web-scraper")
- **File Structure**: LLM determines what files are needed for each project type
- **Content Generation**: LLM creates complete, working file contents
- **Folder Organization**: Each project is saved in its own folder

### 3. **Prompt-Specific Generation**
The LLM analyzes your prompt and generates appropriate files:

#### **React Projects**
- `package.json` with React dependencies
- `src/App.js` or `src/App.tsx` main component
- `src/components/` for component files
- `public/index.html` for HTML template
- `README.md` with setup instructions

#### **Python Projects**
- `requirements.txt` with Python dependencies
- `main.py` or specific Python files
- `.gitignore` for Python projects
- `README.md` with usage instructions

#### **Node.js Projects**
- `package.json` with Express/Node dependencies
- `app.js` or `index.js` main server file
- `routes/` for API routes
- `models/` for data models
- `.env` or `.env.example` for environment variables

## File Structure

```
Documents/
└── genesis/
    ├── react-todo-app/
    │   ├── package.json
    │   ├── src/
    │   │   ├── App.js
    │   │   ├── components/
    │   │   └── styles/
    │   ├── public/
    │   └── README.md
    ├── python-web-scraper/
    │   ├── requirements.txt
    │   ├── main.py
    │   ├── .gitignore
    │   └── README.md
    └── node-auth-api/
        ├── package.json
        ├── app.js
        ├── routes/
        ├── models/
        └── README.md
```

## Usage Examples

### **Frontend Prompt**
```
"Create a React todo app with add, delete, and mark complete functionality"
```

**Generated Files:**
- `package.json` with React dependencies
- `src/App.js` - Main React component
- `src/components/Todo.js` - Todo component
- `src/styles/App.css` - Styling
- `public/index.html` - HTML template
- `README.md` - Setup instructions

### **Backend Prompt**
```
"Create a Node.js Express API server with user authentication"
```

**Generated Files:**
- `package.json` with Express dependencies
- `app.js` - Main server file
- `routes/auth.js` - Authentication routes
- `models/User.js` - User model
- `.env` - Environment variables
- `README.md` - API documentation

### **Python Prompt**
```
"Create a Python web scraper that extracts data from websites"
```

**Generated Files:**
- `requirements.txt` with scraping libraries
- `main.py` - Main scraper script
- `.gitignore` - Python-specific ignores
- `README.md` - Usage instructions

## Benefits

1. **Organized Structure**: Each project has its own folder
2. **Descriptive Names**: LLM generates meaningful project names
3. **Complete Projects**: All necessary files are included
4. **Working Code**: Files contain actual implementation
5. **Easy Access**: All projects in one location (`Documents/genesis/`)

## Testing

Run the test script to verify the system:

```bash
python test_prompt_specific_generation.py
```

This will test:
- React project generation
- Python project generation  
- Node.js project generation
- Separate folder creation

## Frontend Integration

The frontend now shows:
- Project path in the history sidebar
- File previews with actual content
- Download functionality for individual files
- Real-time generation status

## Next Steps

1. **Start the services:**
   ```bash
   # Terminal 1: Backend
   cd backend && cargo run
   
   # Terminal 2: AI Core
   cd ai_core && python main.py
   
   # Terminal 3: Frontend
   cd genesis-frontend && npm run tauri dev
   ```

2. **Use the frontend:**
   - Enter your project description
   - Click "Generate Project"
   - Watch files get created in `Documents/genesis/[project-name]/`

3. **Access your projects:**
   - Navigate to `Documents/genesis/`
   - Each project is in its own folder
   - Open and run the projects directly

The system now provides a complete, organized way to generate and manage AI-created projects! 🚀 