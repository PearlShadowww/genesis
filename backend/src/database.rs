use mongodb::{Client, Database, Collection};
use mongodb::bson::{doc, Document, to_bson};
use futures_util::stream::TryStreamExt;
use crate::models::{ProjectRecord, ProjectQuery, ProjectUpdate};
use anyhow::Result;
use log::{info, error, warn};

pub struct DatabaseService {
    db: Database,
}

impl DatabaseService {
    pub async fn new(connection_string: &str, database_name: &str) -> Result<Self> {
        let client = Client::with_uri_str(connection_string).await?;
        let db = client.database(database_name);
        
        info!("Connected to MongoDB database: {}", database_name);
        
        Ok(Self { db })
    }

    pub fn projects_collection(&self) -> Collection<ProjectRecord> {
        self.db.collection("projects")
    }

    pub async fn create_project(&self, project: ProjectRecord) -> Result<()> {
        let collection = self.projects_collection();
        
        match collection.insert_one(project, None).await {
            Ok(result) => {
                info!("Created project with ID: {:?}", result.inserted_id);
                Ok(())
            }
            Err(e) => {
                error!("Failed to create project: {}", e);
                Err(anyhow::anyhow!("Database error: {}", e))
            }
        }
    }

    pub async fn get_project(&self, project_id: &str) -> Result<Option<ProjectRecord>> {
        let collection = self.projects_collection();
        
        let filter = doc! { "project_id": project_id };
        
        match collection.find_one(filter, None).await {
            Ok(project) => {
                if project.is_some() {
                    info!("Retrieved project: {}", project_id);
                } else {
                    warn!("Project not found: {}", project_id);
                }
                Ok(project)
            }
            Err(e) => {
                error!("Failed to get project {}: {}", project_id, e);
                Err(anyhow::anyhow!("Database error: {}", e))
            }
        }
    }

    pub async fn update_project(&self, project_id: &str, update: ProjectUpdate) -> Result<()> {
        let collection = self.projects_collection();
        
        let mut update_doc = Document::new();
        
        if let Some(status) = update.status {
            update_doc.insert("status", to_bson(&status)?);
        }
        
        if let Some(files) = update.files {
            update_doc.insert("files", to_bson(&files)?);
        }
        
        if let Some(output) = update.output {
            update_doc.insert("output", output);
        }
        
        if let Some(metadata) = update.metadata {
            update_doc.insert("metadata", to_bson(&metadata)?);
        }
        
        update_doc.insert("updated_at", to_bson(&chrono::Utc::now())?);
        
        let filter = doc! { "project_id": project_id };
        let update = doc! { "$set": update_doc };
        
        match collection.update_one(filter, update, None).await {
            Ok(result) => {
                if result.modified_count > 0 {
                    info!("Updated project: {}", project_id);
                } else {
                    warn!("No changes made to project: {}", project_id);
                }
                Ok(())
            }
            Err(e) => {
                error!("Failed to update project {}: {}", project_id, e);
                Err(anyhow::anyhow!("Database error: {}", e))
            }
        }
    }

    pub async fn list_projects(&self, query: ProjectQuery) -> Result<Vec<ProjectRecord>> {
        let collection = self.projects_collection();
        
        let mut filter = Document::new();
        
        if let Some(project_id) = query.project_id {
            filter.insert("project_id", project_id);
        }
        
        if let Some(status) = query.status {
            filter.insert("status", to_bson(&status)?);
        }
        
        let mut options = mongodb::options::FindOptions::default();
        
        if let Some(limit) = query.limit {
            options.limit = Some(limit);
        }
        
        if let Some(skip) = query.skip {
            options.skip = Some(skip);
        }
        
        // Sort by created_at descending (newest first)
        options.sort = Some(doc! { "created_at": -1 });
        
        match collection.find(filter, options).await {
            Ok(cursor) => {
                let projects: Vec<ProjectRecord> = cursor.try_collect().await?;
                info!("Retrieved {} projects", projects.len());
                Ok(projects)
            }
            Err(e) => {
                error!("Failed to list projects: {}", e);
                Err(anyhow::anyhow!("Database error: {}", e))
            }
        }
    }

    #[allow(dead_code)]
    pub async fn delete_project(&self, project_id: &str) -> Result<bool> {
        let collection = self.projects_collection();
        
        let filter = doc! { "project_id": project_id };
        
        match collection.delete_one(filter, None).await {
            Ok(result) => {
                if result.deleted_count > 0 {
                    info!("Deleted project: {}", project_id);
                    Ok(true)
                } else {
                    warn!("Project not found for deletion: {}", project_id);
                    Ok(false)
                }
            }
            Err(e) => {
                error!("Failed to delete project {}: {}", project_id, e);
                Err(anyhow::anyhow!("Database error: {}", e))
            }
        }
    }

    #[allow(dead_code)]
    pub async fn get_project_stats(&self) -> Result<serde_json::Value> {
        let collection = self.projects_collection();
        
        let pipeline = vec![
            doc! {
                "$group": {
                    "_id": "$status",
                    "count": { "$sum": 1 }
                }
            }
        ];
        
        match collection.aggregate(pipeline, None).await {
            Ok(cursor) => {
                let docs: Vec<Document> = cursor.try_collect().await?;
                let mut stats = serde_json::Map::new();
                
                for doc in docs {
                    if let (Some(status), Some(count)) = (doc.get_str("_id").ok(), doc.get_i32("count").ok()) {
                        stats.insert(status.to_string(), serde_json::Value::Number(count.into()));
                    }
                }
                
                Ok(serde_json::Value::Object(stats))
            }
            Err(e) => {
                error!("Failed to get project stats: {}", e);
                Err(anyhow::anyhow!("Database error: {}", e))
            }
        }
    }
} 