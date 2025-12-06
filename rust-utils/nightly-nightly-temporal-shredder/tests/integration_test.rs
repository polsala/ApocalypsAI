use super::{plan_shredding, FileToProcess, ShredAction, parse_duration};
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};
use chrono::{Duration, Utc, DateTime};

#[test]
fn test_parse_duration_valid() {
    assert_eq!(parse_duration("7d").unwrap(), Duration::days(7));
    assert_eq!(parse_duration("30m").unwrap(), Duration::minutes(30));
    assert_eq!(parse_duration("1h").unwrap(), Duration::hours(1));
    assert_eq!(parse_duration("120s").unwrap(), Duration::seconds(120));
}

#[test]
fn test_parse_duration_invalid_unit() {
    assert!(parse_duration("1w").is_err());
    assert!(parse_duration("5x").is_err());
}

#[test]
fn test_parse_duration_invalid_number() {
    assert!(parse_duration("ad").is_err());
    assert!(parse_duration("1.5h").is_err());
}

#[test]
fn test_plan_shredding_no_old_files() {
    let archive_dir = PathBuf::from("/archive");
    let older_than = Duration::days(7);
    let delete_originals = false;

    // # Mock rationale: We manually construct FileToProcess with SystemTime values
    // # that are *newer* than the `older_than` threshold relative to a conceptual `Utc::now()`.
    // # This avoids actual filesystem interaction and ensures deterministic results.
    let now_minus_1_day = (Utc::now() - Duration::days(1)).into();
    let now_minus_6_days = (Utc::now() - Duration::days(6)).into();

    let files = vec![
        FileToProcess {
            path: PathBuf::from("/source/file1.log"),
            modified_time: now_minus_1_day,
        },
        FileToProcess {
            path: PathBuf::from("/source/file2.txt"),
            modified_time: now_minus_6_days,
        },
    ];

    let actions = plan_shredding(files, older_than, &archive_dir, delete_originals);
    assert!(actions.is_empty());
}

#[test]
fn test_plan_shredding_with_old_files() {
    let archive_dir = PathBuf::from("/archive");
    let older_than = Duration::days(7);
    let delete_originals = true;

    // # Mock rationale: We manually construct FileToProcess with SystemTime values.
    // # `now_minus_10_days` is older than 7 days, `now_minus_5_days` is not.
    // # This allows deterministic testing of the age-based filtering logic.
    let now_minus_10_days = (Utc::now() - Duration::days(10)).into();
    let now_minus_5_days = (Utc::now() - Duration::days(5)).into();

    let files = vec![
        FileToProcess {
            path: PathBuf::from("/source/old_file.log"),
            modified_time: now_minus_10_days,
        },
        FileToProcess {
            path: PathBuf::from("/source/recent_file.txt"),
            modified_time: now_minus_5_days,
        },
    ];

    let actions = plan_shredding(files, older_than, &archive_dir, delete_originals);

    assert_eq!(actions.len(), 1);
    assert_eq!(
        actions[0],
        ShredAction::Compress {
            source_path: PathBuf::from("/source/old_file.log"),
            dest_path: PathBuf::from("/archive/old_file.log.gz"),
            delete_original: true,
        }
    );
}

#[test]
fn test_plan_shredding_multiple_old_files_no_delete() {
    let archive_dir = PathBuf::from("/archive");
    let older_than = Duration::hours(24); // 1 day
    let delete_originals = false;

    // # Mock rationale: Manually set SystemTime for files.
    // # `now_minus_2_days` and `now_minus_30_hours` are older than 24 hours.
    // # `now_minus_12_hours` is not.
    let now_minus_2_days = (Utc::now() - Duration::days(2)).into();
    let now_minus_30_hours = (Utc::now() - Duration::hours(30)).into();
    let now_minus_12_hours = (Utc::now() - Duration::hours(12)).into();

    let files = vec![
        FileToProcess {
            path: PathBuf::from("/data/logs/app.log"),
            modified_time: now_minus_2_days,
        },
        FileToProcess {
            path: PathBuf::from("/data/reports/report.csv"),
            modified_time: now_minus_30_hours,
        },
        FileToProcess {
            path: PathBuf::from("/data/config/current.conf"),
            modified_time: now_minus_12_hours,
        },
    ];

    let actions = plan_shredding(files, older_than, &archive_dir, delete_originals);

    assert_eq!(actions.len(), 2);
    assert!(actions.contains(&ShredAction::Compress {
        source_path: PathBuf::from("/data/logs/app.log"),
        dest_path: PathBuf::from("/archive/app.log.gz"),
        delete_original: false,
    }));
    assert!(actions.contains(&ShredAction::Compress {
        source_path: PathBuf::from("/data/reports/report.csv"),
        dest_path: PathBuf::from("/archive/report.csv.gz"),
        delete_original: false,
    }));
    assert!(!actions.contains(&ShredAction::Compress {
        source_path: PathBuf::from("/data/config/current.conf"),
        dest_path: PathBuf::from("/archive/current.conf.gz"),
        delete_original: false,
    }));
}

#[test]
fn test_plan_shredding_empty_file_list() {
    let archive_dir = PathBuf::from("/archive");
    let older_than = Duration::days(1);
    let delete_originals = false;

    let files = vec![];
    let actions = plan_shredding(files, older_than, &archive_dir, delete_originals);
    assert!(actions.is_empty());
}

#[test]
fn test_file_name_with_no_extension() {
    let archive_dir = PathBuf::from("/archive");
    let older_than = Duration::days(1);
    let delete_originals = false;

    let now_minus_2_days = (Utc::now() - Duration::days(2)).into();

    let files = vec![
        FileToProcess {
            path: PathBuf::from("/source/no_ext_file"),
            modified_time: now_minus_2_days,
        },
    ];

    let actions = plan_shredding(files, older_than, &archive_dir, delete_originals);
    assert_eq!(actions.len(), 1);
    assert_eq!(
        actions[0],
        ShredAction::Compress {
            source_path: PathBuf::from("/source/no_ext_file"),
            dest_path: PathBuf::from("/archive/no_ext_file.gz"),
            delete_original: false,
        }
    );
}
