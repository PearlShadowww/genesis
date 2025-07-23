use actix_web::{HttpResponse, ResponseError};
use serde::{Deserialize, Serialize};
use std::fmt;

#[derive(Debug, Serialize, Deserialize)]
pub struct ApiError {
    pub code: String,
    pub message: String,
    pub details: Option<String>,
    pub timestamp: chrono::DateTime<chrono::Utc>,
}

impl ApiError {
    pub fn new(code: &str, message: &str) -> Self {
        Self {
            code: code.to_string(),
            message: message.to_string(),
            details: None,
            timestamp: chrono::Utc::now(),
        }
    }

    pub fn with_details(mut self, details: &str) -> Self {
        self.details = Some(details.to_string());
        self
    }
}

#[derive(Debug)]
pub enum GenesisError {
    DatabaseError(String),
    AiCoreError(String),
    ValidationError(String),
    TimeoutError(String),
    InternalError(String),
    NotFoundError(String),
}

impl fmt::Display for GenesisError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            GenesisError::DatabaseError(msg) => write!(f, "Database error: {}", msg),
            GenesisError::AiCoreError(msg) => write!(f, "AI Core error: {}", msg),
            GenesisError::ValidationError(msg) => write!(f, "Validation error: {}", msg),
            GenesisError::TimeoutError(msg) => write!(f, "Timeout error: {}", msg),
            GenesisError::InternalError(msg) => write!(f, "Internal error: {}", msg),
            GenesisError::NotFoundError(msg) => write!(f, "Not found: {}", msg),
        }
    }
}

impl ResponseError for GenesisError {
    fn error_response(&self) -> HttpResponse {
        let (status_code, error_code, message) = match self {
            GenesisError::DatabaseError(_) => (500, "DATABASE_ERROR", "Database operation failed"),
            GenesisError::AiCoreError(_) => (503, "AI_CORE_ERROR", "AI Core service unavailable"),
            GenesisError::ValidationError(_) => (400, "VALIDATION_ERROR", "Invalid request data"),
            GenesisError::TimeoutError(_) => (408, "TIMEOUT_ERROR", "Request timed out"),
            GenesisError::InternalError(_) => (500, "INTERNAL_ERROR", "Internal server error"),
            GenesisError::NotFoundError(_) => (404, "NOT_FOUND", "Resource not found"),
        };

        let api_error = ApiError::new(error_code, message)
            .with_details(&self.to_string());

        HttpResponse::build(status_code).json(api_error)
    }
}

impl From<reqwest::Error> for GenesisError {
    fn from(err: reqwest::Error) -> Self {
        if err.is_timeout() {
            GenesisError::TimeoutError(err.to_string())
        } else if err.is_connect() {
            GenesisError::AiCoreError("Failed to connect to AI Core".to_string())
        } else {
            GenesisError::InternalError(err.to_string())
        }
    }
}

impl From<serde_json::Error> for GenesisError {
    fn from(err: serde_json::Error) -> Self {
        GenesisError::ValidationError(format!("JSON parsing error: {}", err))
    }
}

impl From<std::io::Error> for GenesisError {
    fn from(err: std::io::Error) -> Self {
        GenesisError::InternalError(format!("IO error: {}", err))
    }
} 