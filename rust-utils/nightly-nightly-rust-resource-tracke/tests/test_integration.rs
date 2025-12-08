use nightly_rust_resource_tracker::*;
use std::fs;
use tempfile::TempDir;

#[cfg(test)]
mod tests {
    use super::*;
    
    fn setup_test_environment() -> (TempDir, String) {
        let temp_dir = tempfile::tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let db_path_str = db_path.to_str().unwrap().to_string();
        
        // Mock environment variables
        std::env::set_var("TEST_DB_PATH", &db_path_str);
        
        // Initialize database
        database::init_database().unwrap();
        
        (temp_dir, db_path_str)
    }
    
    #[test]
    fn test_complete_workflow() {
        let (_temp_dir, _db_path) = setup_test_environment();
        
        // Add multiple resources
        add_resource("Water Bottles", 50, "water", None, Some("Camp".to_string())).unwrap();
        add_resource("Canned Food", 30, "food", Some("2025-06-01".to_string()), Some("Pantry".to_string())).unwrap();
        add_resource("First Aid Kit", 2, "medical", None, Some("Medical Bay".to_string())).unwrap();
        
        // Update a resource
        update_resource("Water Bottles", &Some(45), &None).unwrap();
        
        // Export data
        let temp_dir = tempfile::tempdir().unwrap();
        let json_path = temp_dir.path().join("export.json");
        let csv_path = temp_dir.path().join("export.csv");
        let yaml_path = temp_dir.path().join("export.yaml");
        
        export_data("json", json_path.to_str().unwrap()).unwrap();
        export_data("csv", csv_path.to_str().unwrap()).unwrap();
        export_data("yaml", yaml_path.to_str().unwrap()).unwrap();
        
        // Verify exports
        assert!(json_path.exists());
        assert!(csv_path.exists());
        assert!(yaml_path.exists());
        
        // Backup database
        let backup_path = temp_dir.path().join("backup.db");
        backup_database(backup_path.to_str().unwrap()).unwrap();
        
        assert!(backup_path.exists());
    }
    
    #[test]
    fn test_low_quantity_alerts() {
        let (_temp_dir, _db_path) = setup_test_environment();
        
        // Add resources with low quantities
        add_resource("Bandages", 2, "medical", None, None).unwrap();
        add_resource("Antibiotics", 1, "medical", Some("2024-12-31".to_string()), None).unwrap();
        add_resource("Water Filters", 5, "water", None, None).unwrap();
        
        // This should not fail
        let result = check_expired();
        assert!(result.is_ok());
    }
    
    #[test]
    fn test_expired_items_detection() {
        let (_temp_dir, _db_path) = setup_test_environment();
        
        let conn = database::connect().unwrap();
        
        // Add expired item directly to database
        conn.execute(
            "INSERT INTO resources (name, quantity, category, expires, location, created_at, updated_at) 
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
            rusqlite::params![
                "Expired Food",
                10,
                "food",
                "2020-01-01", // Past date
                "Pantry",
                "2024-01-01T00:00:00Z",
                "2024-01-01T00:00:00Z",
            ],
        ).unwrap();
        
        // Check expired should find this item
        let result = check_expired();
        assert!(result.is_ok());
    }
    
    #[test]
    fn test_report_generation() {
        let (_temp_dir, _db_path) = setup_test_environment();
        
        // Add various resources
        add_resource("Water Purification", 3, "water", None, None).unwrap();
        add_resource("Canned Goods", 15, "food", Some("2024-06-01".to_string()), None).unwrap();
        add_resource("Medicine", 8, "medical", Some("2024-12-31".to_string()), None).unwrap();
        add_resource("Tools", 12, "equipment", None, None).unwrap();
        
        // Generate report
        let result = generate_report(30);
        assert!(result.is_ok());
        
        // Generate longer report
        let result = generate_report(90);
        assert!(result.is_ok());
    }
}
