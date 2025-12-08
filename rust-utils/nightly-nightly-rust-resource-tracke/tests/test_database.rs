use nightly_rust_resource_tracker::database::*;
use rusqlite::Connection;
use std::fs;
use tempfile::TempDir;

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_get_db_path() {
        let db_path = get_db_path();
        assert!(db_path.contains(".config"));
        assert!(db_path.contains("resource-tracker"));
        assert!(db_path.ends_with("resources.db"));
    }
    
    #[test]
    fn test_connect_to_database() {
        let result = connect();
        assert!(result.is_ok());
    }
    
    #[test]
    fn test_init_database() {
        let temp_dir = tempfile::tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let db_path_str = db_path.to_str().unwrap().to_string();
        
        std::env::set_var("TEST_DB_PATH", &db_path_str);
        
        let result = init_database();
        assert!(result.is_ok());
        
        // Verify table was created
        let conn = Connection::open(&db_path).unwrap();
        let mut stmt = conn.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='resources'";
        let table_exists: bool = stmt.exists([]).unwrap();
        assert!(table_exists);
    }
    
    #[test]
    fn test_database_operations() {
        let temp_dir = tempfile::tempdir().unwrap();
        let db_path = temp_dir.path().join("test.db");
        let db_path_str = db_path.to_str().unwrap().to_string();
        
        std::env::set_var("TEST_DB_PATH", &db_path_str);
        
        // Initialize database
        init_database().unwrap();
        
        let conn = Connection::open(&db_path).unwrap();
        
        // Test insert
        conn.execute(
            "INSERT INTO resources (name, quantity, category, expires, location, created_at, updated_at) 
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
            rusqlite::params![
                "Test Item",
                10,
                "test",
                None::<String>,
                None::<String>,
                "2024-01-01T00:00:00Z",
                "2024-01-01T00:00:00Z",
            ],
        ).unwrap();
        
        // Test select
        let mut stmt = conn.prepare("SELECT COUNT(*) FROM resources").unwrap();
        let count: i64 = stmt.query_row([], |row| row.get(0)).unwrap();
        assert_eq!(count, 1);
    }
}
