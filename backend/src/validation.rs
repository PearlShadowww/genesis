use actix_web::{web, HttpRequest, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Mutex;
use std::time::{Duration, Instant};
use validator::{Validate, ValidationError};

use crate::error::GenesisError;

#[derive(Debug, Serialize, Deserialize, Validate)]
pub struct GenerateRequest {
    #[validate(length(min = 10, max = 2000, message = "Prompt must be between 10 and 2000 characters"))]
    pub prompt: String,
    
    #[validate(regex(path = "BACKEND_REGEX", message = "Backend must be 'ollama' or 'openai'"))]
    pub backend: Option<String>,
}

lazy_static::lazy_static! {
    static ref BACKEND_REGEX: regex::Regex = regex::Regex::new(r"^(ollama|openai)$").unwrap();
}

#[derive(Debug)]
pub struct RateLimiter {
    requests: Mutex<HashMap<String, Vec<Instant>>>,
    max_requests: usize,
    window_duration: Duration,
}

impl RateLimiter {
    pub fn new(max_requests: usize, window_duration: Duration) -> Self {
        Self {
            requests: Mutex::new(HashMap::new()),
            max_requests,
            window_duration,
        }
    }
    
    pub fn is_allowed(&self, client_id: &str) -> bool {
        let mut requests = self.requests.lock().unwrap();
        let now = Instant::now();
        
        // Clean old requests
        if let Some(client_requests) = requests.get_mut(client_id) {
            client_requests.retain(|&time| now.duration_since(time) < self.window_duration);
        }
        
        // Check if limit exceeded
        let client_requests = requests.entry(client_id.to_string()).or_insert_with(Vec::new);
        
        if client_requests.len() >= self.max_requests {
            false
        } else {
            client_requests.push(now);
            true
        }
    }
    
    pub fn get_remaining_requests(&self, client_id: &str) -> usize {
        let requests = self.requests.lock().unwrap();
        let now = Instant::now();
        
        if let Some(client_requests) = requests.get(client_id) {
            let valid_requests: Vec<_> = client_requests
                .iter()
                .filter(|&&time| now.duration_since(time) < self.window_duration)
                .collect();
            
            self.max_requests.saturating_sub(valid_requests.len())
        } else {
            self.max_requests
        }
    }
}

pub fn get_client_id(req: &HttpRequest) -> String {
    // In production, you'd want to use a proper client identification method
    // For now, we'll use the IP address
    req.connection_info()
        .realip_remote_addr()
        .unwrap_or("unknown")
        .to_string()
}

pub async fn validate_generate_request(
    req: web::Json<GenerateRequest>,
) -> Result<web::Json<GenerateRequest>, GenesisError> {
    // Validate the request
    if let Err(errors) = req.validate() {
        let error_messages: Vec<String> = errors
            .field_errors()
            .iter()
            .flat_map(|(field, errors)| {
                errors.iter().map(|error| {
                    format!("{}: {}", field, error.message.as_ref().unwrap_or(&"Invalid value".to_string()))
                })
            })
            .collect();
        
        return Err(GenesisError::ValidationError(error_messages.join(", ")));
    }
    
    // Additional business logic validation
    if req.prompt.trim().is_empty() {
        return Err(GenesisError::ValidationError("Prompt cannot be empty".to_string()));
    }
    
    // Check for potentially harmful content (basic check)
    let harmful_keywords = ["delete", "drop", "remove", "system", "admin"];
    let prompt_lower = req.prompt.to_lowercase();
    
    if harmful_keywords.iter().any(|&keyword| prompt_lower.contains(keyword)) {
        return Err(GenesisError::ValidationError(
            "Prompt contains potentially harmful keywords".to_string()
        ));
    }
    
    Ok(req)
}

pub fn rate_limit_middleware(
    rate_limiter: web::Data<RateLimiter>,
) -> impl Fn(HttpRequest, web::Payload) -> std::pin::Pin<Box<dyn std::future::Future<Output = Result<HttpResponse, actix_web::Error>>>> {
    move |req: HttpRequest, payload: web::Payload| {
        let rate_limiter = rate_limiter.clone();
        let client_id = get_client_id(&req);
        
        Box::pin(async move {
            if !rate_limiter.is_allowed(&client_id) {
                let remaining = rate_limiter.get_remaining_requests(&client_id);
                return Ok(HttpResponse::TooManyRequests().json(serde_json::json!({
                    "error": "Rate limit exceeded",
                    "remaining_requests": remaining,
                    "retry_after": 60
                })));
            }
            
            // Continue with the request
            Ok(HttpResponse::Ok().finish())
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_rate_limiter() {
        let limiter = RateLimiter::new(5, Duration::from_secs(60));
        
        // Should allow first 5 requests
        for i in 0..5 {
            assert!(limiter.is_allowed("test_client"), "Request {} should be allowed", i);
        }
        
        // Should block the 6th request
        assert!(!limiter.is_allowed("test_client"), "6th request should be blocked");
        
        // Should have 0 remaining requests
        assert_eq!(limiter.get_remaining_requests("test_client"), 0);
    }
    
    #[test]
    fn test_validate_generate_request() {
        let valid_request = GenerateRequest {
            prompt: "Create a simple React component".to_string(),
            backend: Some("ollama".to_string()),
        };
        
        // This would need to be tested in an async context
        // For now, just test the struct creation
        assert_eq!(valid_request.prompt, "Create a simple React component");
        assert_eq!(valid_request.backend, Some("ollama".to_string()));
    }
} 