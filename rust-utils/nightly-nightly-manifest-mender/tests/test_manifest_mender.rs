use super::*;
use tempfile::tempdir;
use std::io::Cursor;

// Mock rationale: Using in-memory Cursor for input/output streams and tempfile for disk operations
// ensures tests are deterministic, isolated, and do not rely on actual file system state.

#[test]
fn test_parse_valid_yaml() {
    let yaml_content = r#"
cache_id: "TestCache"
location: "TestLocation"
last_inspected: "2024-07-20T10:00:00Z"
resources:
  - item: "Water"
    quantity: 10
    unit: "liters"
    status: "Good"
"#;
    let reader = Cursor::new(yaml_content);
    let manifest = parse_manifest(reader, "yaml").unwrap();
    assert_eq!(manifest.cache_id, "TestCache");
    assert_eq!(manifest.resources.len(), 1);
    assert_eq!(manifest.resources[0].item, "Water");
}

#[test]
fn test_parse_invalid_json() {
    let json_content = r#"
{
  "cache_id": "TestCache",
  "location": "TestLocation",
  "last_inspected": "2024-07-20T10:00:00Z",
  "resources": [
    {
      "item": "Water",
      "quantity": "ten", // Invalid type
      "unit": "liters"
    }
  ]
}
"#;
    let reader = Cursor::new(json_content);
    let result = parse_manifest(reader, "json");
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("invalid type: string"));
}

#[test]
fn test_mend_missing_status() {
    let yaml_content = r#"
cache_id: "TestCache"
location: "TestLocation"
last_inspected: "2024-07-20T10:00:00Z"
resources:
  - item: "Canned Food"
    quantity: 5
    unit: "cans"
"#;
    let reader = Cursor::new(yaml_content);
    let mut manifest = parse_manifest(reader, "yaml").unwrap();
    let actions = manifest.mend(true);
    assert_eq!(manifest.resources[0].status, "Unknown");
    assert!(actions.iter().any(|s| s.contains("Defaulted status for 'Canned Food' to 'Unknown'.")));
}

#[test]
fn test_mend_invalid_date() {
    let yaml_content = r#"
cache_id: "TestCache"
location: "TestLocation"
last_inspected: "not-a-date"
resources:
  - item: "Canned Food"
    quantity: 5
    unit: "cans"
"#;
    let reader = Cursor::new(yaml_content);
    let mut manifest = parse_manifest(reader, "yaml").unwrap();
    let actions = manifest.mend(true);
    assert!(chrono::DateTime::parse_from_rfc3339(&manifest.last_inspected).is_ok());
    assert!(actions.iter().any(|s| s.contains("Mended 'last_inspected' from 'not-a-date' to current UTC time due to invalid format.")));
}

#[test]
fn test_mend_missing_unit() {
    let yaml_content = r#"
cache_id: "TestCache"
location: "TestLocation"
last_inspected: "2024-07-20T10:00:00Z"
resources:
  - item: "First Aid Kit"
    quantity: 1
    status: "Good"
  - item: "Water Purifier"
    quantity: 1
    status: "Good"
  - item: "Ammo Box"
    quantity: 200
"#;
    let reader = Cursor::new(yaml_content);
    let mut manifest = parse_manifest(reader, "yaml").unwrap();
    let actions = manifest.mend(true);
    assert_eq!(manifest.resources[0].unit, "kit");
    assert_eq!(manifest.resources[1].unit, "unit"); // Water Purifier is a 'unit'
    assert_eq!(manifest.resources[2].unit, "round"); // Ammo Box is 'round'
    assert!(actions.iter().any(|s| s.contains("Mended unit for 'First Aid Kit' from '' to 'kit'.")));
    assert!(actions.iter().any(|s| s.contains("Mended unit for 'Ammo Box' from '' to 'round'.")));
}

#[test]
fn test_end_to_end_yaml_to_json() {
    let yaml_content = r#"
cache_id: "E2ECache"
location: "E2ELocation"
last_inspected: "2024-07-20T10:00:00Z"
resources:
  - item: "Emergency Rations"
    quantity: 3
    unit: "packs"
  - item: "Medical Kit"
    quantity: 1
"#;
    let input_reader = Cursor::new(yaml_content);
    let mut manifest = parse_manifest(input_reader, "yaml").unwrap();
    manifest.mend(false);

    let mut output_buffer = Vec::new();
    serialize_manifest(Cursor::new(&mut output_buffer), &manifest, "json").unwrap();
    let json_output = String::from_utf8(output_buffer).unwrap();

    let expected_json_part_medical_kit = r#""item":"Medical Kit","quantity":1,"unit":"kit","status":"Unknown""#;
    let expected_json_part_rations = r#""item":"Emergency Rations","quantity":3,"unit":"packs","status":"Unknown""#;
    assert!(json_output.contains(expected_json_part_medical_kit));
    assert!(json_output.contains(expected_json_part_rations));
}

#[test]
fn test_main_check_only_simulated() -> Result<(), String> {
    let dir = tempdir().unwrap();
    let input_path = dir.path().join("test_input.yaml");
    fs::write(&input_path, r#"
cache_id: "CheckOnlyCache"
location: "CheckOnlyLocation"
last_inspected: "2024-07-20T10:00:00Z"
resources:
  - item: "Water"
    quantity: 10
    unit: "liters"
"#).map_err(|e| e.to_string())?;

    // Mock rationale: Instead of calling main() directly (which exits the process),
    // we simulate its core logic path to test the --check-only flag's effect.
    // This ensures the parsing and mending logic is executed, but no output file is created.
    let file = fs::File::open(&input_path).map_err(|e| format!("Failed to open input file '{}': {}", input_path.display(), e))?;
    let mut manifest = parse_manifest(file, "yaml")?;
    let mending_actions = manifest.mend(false); // verbose = false for this test

    // If check_only were true, the main function would return Ok(()) here without writing output.
    // We assert that the mending logic ran (even if no actions were taken in this specific valid case)
    // and that no error occurred during parsing/mending.
    assert!(mending_actions.is_empty()); // For this specific input, no mending is needed.
    Ok(())
}

#[test]
fn test_main_output_file_simulated() -> Result<(), String> {
    let dir = tempdir().unwrap();
    let input_path = dir.path().join("test_input.json");
    let output_path = dir.path().join("test_output.toml");
    fs::write(&input_path, r#"
{
  "cache_id": "OutputFileCache",
  "location": "OutputFileLocation",
  "last_inspected": "2024-07-20T10:00:00Z",
  "resources": [
    {
      "item": "First Aid Kit",
      "quantity": 1
    }
  ]
}
"#).map_err(|e| e.to_string())?;

    // Mock rationale: Instead of calling main(), we simulate its core logic path
    // to avoid process-level side effects and allow direct assertion on file content.
    let file = fs::File::open(&input_path).map_err(|e| format!("Failed to open input file '{}': {}", input_path.display(), e))?;
    let mut manifest = parse_manifest(file, "json")?;
    let _mending_actions = manifest.mend(true); // verbose = true to test mending actions

    let output_file = fs::File::create(&output_path).map_err(|e| format!("Failed to create output file '{}': {}", output_path.display(), e))?;
    serialize_manifest(output_file, &manifest, "toml")?;

    let output_content = fs::read_to_string(&output_path).map_err(|e| e.to_string())?;
    assert!(output_content.contains("cache_id = \"OutputFileCache\""));
    assert!(output_content.contains("item = \"First Aid Kit\""));
    assert!(output_content.contains("unit = \"kit\"")); // Mended unit
    assert!(output_content.contains("status = \"Unknown\"")); // Defaulted status

    Ok(())
}
