use actix_cors::Cors;
use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use chrono::{DateTime, Utc};
use log::{info, error};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Mutex;
use uuid::Uuid;

// Data structures
#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ProjectRecord {
    pub id: String,
    pub prompt: String,
    pub files: Vec<GeneratedFile>,
    pub output: String,
    pub created_at: DateTime<Utc>,
    pub status: ProjectStatus,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct GeneratedFile {
    pub name: String,
    pub content: String,
    pub language: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub enum ProjectStatus {
    Pending,
    Generating,
    Completed,
    Failed,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct GenerateRequest {
    pub prompt: String,
    pub backend: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub message: String,
    pub data: Option<T>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct HealthResponse {
    pub status: String,
    pub timestamp: DateTime<Utc>,
    pub services: HashMap<String, String>,
}

// App state
struct AppState {
    projects: Mutex<HashMap<String, ProjectRecord>>,
}

impl AppState {
    fn new() -> Self {
        Self {
            projects: Mutex::new(HashMap::new()),
        }
    }
}

// API endpoints
async fn health() -> impl Responder {
    let mut services = HashMap::new();
    services.insert("backend".to_string(), "healthy".to_string());
    
    // Check AI core connectivity
    let ai_core_status = check_ai_core_health().await;
    services.insert("ai_core".to_string(), ai_core_status);
    
    let response = HealthResponse {
        status: "healthy".to_string(),
        timestamp: Utc::now(),
        services,
    };
    
    HttpResponse::Ok().json(ApiResponse {
        success: true,
        message: "Backend is healthy".to_string(),
        data: Some(response),
    })
}

async fn generate_project(
    data: web::Json<GenerateRequest>,
    app_state: web::Data<AppState>,
) -> impl Responder {
    let project_id = Uuid::new_v4().to_string();
    
    info!("Starting project generation: {}", project_id);
    
    // Create initial project record
    let project_record = ProjectRecord {
        id: project_id.clone(),
        prompt: data.prompt.clone(),
        files: Vec::new(),
        output: String::new(),
        created_at: Utc::now(),
        status: ProjectStatus::Pending,
    };
    
    // Store in memory
    {
        let mut projects = app_state.projects.lock().unwrap();
        projects.insert(project_id.clone(), project_record);
    }
    
    // Start async generation process
    let app_state_clone = app_state.clone();
    let prompt = data.prompt.clone();
    let backend = data.backend.clone().unwrap_or_else(|| "ollama".to_string());
    
    let project_id_clone = project_id.clone();
    tokio::spawn(async move {
        generate_project_async(project_id, prompt, backend, app_state_clone).await;
    });
    
    HttpResponse::Accepted().json(ApiResponse {
        success: true,
        message: "Project generation started".to_string(),
        data: Some(project_id_clone),
    })
}

async fn get_projects(app_state: web::Data<AppState>) -> impl Responder {
    let projects = app_state.projects.lock().unwrap();
    let project_list: Vec<ProjectRecord> = projects.values().cloned().collect();
    
    HttpResponse::Ok().json(ApiResponse {
        success: true,
        message: "Projects retrieved successfully".to_string(),
        data: Some(project_list),
    })
}

async fn get_project(
    path: web::Path<String>,
    app_state: web::Data<AppState>,
) -> impl Responder {
    let project_id = path.into_inner();
    let projects = app_state.projects.lock().unwrap();
    
    if let Some(project) = projects.get(&project_id) {
        HttpResponse::Ok().json(ApiResponse {
            success: true,
            message: "Project retrieved successfully".to_string(),
            data: Some(project.clone()),
        })
    } else {
        HttpResponse::NotFound().json(ApiResponse::<ProjectRecord> {
            success: false,
            message: "Project not found".to_string(),
            data: None,
        })
    }
}

// Helper functions
async fn check_ai_core_health() -> String {
    let client = reqwest::Client::new();
    match client
        .get("http://127.0.0.1:8000/health")
        .timeout(std::time::Duration::from_secs(5))
        .send()
        .await
    {
        Ok(response) => {
            if response.status().is_success() {
                "healthy".to_string()
            } else {
                "unhealthy".to_string()
            }
        }
        Err(_) => "unreachable".to_string(),
    }
}

async fn generate_project_async(
    project_id: String,
    prompt: String,
    backend: String,
    app_state: web::Data<AppState>,
) {
    // Update status to generating
    {
        let mut projects = app_state.projects.lock().unwrap();
        if let Some(project) = projects.get_mut(&project_id) {
            project.status = ProjectStatus::Generating;
        }
    }
    
    info!("Generating project {} with prompt: {}", project_id, prompt);
    
    // Call AI core
    let client = reqwest::Client::new();
    let request_body = serde_json::json!({
        "prompt": prompt,
        "backend": backend
    });
    
    match client
        .post("http://127.0.0.1:8000/run")
        .json(&request_body)
        .timeout(std::time::Duration::from_secs(300)) // 5 minutes timeout
        .send()
        .await
    {
        Ok(response) => {
            if response.status().is_success() {
                match response.json::<serde_json::Value>().await {
                    Ok(data) => {
                        // Parse AI core response and update project
                        update_project_with_results(project_id, data, app_state).await;
                    }
                    Err(e) => {
                        error!("Failed to parse AI core response: {}", e);
                        mark_project_failed(project_id, "Failed to parse AI core response".to_string(), app_state).await;
                    }
                }
            } else {
                error!("AI core returned error status: {}", response.status());
                mark_project_failed(project_id, "AI core returned error".to_string(), app_state).await;
            }
        }
        Err(e) => {
            error!("Failed to call AI core: {}", e);
            mark_project_failed(project_id, "Failed to connect to AI core".to_string(), app_state).await;
        }
    }
}

async fn update_project_with_results(
    project_id: String,
    data: serde_json::Value,
    app_state: web::Data<AppState>,
) {
    let mut projects = app_state.projects.lock().unwrap();
    if let Some(project) = projects.get_mut(&project_id) {
        // Parse files from AI core response
        if let Some(files_array) = data.get("files").and_then(|f| f.as_array()) {
            project.files = files_array
                .iter()
                .filter_map(|file| {
                    if let (Some(name), Some(content), Some(language)) = (
                        file.get("name").and_then(|n| n.as_str()),
                        file.get("content").and_then(|c| c.as_str()),
                        file.get("language").and_then(|l| l.as_str()),
                    ) {
                        Some(GeneratedFile {
                            name: name.to_string(),
                            content: content.to_string(),
                            language: language.to_string(),
                        })
                    } else {
                        None
                    }
                })
                .collect();
        }
        
        // Parse output
        if let Some(output) = data.get("output").and_then(|o| o.as_str()) {
            project.output = output.to_string();
        }
        
        project.status = ProjectStatus::Completed;
        info!("Project {} completed successfully", project_id);
    }
}

async fn mark_project_failed(
    project_id: String,
    error_message: String,
    app_state: web::Data<AppState>,
) {
    let mut projects = app_state.projects.lock().unwrap();
    if let Some(project) = projects.get_mut(&project_id) {
        project.status = ProjectStatus::Failed;
        project.output = error_message.clone();
        info!("Project {} failed: {}", project_id, error_message);
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init();
    
    let app_state = web::Data::new(AppState::new());
    
    info!("Starting Genesis Backend server on http://127.0.0.1:8080");
    
    HttpServer::new(move || {
        let cors = Cors::default()
            .allow_any_origin()
            .allow_any_method()
            .allow_any_header()
            .max_age(3600);
        
        App::new()
            .wrap(cors)
            .app_data(app_state.clone())
            .route("/health", web::get().to(health))
            .route("/generate", web::post().to(generate_project))
            .route("/projects", web::get().to(get_projects))
            .route("/projects/{id}", web::get().to(get_project))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
} 