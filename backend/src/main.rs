use actix_web::{web, App, HttpServer, HttpResponse, Result, middleware::Logger};
use actix_cors::Cors;
use chrono::Utc;
use log::{info, error};
use std::sync::Arc;
use std::collections::HashMap;
use uuid::Uuid;
use anyhow::Result as AnyhowResult;

// Import our modules
mod models;
mod database;

use models::*;
use database::DatabaseService;

// App state with MongoDB
struct AppState {
    db: Arc<DatabaseService>,
}

impl AppState {
    async fn new() -> AnyhowResult<Self> {
        let connection_string = std::env::var("MONGODB_URI")
            .unwrap_or_else(|_| "mongodb://localhost:27017".to_string());
        let database_name = std::env::var("MONGODB_DB")
            .unwrap_or_else(|_| "genesis".to_string());
        
        let db = DatabaseService::new(&connection_string, &database_name).await?;
        
        Ok(Self {
            db: Arc::new(db),
        })
    }
}

// API endpoints
async fn health() -> Result<HttpResponse> {
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
    
    Ok(HttpResponse::Ok().json(ApiResponse {
        success: true,
        message: "Backend is healthy".to_string(),
        data: Some(response),
    }))
}

async fn generate_project(
    data: web::Json<GenerateRequest>,
    app_state: web::Data<AppState>,
) -> Result<HttpResponse> {
    let project_id = Uuid::new_v4().to_string();
    
    info!("Starting project generation: {}", project_id);
    
    // Create initial project record
    let project_record = ProjectRecord::new(
        project_id.clone(),
        data.prompt.clone(),
        data.backend.clone().unwrap_or_else(|| "ollama".to_string()),
    );
    
    // Store in MongoDB
    let db = app_state.db.clone();
    match db.create_project(project_record).await {
        Ok(_) => {
            // Start async generation process
            let app_state_clone = app_state.clone();
            let project_id_clone = project_id.clone();
            let prompt_clone = data.prompt.clone();
            let backend_clone = data.backend.clone().unwrap_or_else(|| "ollama".to_string());
            
            tokio::spawn(async move {
                generate_project_async(project_id_clone, prompt_clone, backend_clone, app_state_clone).await;
            });
            
            Ok(HttpResponse::Accepted().json(ApiResponse {
                success: true,
                message: "Project generation started".to_string(),
                data: Some(project_id),
            }))
        }
        Err(e) => {
            error!("Failed to create project in DB: {}", e);
            Ok(HttpResponse::InternalServerError().json(ApiResponse::<String> {
                success: false,
                message: "Failed to start project generation".to_string(),
                data: None,
            }))
        }
    }
}

async fn get_projects(app_state: web::Data<AppState>) -> Result<HttpResponse> {
    let db = app_state.db.clone();
    let query = ProjectQuery {
        project_id: None,
        status: None,
        limit: Some(100),
        skip: Some(0),
    };
    
    match db.list_projects(query).await {
        Ok(project_list) => {
            Ok(HttpResponse::Ok().json(ApiResponse {
                success: true,
                message: "Projects retrieved successfully".to_string(),
                data: Some(project_list),
            }))
        }
        Err(e) => {
            error!("Failed to get projects from DB: {}", e);
            Ok(HttpResponse::InternalServerError().json(ApiResponse::<Vec<ProjectRecord>> {
                success: false,
                message: "Failed to retrieve projects".to_string(),
                data: None,
            }))
        }
    }
}

async fn get_project(
    path: web::Path<String>,
    app_state: web::Data<AppState>,
) -> Result<HttpResponse> {
    let project_id = path.into_inner();
    let db = app_state.db.clone();
    
    match db.get_project(&project_id).await {
        Ok(Some(project)) => {
            Ok(HttpResponse::Ok().json(ApiResponse {
                success: true,
                message: "Project retrieved successfully".to_string(),
                data: Some(project),
            }))
        }
        Ok(None) => {
            Ok(HttpResponse::NotFound().json(ApiResponse::<ProjectRecord> {
                success: false,
                message: "Project not found".to_string(),
                data: None,
            }))
        }
        Err(e) => {
            error!("Failed to get project from DB: {}", e);
            Ok(HttpResponse::InternalServerError().json(ApiResponse::<ProjectRecord> {
                success: false,
                message: "Failed to retrieve project".to_string(),
                data: None,
            }))
        }
    }
}

// Helper functions
async fn check_ai_core_health() -> String {
    let client = reqwest::Client::new();
    match client
        .get("http://127.0.0.1:8000/health")
        .timeout(std::time::Duration::from_secs(10))
        .send()
        .await
    {
        Ok(response) => {
            if response.status().is_success() {
                match response.json::<serde_json::Value>().await {
                    Ok(data) => {
                        if data.get("success").and_then(|s| s.as_bool()).unwrap_or(false) {
                            "healthy".to_string()
                        } else {
                            "unhealthy".to_string()
                        }
                    }
                    Err(_) => "unhealthy".to_string()
                }
            } else {
                format!("unhealthy (status: {})", response.status())
            }
        }
        Err(e) => {
            error!("AI Core health check failed: {}", e);
            "unreachable".to_string()
        }
    }
}

async fn generate_project_async(
    project_id: String,
    prompt: String,
    backend: String,
    app_state: web::Data<AppState>,
) {
    // Update status to generating
    let db = app_state.db.clone();
    let update = ProjectUpdate {
        status: Some(ProjectStatus::Generating),
        files: None,
        output: None,
        metadata: None,
    };
    
    if let Err(e) = db.update_project(&project_id, update).await {
        error!("Failed to update project status to generating: {}", e);
        return;
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
        .timeout(std::time::Duration::from_secs(300))
        .send()
        .await
    {
        Ok(response) => {
            if response.status().is_success() {
                match response.json::<serde_json::Value>().await {
                    Ok(data) => {
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
    let db = app_state.db.clone();
    
    // Parse files from AI core response
    let mut files = Vec::new();
    if let Some(files_array) = data.get("data").and_then(|d| d.get("files")).and_then(|f| f.as_array()) {
        for file in files_array {
            if let (Some(name), Some(content), Some(language)) = (
                file.get("name").and_then(|n| n.as_str()),
                file.get("content").and_then(|c| c.as_str()),
                file.get("language").and_then(|l| l.as_str()),
            ) {
                files.push(GeneratedFile {
                    name: name.to_string(),
                    content: content.to_string(),
                    language: language.to_string(),
                    size: None,
                    last_modified: None,
                });
            }
        }
    }
    
    // Parse output
    let output = data.get("data")
        .and_then(|d| d.get("output"))
        .and_then(|o| o.as_str())
        .unwrap_or("")
        .to_string();
    
    let update = ProjectUpdate {
        status: Some(ProjectStatus::Completed),
        files: Some(files),
        output: Some(output),
        metadata: None,
    };
    
    match db.update_project(&project_id, update).await {
        Ok(_) => {
            info!("Project {} completed successfully", project_id);
        }
        Err(e) => {
            error!("Failed to update project with results: {}", e);
            mark_project_failed(project_id, "Failed to update project with results".to_string(), app_state).await;
        }
    }
}

async fn mark_project_failed(
    project_id: String,
    error_message: String,
    app_state: web::Data<AppState>,
) {
    let db = app_state.db.clone();
    let update = ProjectUpdate {
        status: Some(ProjectStatus::Failed),
        files: None,
        output: Some(error_message.clone()),
        metadata: None,
    };
    
    if let Err(e) = db.update_project(&project_id, update).await {
        error!("Failed to mark project as failed: {}", e);
        return;
    }
    
    info!("Project {} failed: {}", project_id, error_message);
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init();
    
    let app_state = match AppState::new().await {
        Ok(state) => web::Data::new(state),
        Err(e) => {
            error!("Failed to initialize database: {}", e);
            return Err(std::io::Error::new(std::io::ErrorKind::Other, e));
        }
    };
    
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
            .wrap(Logger::default())
            .route("/health", web::get().to(health))
            .route("/generate", web::post().to(generate_project))
            .route("/projects", web::get().to(get_projects))
            .route("/projects/{id}", web::get().to(get_project))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
} 