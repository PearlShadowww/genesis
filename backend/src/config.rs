use serde::{Deserialize, Serialize};
use std::env;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    pub server: ServerConfig,
    pub ai_core: AiCoreConfig,
    pub logging: LoggingConfig,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ServerConfig {
    pub host: String,
    pub port: u16,
    pub workers: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AiCoreConfig {
    pub url: String,
    pub timeout_seconds: u64,
    pub max_retries: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LoggingConfig {
    pub level: String,
    pub format: String,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            server: ServerConfig {
                host: "127.0.0.1".to_string(),
                port: 8080,
                workers: num_cpus::get(),
            },
            ai_core: AiCoreConfig {
                url: "http://127.0.0.1:8000".to_string(),
                timeout_seconds: 300, // 5 minutes
                max_retries: 3,
            },
            logging: LoggingConfig {
                level: "info".to_string(),
                format: "json".to_string(),
            },
        }
    }
}

impl Config {
    pub fn from_env() -> Self {
        let mut config = Config::default();
        
        // Server configuration
        if let Ok(host) = env::var("GENESIS_HOST") {
            config.server.host = host;
        }
        if let Ok(port) = env::var("GENESIS_PORT") {
            if let Ok(port_num) = port.parse() {
                config.server.port = port_num;
            }
        }
        if let Ok(workers) = env::var("GENESIS_WORKERS") {
            if let Ok(workers_num) = workers.parse() {
                config.server.workers = workers_num;
            }
        }
        
        // AI Core configuration
        if let Ok(url) = env::var("AI_CORE_URL") {
            config.ai_core.url = url;
        }
        if let Ok(timeout) = env::var("AI_CORE_TIMEOUT") {
            if let Ok(timeout_num) = timeout.parse() {
                config.ai_core.timeout_seconds = timeout_num;
            }
        }
        if let Ok(retries) = env::var("AI_CORE_MAX_RETRIES") {
            if let Ok(retries_num) = retries.parse() {
                config.ai_core.max_retries = retries_num;
            }
        }
        
        // Logging configuration
        if let Ok(level) = env::var("LOG_LEVEL") {
            config.logging.level = level;
        }
        if let Ok(format) = env::var("LOG_FORMAT") {
            config.logging.format = format;
        }
        
        config
    }
    
    pub fn server_url(&self) -> String {
        format!("{}:{}", self.server.host, self.server.port)
    }
    
    pub fn ai_core_health_url(&self) -> String {
        format!("{}/health", self.ai_core.url)
    }
    
    pub fn ai_core_run_url(&self) -> String {
        format!("{}/run", self.ai_core.url)
    }
} 