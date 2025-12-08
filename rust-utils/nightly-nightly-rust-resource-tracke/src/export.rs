use serde::{Deserialize, Serialize};
use std::fs;
use std::io::Write;

#[derive(Debug, Serialize, Deserialize)]
pub struct ExportResource {
    pub name: String,
    pub quantity: i32,
    pub category: String,
    pub expires: Option<String>,
    pub location: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

impl From<&super::Resource> for ExportResource {
    fn from(resource: &super::Resource) -> Self {
        ExportResource {
            name: resource.name.clone(),
            quantity: resource.quantity,
            category: resource.category.clone(),
            expires: resource.expires.clone(),
            location: resource.location.clone(),
            created_at: resource.created_at.clone(),
            updated_at: resource.updated_at.clone(),
        }
    }
}

pub fn to_json(resources: &[super::Resource], path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let export_resources: Vec<ExportResource> = resources.iter().map(ExportResource::from).collect();
    let json = serde_json::to_string_pretty(&export_resources)?;
    fs::write(path, json)?;
    Ok(())
}

pub fn to_csv(resources: &[super::Resource], path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let mut wtr = csv::Writer::from_path(path)?;
    
    for resource in resources {
        wtr.write_record(&[
            &resource.name,
            &resource.quantity.to_string(),
            &resource.category,
            &resource.expires.clone().unwrap_or_default(),
            &resource.location.clone().unwrap_or_default(),
            &resource.created_at,
            &resource.updated_at,
        ])?;
    }
    
    wtr.flush()?;
    Ok(())
}

pub fn to_yaml(resources: &[super::Resource], path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let export_resources: Vec<ExportResource> = resources.iter().map(ExportResource::from).collect();
    let yaml = serde_yaml::to_string(&export_resources)?;
    fs::write(path, yaml)?;
    Ok(())
}
