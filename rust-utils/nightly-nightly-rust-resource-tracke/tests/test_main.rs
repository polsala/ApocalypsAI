use nightly_rust_resource_tracker::*;
use rusqlite::Connection;
use std::fs;
use tempfile::TempDir;

#[cfg(test)]
mod tests {
    use super::*;
    
    fn setup_test_db() -> (TempDir, String) {
        let temp_dir = tempfile::tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let db_path_str = db_path.to_str().unwrap().to_string();
        
        // Mock the get_db_path function
        std::env::set_var("TEST_DB_PATH", &db_path_str);
        
        let conn = Connection::open(&db_path).unwrap();
        conn.execute(
            "CREATE TABLE resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                category TEXT NOT NULL,
                expires TEXT,
                location TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )",
            [],
        ).unwrap();
        
        (temp_dir, db_path_str)
    }
    
    #[test]
    fn test_add_resource() {
        let (_temp_dir, _db_path) = setup_test_db();
        
        let result = add_resource("Water Purification Tablets", 50, "supplies", None, None);
        assert!(result.is_ok());
    }
    
    #[test]
    fn test_update_resource() {
        let (_temp_dir, _db_path) = setup_test_db();
        
        // Add a resource first
        add_resource("Canned Food", 20, "food", None, None).unwrap();
        
        // Update it
        let result = update_resource("Canned Food", &Some(15), &Some("Pantry".to_string()));
        assert!(result.is_ok());
    }
    
    #[test]
    fn test_remove_resource() {
        let (_temp_dir, _db_path) = setup_test_db();
        
        // Add a resource first
        add_resource("First Aid Kit", 2, "medical", None, None).unwrap();
        
        // Remove it
        let result = remove_resource("First Aid Kit");
        assert!(result.is_ok());
    }
    
    #[test]
    fn test_resource_creation() {
        let resource = Resource::new(
            "Test Resource".to_string(),
            100,
            "test".to_string(),
            None,
            None,
        );
        
        assert_eq!(resource.name, "Test Resource");
        assert_eq!(resource.quantity, 100);
        assert_eq!(resource.category, "test");
        assert!(resource.expires.is_none());
        assert!(resource.location.is_none());
        assert!(!resource.created_at.is_empty());
        assert!(!resource.updated_at.is_empty());
    }
    
    #[test]
    fn test_resource_with_expiration() {
        let resource = Resource::new(
            "Perishable Item".to_string(),
            50,
            "food".to_string(),
            Some("2025-12-31".to_string()),
            Some("Refrigerator".to_string()),
        );
        
        assert_eq!(resource.name, "Perishable Item");
        assert_eq!(resource.quantity, 50);
        assert_eq!(resource.category, "food");
        assert_eq!(resource.expires, Some("2025-12-31".to_string()));
        assert_eq!(resource.location, Some("Refrigerator".to_string()));
    }
}
