pub mod resource_tracker {
    use serde::{Deserialize, Serialize};
    use std::collections::HashMap;
    use std::fs;
    use std::time::{SystemTime, UNIX_EPOCH};
    
    #[derive(Debug, Clone, Serialize, Deserialize)]
    pub struct Resource {
        pub name: String,
        pub quantity: u32,
        pub category: String,
        pub last_updated: u64,
    }
    
    #[derive(Debug, Serialize, Deserialize)]
    pub struct ResourceTracker {
        resources: HashMap<String, Resource>,
    }
    
    impl ResourceTracker {
        pub fn new() -> Self {
            Self {
                resources: HashMap::new(),
            }
        }
        
        pub fn load() -> Result<Self, Box<dyn std::error::Error>> {
            let data = fs::read_to_string("resources.json")?;
            Ok(serde_json::from_str(&data)?)
        }
        
        pub fn save(&self) -> Result<(), Box<dyn std::error::Error>> {
            let data = serde_json::to_string_pretty(self)?;
            fs::write("resources.json", data)?;
            Ok(())
        }
        
        pub fn add_resource(&mut self, name: String, quantity: u32, category: String) {
            let now = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs();
            
            let resource = Resource {
                name: name.clone(),
                quantity,
                category,
                last_updated: now,
            };
            
            self.resources.insert(name, resource);
        }
        
        pub fn get_resource(&self, name: &str) -> Option<&Resource> {
            self.resources.get(name)
        }
        
        pub fn get_all_resources(&self) -> Vec<&Resource> {
            self.resources.values().collect()
        }
        
        pub fn update_quantity(&mut self, name: String, quantity: u32) -> Result<(), String> {
            match self.resources.get_mut(&name) {
                Some(resource) => {
                    resource.quantity = quantity;
                    resource.last_updated = SystemTime::now()
                        .duration_since(UNIX_EPOCH)
                        .unwrap()
                        .as_secs();
                    Ok(())
                },
                None => Err(format!("Resource '{}' not found", name)),
            }
        }
        
        pub fn remove_resource(&mut self, name: String) -> Result<(), String> {
            match self.resources.remove(&name) {
                Some(_) => Ok(()),
                None => Err(format!("Resource '{}' not found", name)),
            }
        }
        
        pub fn get_total_quantity(&self) -> u32 {
            self.resources.values().map(|r| r.quantity).sum()
        }
        
        pub fn get_category_totals(&self) -> HashMap<String, u32> {
            self.resources.values()
                .fold(HashMap::new(), |mut acc, r| {
                    *acc.entry(r.category.clone()).or_insert(0) += r.quantity;
                    acc
                })
        }
    }
    
    #[cfg(test)]
    mod tests {
        use super::*;
        use std::fs;
        
        #[test]
        fn test_new_tracker() {
            let tracker = ResourceTracker::new();
            assert!(tracker.get_all_resources().is_empty());
        }
        
        #[test]
        fn test_add_resource() {
            let mut tracker = ResourceTracker::new();
            tracker.add_resource("Water".to_string(), 100, "Essentials".to_string());
            
            let resources = tracker.get_all_resources();
            assert_eq!(resources.len(), 1);
            assert_eq!(resources[0].name, "Water");
            assert_eq!(resources[0].quantity, 100);
            assert_eq!(resources[0].category, "Essentials");
        }
        
        #[test]
        fn test_update_quantity() {
            let mut tracker = ResourceTracker::new();
            tracker.add_resource("Water".to_string(), 100, "Essentials".to_string());
            
            assert!(tracker.update_quantity("Water".to_string(), 150).is_ok());
            assert_eq!(tracker.get_resource("Water").unwrap().quantity, 150);
            
            assert!(tracker.update_quantity("Nonexistent".to_string(), 50).is_err());
        }
        
        #[test]
        fn test_remove_resource() {
            let mut tracker = ResourceTracker::new();
            tracker.add_resource("Water".to_string(), 100, "Essentials".to_string());
            
            assert!(tracker.remove_resource("Water".to_string()).is_ok());
            assert!(tracker.get_resource("Water").is_none());
            
            assert!(tracker.remove_resource("Nonexistent".to_string()).is_err());
        }
        
        #[test]
        fn test_get_total_quantity() {
            let mut tracker = ResourceTracker::new();
            tracker.add_resource("Water".to_string(), 100, "Essentials".to_string());
            tracker.add_resource("Food".to_string(), 50, "Essentials".to_string());
            
            assert_eq!(tracker.get_total_quantity(), 150);
        }
        
        #[test]
        fn test_get_category_totals() {
            let mut tracker = ResourceTracker::new();
            tracker.add_resource("Water".to_string(), 100, "Essentials".to_string());
            tracker.add_resource("Food".to_string(), 50, "Essentials".to_string());
            tracker.add_resource("Weapons".to_string(), 10, "Defense".to_string());
            
            let category_totals = tracker.get_category_totals();
            assert_eq!(category_totals.get("Essentials"), Some(&150));
            assert_eq!(category_totals.get("Defense"), Some(&10));
        }
        
        #[test]
        fn test_save_and_load() {
            let mut tracker = ResourceTracker::new();
            tracker.add_resource("Water".to_string(), 100, "Essentials".to_string());
            tracker.save().unwrap();
            
            let loaded_tracker = ResourceTracker::load().unwrap();
            assert_eq!(loaded_tracker.get_all_resources().len(), 1);
            assert_eq!(loaded_tracker.get_resource("Water").unwrap().quantity, 100);
            
            // Cleanup
            fs::remove_file("resources.json").ok();
        }
    }
}
