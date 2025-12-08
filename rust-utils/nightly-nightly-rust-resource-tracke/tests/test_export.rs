use nightly_rust_resource_tracker::export::*;
use nightly_rust_resource_tracker::Resource;
use std::fs;
use tempfile::TempDir;

#[cfg(test)]
mod tests {
    use super::*;
    
    fn create_test_resource() -> Resource {
        Resource {
            id: 1,
            name: "Test Resource".to_string(),
            quantity: 100,
            category: "test".to_string(),
            expires: Some("2025-12-31".to_string()),
            location: Some("Storage".to_string()),
            created_at: "2024-01-01T00:00:00Z".to_string(),
            updated_at: "2024-01-01T00:00:00Z".to_string(),
        }
    }
    
    #[test]
    fn test_export_to_json() {
        let temp_dir = tempfile::tempdir().unwrap();
        let output_path = temp_dir.path().join("test.json");
        let output_path_str = output_path.to_str().unwrap().to_string();
        
        let resources = vec![create_test_resource()];
        
        let result = to_json(&resources, &output_path_str);
        assert!(result.is_ok());
        
        // Verify file was created
        assert!(output_path.exists());
        
        // Verify content
        let content = fs::read_to_string(&output_path).unwrap();
        assert!(content.contains("Test Resource"));
        assert!(content.contains("100"));
        assert!(content.contains("test"));
    }
    
    #[test]
    fn test_export_to_csv() {
        let temp_dir = tempfile::tempdir().unwrap();
        let output_path = temp_dir.path().join("test.csv");
        let output_path_str = output_path.to_str().unwrap().to_string();
        
        let resources = vec![create_test_resource()];
        
        let result = to_csv(&resources, &output_path_str);
        assert!(result.is_ok());
        
        // Verify file was created
        assert!(output_path.exists());
        
        // Verify content
        let content = fs::read_to_string(&output_path).unwrap();
        let lines: Vec<&str> = content.lines().collect();
        assert_eq!(lines.len(), 1); // One data row
        assert!(lines[0].contains("Test Resource"));
        assert!(lines[0].contains("100"));
    }
    
    #[test]
    fn test_export_to_yaml() {
        let temp_dir = tempfile::tempdir().unwrap();
        let output_path = temp_dir.path().join("test.yaml");
        let output_path_str = output_path.to_str().unwrap().to_string();
        
        let resources = vec![create_test_resource()];
        
        let result = to_yaml(&resources, &output_path_str);
        assert!(result.is_ok());
        
        // Verify file was created
        assert!(output_path.exists());
        
        // Verify content
        let content = fs::read_to_string(&output_path).unwrap();
        assert!(content.contains("Test Resource"));
        assert!(content.contains("100"));
        assert!(content.contains("test"));
    }
    
    #[test]
    fn test_export_resource_conversion() {
        let resource = create_test_resource();
        let export_resource: ExportResource = (&resource).into();
        
        assert_eq!(export_resource.name, "Test Resource");
        assert_eq!(export_resource.quantity, 100);
        assert_eq!(export_resource.category, "test");
        assert_eq!(export_resource.expires, Some("2025-12-31".to_string()));
        assert_eq!(export_resource.location, Some("Storage".to_string()));
        assert_eq!(export_resource.created_at, "2024-01-01T00:00:00Z");
        assert_eq!(export_resource.updated_at, "2024-01-01T00:00:00Z");
    }
}
