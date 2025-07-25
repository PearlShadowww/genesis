use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use mongodb::bson::oid::ObjectId;
use validator::Validate;

#[derive(Debug, Serialize, Deserialize, Clone, Validate)]
pub struct GeneratedFile {
    pub name: String,
    pub content: String,
    pub language: String,
    pub size: Option<u64>,
    pub last_modified: Option<DateTime<Utc>>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub enum ProjectStatus {
    Pending,
    Generating,
    Completed,
    Failed,
}

#[derive(Debug, Serialize, Deserialize, Clone, Validate)]
pub struct ProjectRecord {
    #[serde(rename = "_id", skip_serializing_if = "Option::is_none")]
    pub id: Option<ObjectId>,
    pub project_id: String,
    pub prompt: String,
    pub files: Vec<GeneratedFile>,
    pub output: String,
    pub status: ProjectStatus,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    pub backend: String,
    pub metadata: Option<serde_json::Value>,
}

#[derive(Debug, Serialize, Deserialize, Clone, Validate)]
pub struct GenerateRequest {
    #[validate(length(min = 1, message = "Prompt cannot be empty"))]
    pub prompt: String,
    pub backend: Option<String>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub message: String,
    pub data: Option<T>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct HealthResponse {
    pub status: String,
    pub timestamp: DateTime<Utc>,
    pub services: std::collections::HashMap<String, String>,
}

// MongoDB-specific models
#[derive(Debug, Serialize, Deserialize)]
pub struct ProjectQuery {
    pub project_id: Option<String>,
    pub status: Option<ProjectStatus>,
    pub limit: Option<i64>,
    pub skip: Option<u64>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ProjectUpdate {
    pub status: Option<ProjectStatus>,
    pub files: Option<Vec<GeneratedFile>>,
    pub output: Option<String>,
    pub metadata: Option<serde_json::Value>,
}

impl ProjectRecord {
    pub fn new(project_id: String, prompt: String, backend: String) -> Self {
        let now = Utc::now();
        
        Self {
            id: None,
            project_id,
            prompt,
            files: Vec::new(),
            output: String::new(),
            status: ProjectStatus::Generating,
            created_at: now,
            updated_at: now,
            backend,
            metadata: None,
        }
    }

    #[allow(dead_code)]
    pub fn update_status(&mut self, status: ProjectStatus) {
        self.status = status;
        self.updated_at = Utc::now();
    }

    #[allow(dead_code)]
    pub fn add_files(&mut self, files: Vec<GeneratedFile>) {
        self.files = files;
        self.updated_at = Utc::now();
    }

    #[allow(dead_code)]
    pub fn set_output(&mut self, output: String) {
        self.output = output;
        self.updated_at = Utc::now();
    }
} 