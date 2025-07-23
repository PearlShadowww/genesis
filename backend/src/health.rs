use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::{Duration, Instant};
use tokio::time::timeout;

use crate::config::Config;
use crate::error::GenesisError;

#[derive(Debug, Serialize, Deserialize)]
pub struct HealthStatus {
    pub status: String,
    pub timestamp: chrono::DateTime<chrono::Utc>,
    pub version: String,
    pub uptime: Duration,
    pub services: HashMap<String, ServiceHealth>,
    pub system: SystemInfo,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ServiceHealth {
    pub status: String,
    pub response_time: Option<f64>,
    pub last_check: chrono::DateTime<chrono::Utc>,
    pub error: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct SystemInfo {
    pub memory_usage: f64,
    pub cpu_usage: f64,
    pub active_connections: usize,
}

pub async fn health_check(config: web::Data<Config>) -> impl Responder {
    let start_time = Instant::now();
    
    let mut services = HashMap::new();
    
    // Check AI Core health
    let ai_core_health = check_ai_core_health(&config).await;
    services.insert("ai_core".to_string(), ai_core_health);
    
    // Check Ollama health
    let ollama_health = check_ollama_health().await;
    services.insert("ollama".to_string(), ollama_health);
    
    // Determine overall status
    let overall_status = if services.values().all(|s| s.status == "healthy") {
        "healthy"
    } else {
        "degraded"
    };
    
    let health_status = HealthStatus {
        status: overall_status.to_string(),
        timestamp: chrono::Utc::now(),
        version: env!("CARGO_PKG_VERSION").to_string(),
        uptime: start_time.elapsed(),
        services,
        system: get_system_info().await,
    };
    
    HttpResponse::Ok().json(health_status)
}

async fn check_ai_core_health(config: &Config) -> ServiceHealth {
    let start_time = Instant::now();
    
    match timeout(
        Duration::from_secs(5),
        reqwest::get(&config.ai_core_health_url())
    ).await {
        Ok(Ok(response)) => {
            let response_time = start_time.elapsed().as_secs_f64();
            
            if response.status().is_success() {
                ServiceHealth {
                    status: "healthy".to_string(),
                    response_time: Some(response_time),
                    last_check: chrono::Utc::now(),
                    error: None,
                }
            } else {
                ServiceHealth {
                    status: "unhealthy".to_string(),
                    response_time: Some(response_time),
                    last_check: chrono::Utc::now(),
                    error: Some(format!("HTTP {}", response.status())),
                }
            }
        }
        Ok(Err(e)) => ServiceHealth {
            status: "unhealthy".to_string(),
            response_time: Some(start_time.elapsed().as_secs_f64()),
            last_check: chrono::Utc::now(),
            error: Some(e.to_string()),
        },
        Err(_) => ServiceHealth {
            status: "unhealthy".to_string(),
            response_time: Some(start_time.elapsed().as_secs_f64()),
            last_check: chrono::Utc::now(),
            error: Some("Timeout".to_string()),
        },
    }
}

async fn check_ollama_health() -> ServiceHealth {
    let start_time = Instant::now();
    
    match timeout(
        Duration::from_secs(5),
        reqwest::get("http://localhost:11434/api/tags")
    ).await {
        Ok(Ok(response)) => {
            let response_time = start_time.elapsed().as_secs_f64();
            
            if response.status().is_success() {
                ServiceHealth {
                    status: "healthy".to_string(),
                    response_time: Some(response_time),
                    last_check: chrono::Utc::now(),
                    error: None,
                }
            } else {
                ServiceHealth {
                    status: "unhealthy".to_string(),
                    response_time: Some(response_time),
                    last_check: chrono::Utc::now(),
                    error: Some(format!("HTTP {}", response.status())),
                }
            }
        }
        Ok(Err(e)) => ServiceHealth {
            status: "unhealthy".to_string(),
            response_time: Some(start_time.elapsed().as_secs_f64()),
            last_check: chrono::Utc::now(),
            error: Some(e.to_string()),
        },
        Err(_) => ServiceHealth {
            status: "unhealthy".to_string(),
            response_time: Some(start_time.elapsed().as_secs_f64()),
            last_check: chrono::Utc::now(),
            error: Some("Timeout".to_string()),
        },
    }
}

async fn get_system_info() -> SystemInfo {
    // This is a simplified version. In production, you'd want to use
    // system monitoring libraries like `sysinfo`
    SystemInfo {
        memory_usage: 0.0, // Placeholder
        cpu_usage: 0.0,    // Placeholder
        active_connections: 0, // Placeholder
    }
}

pub async fn readiness_check() -> impl Responder {
    // Check if the service is ready to accept requests
    HttpResponse::Ok().json(serde_json::json!({
        "status": "ready",
        "timestamp": chrono::Utc::now(),
    }))
}

pub async fn liveness_check() -> impl Responder {
    // Check if the service is alive
    HttpResponse::Ok().json(serde_json::json!({
        "status": "alive",
        "timestamp": chrono::Utc::now(),
    }))
} 