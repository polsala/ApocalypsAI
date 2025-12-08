use rusqlite::{Connection, Result};
use std::path::Path;
use std::fs;

pub fn get_db_path() -> String {
    let home = std::env::var("HOME").unwrap_or_else(|_| ".".to_string());
    let db_path = format!("{}/.config/resource-tracker/resources.db", home);
    
    if let Some(parent) = Path::new(&db_path).parent() {
        fs::create_dir_all(parent).unwrap_or_default();
    }
    
    db_path
}

pub fn connect() -> Result<Connection> {
    let db_path = get_db_path();
    Connection::open(db_path)
}

pub fn init_database() -> Result<()> {
    let conn = connect()?;
    
    conn.execute(
        "CREATE TABLE IF NOT EXISTS resources (
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
    )?;
    
    Ok(())
}
